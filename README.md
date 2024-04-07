
# Chamuyo-Bot

## Descripción

**Chamuyo-Bot** es un bot de Telegram diseñado para generar una carcajada, o si se lo toman en serio hasta motiviación, a tu desanimado e inerte equipo de desarrollo de software. Cada mañana, este bot envía mensajes "motivacionales" a los miembros de tu equipo. Ideal para equipos de virgos nerds que no suben PR en semanas y el último feature sin errores fue el cambio de la precisión decimal en una columna tipo INT.

Este proyecto utiliza la API de OpenAI para generar los mensajes, para que ningún ser humano tenga que esforzarse.

Enlace al bot: [chamuyo-bot](https://t.me/chamuyo_bot)

## Características

- Envío automático de mensajes cada mañana.
- Mensajes generados mediante inteligencia artificial para ofrecer variedad y relevancia.
- Fácil configuración y personalización para adaptarse a las necesidades de tu equipo.

## Requisitos

Antes de comenzar, asegúrate de tener instalado Python y pip. Este proyecto requiere las siguientes librerías:

- openai
- requests
- aiohttp
- boto3

Puedes instalar todas las dependencias necesarias con el siguiente comando:

```bash
pip install openai requests aiohttp boto3
```

## Configuración

Para que **Chamuyo-Bot** funcione correctamente, necesitas configurar las siguientes variables de entorno con tus claves de API de OpenAI y el token de tu bot de Telegram:

```bash
export OPENAI_API_KEY='tu_clave_api_openai'
export TELEGRAM_TOKEN='tu_token_telegram'
```

Asegúrate de reemplazar `tu_clave_api_openai` y `tu_token_telegram` con tus respectivas claves.

## Uso

Una vez configurado, puedes iniciar el bot ejecutando el script principal. Este se encargará de enviar automáticamente los mensajes inspiracionales a los miembros del equipo cada mañana.

## Contribuir

Si estás interesado en contribuir al proyecto, tus aportes son bienvenidos. Puedes abrir un issue para discutir lo que te gustaría cambiar o directamente enviar un pull request con tus mejoras.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
