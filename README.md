# 🧠 Asistente-SQL-Inteligente

Asistente SQL en **Python + Flet** que interpreta consultas SQL convirtiéndolas en **lenguaje natural comprensible** y genera comandos `INSERT` desde archivos **Excel**, con detección automática de tipos. Ideal para **científicos de datos**, analistas y usuarios no técnicos.

Link de la exposición del proyecto: https://youtu.be/3iTRXQrMoCw?si=KX0uDDNXe-rnpcmG

---

## 🚀 Funcionalidades principales

- 🗣 Interpreta sentencias SQL y las transforma en descripciones en lenguaje natural.
- 📄 Genera sentencias `INSERT INTO` desde archivos Excel.
- 🧠 Detección automática de tipos de datos por columna.
- 🖥 Interfaz gráfica amigable desarrollada con Flet.
- 🔒 100% local, sin conexión a APIs externas.

---

## 🛠 Tecnologías utilizadas

- Python 3.10+
- [Flet](https://flet.dev/)
- openpyxl
- SQLParse
- Tipado personalizado

---

## 📸 Captura (Formatear e interpretar consulta SQL)

> *![image](https://github.com/user-attachments/assets/b5ae1ff9-3394-4f11-93b7-5e5295fc0c47))*

## 📸 Captura (Generador de insert SQL con datos excel)
> *![image](https://github.com/user-attachments/assets/252faf50-5b44-406f-b8d9-8bbb614cf743)
*

---

## ▶️ Cómo ejecutar y utilizar la aplicación

La interfaz gráfica ha sido diseñada para ser intuitiva y fácil de usar, adaptándose a las necesidades tanto de usuarios técnicos como no técnicos.

Al iniciar la aplicación, verás dos opciones principales en la parte superior de la pantalla:

### 1. 🛠 **Formateador SQL**

Esta sección permite pegar una consulta SQL desordenada o difícil de leer, y realizar varias acciones:

- 🧾 **Caja de entrada**: ingresa aquí tu consulta SQL.
- 🔘 **Botones disponibles**:
  - `Formatear SQL`: mejora la estructura y legibilidad de la consulta.
  - `Interpretar SQL`: muestra una explicación en lenguaje natural de la consulta.
  - `Copiar SQL`: copia el resultado formateado al portapapeles.
  - `Exportar a .txt`: guarda el SQL formateado en un archivo de texto.
  - `Limpiar todo`: borra todos los campos.

- 📄 **Resultados**:
  - Una caja de texto mostrará el SQL ya formateado.
  - Otra caja mostrará la interpretación en lenguaje natural.

---

### 2. 📥 **Generador de INSERT**

Esta sección te permite cargar un archivo Excel y generar automáticamente los comandos `INSERT INTO` para una tabla:

- 🧾 **Campo "Nombre de tabla"**: escribe el nombre de la tabla destino del `INSERT`.
- 🔘 **Botones disponibles**:
  - `Subir archivo`: selecciona el archivo Excel a procesar.
  - `Guardar INSERT`: guarda el script generado en un archivo.
  - `Copiar INSERT`: copia el código generado al portapapeles.
  - `Limpiar todo`: limpia campos y resultados.

- 📋 **Resultados**:
  - Vista previa de la tabla cargada (campos y registros).
  - Caja de texto con el script `INSERT` completo generado automáticamente.

---

Esta estructura te permite cubrir de forma eficiente los dos flujos principales del sistema, facilitando el trabajo con SQL para cualquier perfil de usuario.

