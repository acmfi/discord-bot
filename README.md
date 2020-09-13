Discord bot developed during summer 2020 as a summer project :D

## Introducción
Este bot esta desarrollado con la intención de automatizar y facilitar la gestión del servidor de discord de ACM-UPM creado durante el verano de 2020.

## :heart: Colaboradores :heart:
[@onmax](https://github.com/onmax)
[@Santixs](https://github.com/Santixs)
[@Thurmiel](https://github.com/Thurmiel)
[@Daniel-Tomas](https://github.com/Daniel-Tomas)
[@Formil](https://github.com/Formil)
[@jonsalchichonnn](https://github.com/jonsalchichonnn)
[@xiaopeng-ye](https://github.com/xiaopeng-ye)
[@JustAntoRS](https://github.com/JustAntoRS)
[@juan-vmarin](https://github.com/juan-vmarin)

## Como colaborar
(Debes ser miembro del equipo discord-bot en la org acmfi)
1. Clonar el repositorio en tu ordenador
2. Crear un issue para el cambio que vas a hacer,asignar la issue al project **Development**, en la issue debes explicar que vas a cambiar y porque.
3. En el project **Development** mover la issue de **To Do** a la columna **In Progress**
3. Crear una branch en tu copia local del repositorio, como nombra de la branch puedes usar el identificador de la issue (#numero) 
4. Subir tu código al repositorio y cuando hayas acabado de trabajar en el, ir al project **Development** y mover la issue de la columna **In Progress** a **To Review**
5. Crear una pull request de la branch que implementa la issue a master. 
6. Como mínimo 1 persona debe revisar el código y aprobar la pull request para que se pueda realizar el merge a master.

## Como instalar e iniciar el proyecto
Una vez hayas clonado el repositorio y suponiendo que cuentas con Python instalado en tu ordenador (puedes descargar la última versión desde [aquí](https://www.python.org/)) debes seguir los siguientes pasos:

1. Instalar las dependencias del proyecto usando **pipenv**
```
pipenv install
```
2. Obtener un token para el bot, lo puedes conseguir [aquí](https://discordapp.com/developers/applications/) y escribir ese token en el fichero token.txt dentro de la carpeta src/
3. IMPORTANTE: NO SUBIR EL TOKEN AL REPOSITORIO, EL FICHERO ESTA INCLUIDO EN EL .gitignore
4. Iniciar el proyecto 
```
pipenv run python3 src/bot.py
```

## Configuración del bot
Crear y modificar el fichero src/bot_conf.json con la siguiente forma, consulte la siguiente [página](https://support.discord.com/hc/es/articles/206346498--D%C3%B3nde-puedo-encontrar-mi-ID-de-usuario-servidor-mensaje-) para encontrar el ID de tu canal.

```json
{
    "token": "token del bot de discord",
    "channels_id": [
        "Primer ID (id de los canales que desean recibir avisos enviados por el canal de telegram)",
        "Segundo ID"
    ],
    "api_users": [
        {
            "user": "nombre de usuario 1 (array de todo los usuarios que puedan usar el API)",
            "password": "contraseña"
        },
        {
            "user": "nombre de usuario 2",
            "password": "contraseña 2"
        }
    ]
}
```




