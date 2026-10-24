# 04 - Armazenamento e Segurança

## Diretório de Saída e Mídias
- **Diretório Raiz de Áudio**: `./output/` [app.py], [.gitignore].
- **Estrutura por Livro**: `output/audiobooks/<nome_higienizado_do_livro>/` [app.py].
- **Arquivos Temporários**: Prévia de áudio salva em `output/preview_sample.mp3` [app.py].
- **Pacotes Gerados**: Pacotes comprimidos salvos em `output/<nome_do_livro>_audiobook.zip` [app.py].

## Regras de Governança de Arquivos
- SEMPRE sanitizar nomes de arquivos removendo caracteres especiais de SO (`\/:*?"<>|`) antes de criar pastas ou arquivos [app.py].
- NUNCA versionar ou commitar arquivos dentro de `output/`, `.mp3`, `.m4b` ou `.zip` [.gitignore].
- SEMPRE respeitar o `.gitignore` mantendo binários e mídias geradas fora do controle de versão [.gitignore].

## Segurança e Gestão de Segredos
- NUNCA commitar arquivos `.env`, tokens, chaves privadas ou certificados no repositório [DIRETRIZ].
- NUNCA logar trechos confidenciais de arquivos dos usuários em logs públicos [DIRETRIZ].
- Se futuras integrações exigirem tokens (ex.: OpenAI, ElevenLabs), SEMPRE carregar via variáveis de ambiente (`os.environ`) ou `st.secrets` do Streamlit, documentando em `.env.example` sem valores reais [DIRETRIZ].
