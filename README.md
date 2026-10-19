# Motor de Vídeos Narrativos

**[Português](README.md) · [English](README.en.md) · [Español](README.es.md)**

[![Motor de Vídeos Narrativos](guia/assets/banner.jpg)](https://inematds.github.io/motor-videos-narrativos/guia/)

## O que é

Uma ferramenta em Python para quem planeja vídeos educativos e narrativos. A partir de um assunto, organiza as cenas, os tempos previstos e as orientações de imagem, voz e música em dois arquivos. O histórico local ajuda a variar as escolhas entre trabalhos. Basta ter Python 3.9 ou superior: a criação do plano funciona offline, sem chave de API. O roteiro final, o áudio e o vídeo são produzidos depois, com outras ferramentas.

## Guia de uso

[Abra o guia completo](https://inematds.github.io/motor-videos-narrativos/guia/).

```bash
git clone https://github.com/inematds/motor-videos-narrativos.git
cd motor-videos-narrativos
python3 motor_video.py --tema "Como o café chegou ao Brasil" --duracao 60 --formato 9:16
```

Saídas: `jobs/<id>/plano.json` e `jobs/<id>/prompt_pack.md`. O histórico local `history.json` é criado automaticamente e não é versionado. Os exemplos recebidos estão em `exemplos/`, incluindo o histórico original.

- Python 3.9+, somente biblioteca padrão; sem APIs ou pacotes externos.
- `--help`: lista todas as opções; duração entre 20 e 600 segundos.
- `--voz informative_warm`: seleciona um perfil do catálogo; não sintetiza áudio.
- `--seed`: repete escolhas apenas com os mesmos argumentos, configuração e histórico de entrada; metadados de data variam.
- `--out`: escolha uma pasta nova para evitar sobrescrever saídas anteriores.
- As escolhas são sorteios com restrições de histórico; não há análise semântica do tema.
- O motor gera orientações e espaços para roteiro. Não pesquisa fatos, não escreve o roteiro final e não renderiza MP4.

## Materiais

- [DNA audiovisual](reference_analysis.md): análise fornecida, com medições relatadas da referência.
- [Proposta original](docs/proposta-original.md): visão completa do fluxo; inclui etapas ainda externas ao código.
- [Café](exemplos/demo_cafe/prompt_pack.md) e [rios](exemplos/demo_rios/prompt_pack.md): exemplos recebidos em português.
- `engine_config.json`: estruturas narrativas, linguagens visuais, vozes, música e regras de produção.

O ZIP recebido contém o mesmo motor e configuração dos arquivos avulsos; seus exemplos foram incorporados sem alterar o código. O vídeo de referência e a transcrição não vieram no pacote. As referências a esses arquivos nos documentos originais são preservadas como contexto.
