import os
import io
import re
import asyncio
import streamlit as st
from src.extractors.pdf_extractor import PDFExtractor
from src.extractors.epub_extractor import EPUBExtractor
from src.tts.edge_tts_engine import EdgeTTSEngine, AVAILABLE_VOICES
from src.audio.audio_manager import AudioManager

st.set_page_config(
    page_title="Audiobook Runner",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling para visual moderno e esportivo
st.markdown(
    """
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF4B4B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 12px 16px;
        border-left: 4px solid #FF4B4B;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🎧 Audiobook Runner</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Converta seus livros em PDF e EPUB para ouvir enquanto corre ou treina.</div>',
    unsafe_allow_html=True,
)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("⚙️ Configurações de Voz")

    voice_options = {v["id"]: f"{v['name']}" for v in AVAILABLE_VOICES}
    selected_voice_id = st.selectbox(
        "Selecione o Narrador:",
        options=list(voice_options.keys()),
        format_func=lambda x: voice_options[x],
        index=0,
    )

    speed_multiplier = st.slider(
        "Velocidade de Reprodução:",
        min_value=0.8,
        max_value=1.8,
        value=1.1,
        step=0.05,
        help="Ideal para corridas: 1.1x a 1.25x permite absorver o conteúdo no ritmo do treino sem parecer acelerado demais.",
    )

    # Converte multiplicador em formato aceito pelo edge-tts (ex: +10%)
    speed_percent = int(round((speed_multiplier - 1.0) * 100))
    rate_str = f"{'+' if speed_percent >= 0 else ''}{speed_percent}%"

    st.markdown("---")
    st.subheader("🔊 Testar Prévia da Voz")
    sample_text = st.text_input(
        "Texto de teste:",
        value="Olá! Esta é a voz que vai narrar seu livro enquanto você corre.",
    )

    if st.button("Ouvir Amostra", use_container_width=True):
        with st.spinner("Gerando prévia..."):
            preview_engine = EdgeTTSEngine(voice=selected_voice_id, rate=rate_str)
            preview_path = "output/preview_sample.mp3"
            preview_engine.generate_speech_sync(sample_text, preview_path)
            st.audio(preview_path, format="audio/mp3")

    st.markdown("---")
    st.subheader("🧹 Gerenciamento de Espaço")
    if st.button(
        "🗑️ Limpar Áudios Antigos",
        help="Remove arquivos temporários e pacotes .zip para liberar espaço no disco.",
    ):
        import shutil

        if os.path.exists("output"):
            shutil.rmtree("output")
            os.makedirs("output", exist_ok=True)
        st.session_state.pop("generated_files", None)
        st.session_state.pop("zip_path", None)
        st.success("Pasta de saída limpa com sucesso!")

# ----------------- UPLOAD DE LIVRO -----------------
uploaded_file = st.file_uploader(
    "Carregue seu livro (PDF ou EPUB):",
    type=["pdf", "epub"],
    help="Envie um arquivo PDF ou EPUB para que o sistema extraia os capítulos e organize a narração.",
)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    clean_book_name = re.sub(r'[\/:*?"<>|]', "", os.path.splitext(file_name)[0])

    # Inicializa estado da sessão para armazenar capítulos
    if (
        "current_book" not in st.session_state
        or st.session_state.current_book != file_name
    ):
        with st.spinner("Processando e limpando o livro..."):
            if file_name.lower().endswith(".pdf"):
                extractor = PDFExtractor(io.BytesIO(file_bytes))
                chapters = extractor.extract_chapters()
            else:
                extractor = EPUBExtractor(io.BytesIO(file_bytes))
                chapters = extractor.extract_chapters()

            st.session_state.chapters = chapters
            st.session_state.current_book = file_name
            st.session_state.audio_files = {}

    chapters = st.session_state.chapters

    if not chapters:
        st.warning(
            "Nenhum capítulo ou texto legível foi encontrado neste arquivo. Verifique se o PDF não é composto apenas por imagens escaneadas."
        )
    else:
        # Métricas do Livro
        total_words = sum(c["word_count"] for c in chapters)
        # Média de narração ~150 palavras por minuto ajustado pela velocidade
        estimated_minutes = int(total_words / (150 * speed_multiplier))
        est_hours = estimated_minutes // 60
        est_mins = estimated_minutes % 60

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Capítulos", len(chapters))
        with col2:
            st.metric("Total de Palavras", f"{total_words:,}")
        with col3:
            st.metric("Duração Estimada", f"{est_hours}h {est_mins}m")

        st.markdown("---")

        # Seleção de Capítulos para Conversão
        st.subheader("📑 Capítulos Detectados")
        select_all = st.checkbox("Selecionar todos os capítulos", value=True)

        selected_chapters = []
        for ch in chapters:
            col_check, col_title, col_words = st.columns([1, 7, 2])
            with col_check:
                is_selected = st.checkbox("", value=select_all, key=f"ch_{ch['id']}")
                if is_selected:
                    selected_chapters.append(ch)
            with col_title:
                with st.expander(f"{ch['id']}. {ch['title']}"):
                    st.write(
                        ch["text"][:600] + ("..." if len(ch["text"]) > 600 else "")
                    )
            with col_words:
                st.caption(f"{ch['word_count']} palavras")

        st.markdown("---")

        # Botão de Conversão
        st.subheader("🎙️ Gerar Áudio")

        if st.button(
            "🚀 Iniciar Conversão dos Capítulos Selecionados",
            type="primary",
            use_container_width=True,
        ):
            if not selected_chapters:
                st.warning("Selecione pelo menos um capítulo para converter.")
            else:
                book_output_dir = os.path.join("output", "audiobooks", clean_book_name)
                os.makedirs(book_output_dir, exist_ok=True)

                audio_mgr = AudioManager()
                engine = EdgeTTSEngine(voice=selected_voice_id, rate=rate_str)

                progress_bar = st.progress(0)
                status_text = st.empty()

                total_sel = len(selected_chapters)
                generated_files = []

                for idx, ch in enumerate(selected_chapters):
                    status_text.text(
                        f"Convertendo capítulo {idx + 1} de {total_sel}: {ch['title']}"
                    )
                    sanitized_title = re.sub(r'[\/:*?"<>|]', "", ch["title"])[
                        :40
                    ].strip()
                    filename = f"{ch['id']:02d} - {sanitized_title}.mp3"
                    out_path = os.path.join(book_output_dir, filename)

                    # Gera o arquivo de áudio
                    engine.generate_speech_sync(ch["text"], out_path)

                    # Adiciona metadados para players e smartwatches
                    audio_mgr.tag_mp3(
                        file_path=out_path,
                        title=ch["title"],
                        book_title=clean_book_name,
                        track_num=ch["id"],
                        total_tracks=len(chapters),
                    )

                    generated_files.append((ch["title"], out_path))
                    progress_bar.progress((idx + 1) / total_sel)

                status_text.success("🎉 Conversão concluída com sucesso!")

                # Cria arquivo ZIP com todos os capítulos
                zip_filename = f"{clean_book_name}_audiobook.zip"
                zip_path = audio_mgr.create_zip_package(book_output_dir, zip_filename)

                st.session_state.zip_path = zip_path
                st.session_state.generated_files = generated_files

        # Se já tiver gerado os áudios
        if "generated_files" in st.session_state and st.session_state.generated_files:
            st.markdown("---")
            st.subheader("🎧 Seus Arquivos de Áudio Estão Prontos!")

            # Botão de download do ZIP completo
            if "zip_path" in st.session_state and os.path.exists(
                st.session_state.zip_path
            ):
                with open(st.session_state.zip_path, "rb") as f:
                    st.download_button(
                        label="📦 Baixar Todos os Capítulos (Arquivo .ZIP)",
                        data=f,
                        file_name=os.path.basename(st.session_state.zip_path),
                        mime="application/zip",
                        type="primary",
                    )

            # Players individuais para ouvir no navegador
            st.markdown("#### Ouvir ou Baixar por Capítulo:")
            for title, path in st.session_state.generated_files:
                if os.path.exists(path):
                    with st.container():
                        st.write(f"**{title}**")
                        st.audio(path, format="audio/mp3")
                        with open(path, "rb") as audio_file:
                            st.download_button(
                                label=f"⬇️ Baixar {os.path.basename(path)}",
                                data=audio_file,
                                file_name=os.path.basename(path),
                                mime="audio/mp3",
                                key=f"dl_{path}",
                            )
else:
    st.info("👆 Faça o upload de um arquivo PDF ou EPUB para começar.")
