# 🎧 Audiobook Runner

Transforme seus livros em **PDF** e **EPUB** em audiobooks organizados por capítulos, prontos para você ouvir no celular ou smartwatch enquanto corre ou treina.

---

## 🏃 Principais Recursos

- **Vozes Neurais Realistas**: Utiliza a tecnologia `edge-tts` com narração natural em português (*Francisca*, *Antonio*, *Thalita* e outras) sem custo e sem necessidade de chave de API paga.
- **Leitura de PDF e EPUB**: Limpeza automática de rodapés, cabeçalhos e números de páginas que atrapalhariam a narração.
- **Detecção Inteligente de Capítulos**: Cada capítulo vira uma faixa de áudio separada com tags ID3 (título, livro, autor, número de faixa), garantindo compatibilidade imediata com tocadores de smartwatch (Garmin, Apple Watch, etc.) e celulares.
- **Controle de Ritmo (Velocidade)**: Ajuste a velocidade de 0.8x a 1.8x (ótimo para manter um ritmo acelerado nos treinos).
- **Download Flexível**: Baixe capítulos individuais em `.mp3` ou um pacote `.zip` com todas as faixas nomeadas na sequência certa.

---

## 🚀 Como Executar

### 1. Criar ambiente virtual e instalar dependências

```bash
# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 2. Iniciar a aplicação local

```bash
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 📱 Dica para Corredores

1. Abra o app no computador e converta o seu livro favorito.
2. Baixe o arquivo `.zip` ou os arquivos `.mp3`.
3. Conecte seu celular ou relógio (Garmin Express / Apple Watch) e copie a pasta para a memória do dispositivo.
4. Conecte o fone Bluetooth e boas passadas!
