# Motor de Vídeos Narrativos

**[Português](README.md) · [English](README.en.md) · [Español](README.es.md)**

[![Motor de Vídeos Narrativos](guia/assets/banner-es.jpg)](https://inematds.github.io/motor-videos-narrativos/guia/es/)

## Qué es

Una herramienta en Python para quienes planifican vídeos educativos y narrativos. A partir de un tema, organiza las escenas, los tiempos previstos y las indicaciones de imagen, voz y música en dos archivos. El historial local ayuda a variar las elecciones entre proyectos. Basta con tener Python 3.9 o superior: la creación del plan funciona sin conexión y sin clave de API. El guion final, el audio y el vídeo se producen después, con otras herramientas.

## Guía de uso

[Abre la guía completa](https://inematds.github.io/motor-videos-narrativos/guia/es/).

```bash
git clone https://github.com/inematds/motor-videos-narrativos.git
cd motor-videos-narrativos
python3 motor_video.py --tema "Como o café chegou ao Brasil" --duracao 60 --formato 9:16
```

Resultados: `jobs/<id>/plano.json` y `jobs/<id>/prompt_pack.md`. El historial local `history.json` se crea automáticamente y no se incluye en el control de versiones. Los ejemplos recibidos están en `exemplos/`, incluido el historial original. La interfaz del motor, los textos generados y los documentos originales están en portugués.

- Python 3.9+, solo biblioteca estándar; sin APIs ni paquetes externos.
- `--help`: enumera todas las opciones; duración entre 20 y 600 segundos.
- `--voz informative_warm`: selecciona un perfil del catálogo; no sintetiza audio.
- `--seed`: repite las elecciones solo con los mismos argumentos, configuración e historial de entrada; los metadatos de fecha varían.
- `--out`: elige una carpeta nueva para evitar sobrescribir resultados anteriores.
- Las elecciones son sorteos con restricciones del historial; no hay análisis semántico del tema.
- El motor genera indicaciones y espacios para el guion. No investiga hechos, no escribe el guion final y no renderiza MP4.

## Materiales

- [ADN audiovisual](reference_analysis.md): análisis proporcionado, con mediciones comunicadas de la referencia.
- [Propuesta original](docs/proposta-original.md): visión completa del flujo; incluye etapas aún externas al código.
- [Café](exemplos/demo_cafe/prompt_pack.md) y [ríos](exemplos/demo_rios/prompt_pack.md): ejemplos recibidos en portugués.
- `engine_config.json`: estructuras narrativas, lenguajes visuales, voces, música y reglas de producción.

El ZIP recibido contiene el mismo motor y la misma configuración que los archivos sueltos; sus ejemplos se incorporaron sin modificar el código. El vídeo de referencia y la transcripción no venían en el paquete. Las referencias a esos archivos en los documentos originales se conservan como contexto.
