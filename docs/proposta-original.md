# Motor de Vídeos Narrativos Variáveis

Este diretório contém o motor de direção audiovisual aprendido a partir do Reel fornecido pelo usuário. Ele transforma um assunto em um **plano de vídeo original**, com estrutura narrativa, mapa de batidas, direção de voz, trilha, efeitos, movimentos de câmera e regras de montagem.

O motor aprende o que torna a referência eficiente — narração como espinha dorsal, imagens estáticas com movimento de camadas, texto sincronizado, trilha em curva e CTA depois da entrega de valor — sem clonar a marca, o texto, a voz ou as imagens da peça original.

## Arquivos

- `reference_analysis.md`: DNA audiovisual observado e regras incorporadas.
- `engine_config.json`: catálogo de arquétipos, gramáticas visuais, câmeras, transições, vozes, trilhas, SFX e regras anti-repetição.
- `motor_video.py`: CLI que cria um plano de produção e um pacote de prompts.
- `history.json`: memória das últimas combinações usadas para evitar vídeos parecidos.
- `reference/`: cópia técnica de trabalho, transcrição e quadros extraídos da referência.
- `jobs/`: planos gerados para assuntos futuros.

## Uso rápido

```bash
cd /home/ubuntu/video_engine
python3 motor_video.py \
  --tema "Como uma invenção mudou a vida nas cidades" \
  --duracao 60 \
  --formato 9:16 \
  --objetivo "educar e gerar curiosidade" \
  --cta "Comente o que você descobriu"
```

O comando cria duas saídas em `jobs/<id>/`:

- `plano.json`: manifesto estruturado para produção e montagem;
- `prompt_pack.md`: briefing legível com shots, direção da narração, trilha e checklist.

Para repetir exatamente uma combinação, use `--seed`. Para escolher uma voz específica, use um dos perfis do arquivo de configuração, por exemplo `--voz informative_warm`.

## Como a variação funciona

A cada novo assunto, o motor escolhe uma combinação controlada de:

- arquétipo narrativo: origem-crise-legado, mito-revelação, problema-mecanismo-solução, cronologia reversa, jornada por lugares ou objeto-testemunha;
- gramática visual: pintura em camadas, mapa, documento, objetos em mesa, tipografia cinética, B-roll ou colagem;
- movimentos de câmera: push-in, pull-back, pan, orbit, dolly, rack focus, parallax, top-down, hold e outros;
- transições: corte factual, dissolve, wipe de mapa, revelação de tinta, escurecimento, match cut e lift de luz;
- voz: perfis graves, informativos, amistosos, firmes ou femininos, conforme o assunto;
- trilha: épica histórica, pulso documental, memória humana, curiosa minimalista ou produto premium;
- arco de cor e estilo de CTA.

A memória em `history.json` bloqueia repetições recentes. A aleatoriedade é determinística por seed e sempre subordinada ao sentido do assunto.

## Fluxo quando o usuário enviar um assunto

1. Definir a tese em uma frase e o público.
2. Escolher uma estrutura que não repita os últimos vídeos.
3. Escrever um roteiro original em português brasileiro.
4. Gerar a narração com instruções de voz separadas do texto falado.
5. Medir o áudio real antes de fixar a duração de cada imagem.
6. Criar o beat map e as imagens ou clips necessários.
7. Gerar uma trilha instrumental e SFX pontuais.
8. Montar com FFmpeg ou gerador de vídeo, sincronizar texto e legendas.
9. Verificar dimensão, duração, codecs, volume, legibilidade e ritmo.
10. Entregar o vídeo final e, quando útil, o plano reutilizável.

## Direção de voz

A direção de performance deve ser escrita em inglês para orientar o sintetizador, enquanto o roteiro falado permanece em pt-BR. A forma é:

```text
English performance direction: texto falado em português brasileiro.
```

O motor não força uma duração artificial. O áudio gerado é medido e os visuais são ajustados a ele. Pausas curtas depois de datas, números e viradas são preferidas a uma leitura acelerada.

## Regras de qualidade

- A voz fica na frente da música.
- A música é instrumental e tem espaço para a fala.
- Efeitos sonoros apoiam eventos visíveis; não são usados como decoração constante.
- Imagem estática pode ter movimento, mas movimento não substitui informação.
- Um mesmo preset de câmera não deve aparecer em todos os shots.
- O texto na tela destaca uma ideia, não duplica um parágrafo inteiro.
- O CTA tem tempo de leitura e não aparece antes da entrega da promessa narrativa.
- Pessoas, produtos, logos, documentos e marcas exigem referências aprovadas quando a fidelidade visual for importante.

## Próximo passo

Basta enviar o assunto, por exemplo: **“a história do café no Brasil, para um vídeo de 60 segundos”**. O motor será usado para construir o roteiro, a direção audiovisual, a narração, a trilha, os movimentos variados e a montagem final.
