# Validação — 19/10/2026

Motor original preservado. Teste de execução em diretório temporário, sem rede ou APIs:

- CLI executada com duração de 20, 60 e 600 segundos e formatos 9:16, 1:1 e 16:9.
- Resoluções 1080x1920, 1080x1080 e 1920x1080 confirmadas.
- Plano JSON e pacote Markdown gerados; cenas contíguas entre zero e a duração solicitada.
- Histórico registra as quatro execuções válidas.
- Perfil informative_warm selecionado corretamente.
- Durações 19 e 601 e voz inexistente rejeitadas.
- Todos os JSONs recebidos passaram no parser.

Este teste verifica planejamento. Não houve geração de áudio, imagens de cenas ou vídeo final.
