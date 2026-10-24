# 03 - Testes e Garantia de Qualidade

## Framework e Estrutura de Testes
- **Framework**: `pytest` [DIRETRIZ aprovada pelo usuário].
- **Formatter**: `black` [DIRETRIZ aprovada pelo usuário].
- **CI / Automação**: GitHub Actions (`.github/workflows/ci.yml`) [DIRETRIZ].
- **Diretório de Testes**: `tests/` na raiz do projeto [DIRETRIZ].
- **Nomenclatura**: Arquivos `test_<modulo>.py` e funções de teste `test_<comportamento>()` [DIRETRIZ].

## Regras de Mocks e Isolamento
- **Testes Unitários de Extração**:
  - SEMPRE usar buffers em memória (`io.BytesIO`) ou fixtures sintéticas em `tests/fixtures/` para testar `PDFExtractor` e `EPUBExtractor` [DIRETRIZ].
- **Testes Unitários de TTS**:
  - SEMPRE mockar chamadas de rede do `edge_tts.Communicate.save` para não depender de conexão nem gastar banda em testes automatizados [DIRETRIZ].
  - NUNCA disparar requisições reais para servidores externos durante a execução de testes unitários [DIRETRIZ].
- **Testes de Áudio**:
  - Usar arquivos temporários gerenciados por fixtures `tmp_path` do pytest para validar `AudioManager.tag_mp3` e `create_zip_package` [DIRETRIZ].

## Checklist Obrigatório para Agentes de IA
Antes de considerar qualquer tarefa ou refatoração concluída, o agente DEVE cumprir:
1. **Validação de Sintaxe e Estilo**: Garantir sintaxe válida e formatação com `black --check .` [DIRETRIZ].
2. **Execução de Testes**: Rodar a suíte com `pytest` e garantir que todos os testes passem [DIRETRIZ].
3. **Escopo Restrito**: NUNCA alterar arquivos fora do escopo solicitado pelo usuário [DIRETRIZ].
4. **Dependências**: NUNCA adicionar dependências ao `requirements.txt` sem aprovação prévia do usuário [DIRETRIZ].
5. **Preservação de Regras**: NUNCA remover docstrings, comentários explicativos ou regras em `.gemini/rules/` [DIRETRIZ].
