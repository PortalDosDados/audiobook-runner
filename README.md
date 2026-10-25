# 🎧 Audiobook Runner

Transforme seus livros em **PDF** e **EPUB** em audiobooks organizados por capítulos ou compilados em um arquivo único contínuo, prontos para você ouvir no celular ou smartwatch enquanto corre ou treina.

---

## 🏃 Principais Recursos

- **Vozes Neurais Realistas**: Utiliza a tecnologia `edge-tts` com narração natural em português (*Francisca*, *Antonio*, *Thalita* e outras) sem custo e sem necessidade de chave de API paga.
- **Leitura de PDF e EPUB**: Limpeza automática de rodapés, cabeçalhos e números de páginas que atrapalhariam a narração.
- **Detecção Inteligente de Capítulos**: Cada capítulo vira uma faixa de áudio com tags ID3 (título, livro, autor, número de faixa), garantindo compatibilidade imediata com tocadores de smartwatch (Garmin, Apple Watch, etc.) e celulares.
- **Audiobook Completo (Arquivo Único)**: Compilação automática de todos os capítulos selecionados em um único arquivo `.mp3` contínuo e limpo, sem artefatos ou sobreposição de tags ID3 intermediárias, ideal para treinos longos e corridas contínuas.
- **Controle de Ritmo (Velocidade)**: Ajuste a velocidade de 0.8x a 1.8x (ótimo para manter um ritmo acelerado nos treinos).
- **Download Flexível**: Baixe o audiobook completo em `.mp3`, capítulos individuais ou o pacote `.zip` com todas as faixas ordenadas na sequência correta.

---

## 🚀 Como Executar

### Opção 1: Nuvem (Streamlit Community Cloud) - Direto no Celular
O projeto está pronto para deploy gratuito no **[Streamlit Community Cloud](https://share.streamlit.io/)**:
1. Conecte sua conta do GitHub ao Streamlit Cloud.
2. Selecione o repositório `PortalDosDados/audiobook-runner` (branch `master`) com arquivo principal `app.py`.
3. Clique em **Deploy**.
4. Acesse a URL gerada pelo celular (ex.: `https://audiobook-runner.streamlit.app`) e adicione à tela inicial para usar como um app nativo!

### Opção 2: Localmente no Computador

#### 1. Criar ambiente virtual e instalar dependências

```bash
# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

#### 2. Iniciar a aplicação local

```bash
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`. Na mesma rede Wi-Fi, o endereço `Network URL` exibido no terminal permite acessar a aplicação diretamente pelo navegador do celular.

---

## 📱 Dica para Corredores

1. Abra o app no celular ou no computador e converta o seu livro favorito.
2. Baixe o **Audiobook Completo (.MP3)** para treinos longos ou o arquivo `.zip` para manter os capítulos separados.
3. Se usar relógio esportivo (Garmin Express / Apple Watch), transfira o arquivo para o relógio ou abra no seu tocador favorito do smartphone.
4. Conecte o fone Bluetooth e boas passadas!
