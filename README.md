# Proyecto de Aplicación Web de Chat

Este proyecto es una aplicación web de chat que permite a los usuarios interactuar en canales específicos, enviar mensajes y mantener un historial de hasta 100 mensajes por canal. La aplicación cumple con los requisitos establecidos y proporciona funcionalidades adicionales para mejorar la experiencia de los usuarios.

## Archivos Incluidos

- **app.py**: Contiene la lógica principal de la aplicación, incluyendo el manejo de solicitudes, el almacenamiento de mensajes y la gestión de canales.
- **templates/**: Carpeta que contiene los archivos HTML para las diferentes páginas y elementos de la interfaz de usuario.
- **static/**: Carpeta que contiene archivos estáticos como CSS, imágenes o scripts JS para el diseño y la funcionalidad adicional.
- **requirements.txt**: Archivo que enumera los paquetes de Python necesarios para ejecutar la aplicación web.

## Funcionalidades Principales

### 1. Nombre Visual y Recordatorio de Canal
- Al ingresar por primera vez, se solicita al usuario un nombre que se asocia a sus mensajes y se recuerda para visitas futuras.
- La aplicación recuerda el canal en el que el usuario estaba anteriormente, llevándolo de vuelta a ese canal al regresar.

### 2. Creación y Visualización de Canales
- Los usuarios pueden crear nuevos canales, siempre que el nombre no esté en conflicto con canales existentes.
- Se muestra una lista de todos los canales disponibles para que los usuarios puedan seleccionar y acceder a ellos.

### 3. Vista de Mensajes y Envío de Mensajes
- Al seleccionar un canal, se muestra un historial de hasta 100 mensajes previos en ese canal.
- Los usuarios pueden enviar mensajes de texto a otros en el canal sin necesidad de recargar la página.

## Funcionalidad Adicional - Mensajes Privados
Una característica adicional que se agregó a la aplicación es la capacidad de enviar mensajes privados entre dos usuarios. Esta función permite una comunicación más personalizada y directa entre los participantes del chat.
