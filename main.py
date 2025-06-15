import flet as ft
from logic.formateador import formatear_sql
from logic.interpretador import interpretar_sql
from logic.generador_inserts import procesar_excel


def main(page: ft.Page):
    page.title = "Asistente SQL By Julian Restrepo"
    page.window_icon = "assets/logo.png"  # usa png para más compatibilidad    page.window_width = 1100
    page.window_height = 720
    page.window_resizable = False
    page.padding = 20

    entrada_sql = ft.TextField(label="Escribe tu consulta SQL", multiline=True, min_lines=8, max_lines=8)
    salida_formateado = ft.TextField(label="Consulta Formateada", multiline=True, read_only=True, min_lines=12, max_lines=12)
    salida_interpretado = ft.TextField(label="Interpretación de la Consulta", multiline=True, read_only=True, min_lines=12, max_lines=12)

    salida_insert = ft.TextField(label="Comandos INSERT generados", multiline=True, min_lines=10, expand=True, max_lines=30)
    nombre_tabla_input = ft.TextField(label="Nombre de la tabla para INSERT", width=300)

    tabla_container = ft.Container(visible=False)
    snackbar = ft.SnackBar(content=ft.Text(""))
    page.snack_bar = snackbar

    filas_actuales = []
    columnas_actuales = []
    pagina_actual = 0
    filas_por_pagina = 10

    def mostrar_pagina(pagina: int):
        nonlocal filas_actuales, columnas_actuales, pagina_actual
        pagina_actual = pagina
        inicio = pagina * filas_por_pagina
        fin = inicio + filas_por_pagina
        filas_pagina = filas_actuales[inicio:fin]

        tabla_excel = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in columnas_actuales],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell or ""))) for cell in fila]) for fila in filas_pagina],
            width=1000,
            # Sin colores para fondo ni filas ni encabezados
        )

        tabla_container.content = ft.Column([
            ft.Container(
                ft.ListView(expand=True, controls=[tabla_excel]),
                height=300,
                expand=True,
                # Quitamos bgcolor para que no pinte fondo blanco
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
            ),
            ft.Row([
                ft.ElevatedButton("Anterior", on_click=lambda _: navegar_pagina(pagina_actual - 1), disabled=(pagina_actual == 0)),
                ft.Text(f"Página {pagina_actual + 1} de {((len(filas_actuales) - 1) // filas_por_pagina) + 1}"),
                ft.ElevatedButton("Siguiente", on_click=lambda _: navegar_pagina(pagina_actual + 1), disabled=(fin >= len(filas_actuales))),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])
        tabla_container.visible = True
        page.update()

    def navegar_pagina(nueva_pagina: int):
        if 0 <= nueva_pagina <= (len(filas_actuales) - 1) // filas_por_pagina:
            mostrar_pagina(nueva_pagina)

    def formatear(e):
        salida_formateado.value = formatear_sql(entrada_sql.value) if entrada_sql.value.strip() else ""
        page.update()

    def interpretar(e):
        salida_interpretado.value = interpretar_sql(entrada_sql.value) if entrada_sql.value.strip() else ""
        page.update()

    def copiar_sql(e):
        texto = salida_formateado.value.strip()
        if texto:
            page.set_clipboard(texto)
            snackbar.content.value = "Consulta copiada al portapapeles ✅"
        else:
            snackbar.content.value = "No hay consulta para copiar ⚠️"
        snackbar.open = True
        page.update()

    def guardar_archivo(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                with open(e.path, "w", encoding="utf-8") as f:
                    f.write(salida_formateado.value)
                snackbar.content.value = f"Archivo guardado en: {e.path}"
            except Exception as ex:
                snackbar.content.value = f"Error al guardar: {ex}"
            snackbar.open = True
            page.update()

    def exportar_txt(e):
        if not salida_formateado.value.strip():
            snackbar.content.value = "No hay consulta formateada para exportar."
            snackbar.open = True
            page.update()
            return
        file_picker.save_file(dialog_title="Guardar como", file_name="consulta_formateada.txt")

    def copiar_inserts(e):
        texto = salida_insert.value.strip()
        if texto:
            page.set_clipboard(texto)
            snackbar.content.value = "INSERTs copiados al portapapeles ✅"
        else:
            snackbar.content.value = "No hay contenido INSERT para copiar ⚠️"
        snackbar.open = True
        page.update()

    def guardar_inserts(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                with open(e.path, "w", encoding="utf-8") as f:
                    f.write(salida_insert.value)
                snackbar.content.value = f"Archivo INSERT guardado en: {e.path}"
            except Exception as ex:
                snackbar.content.value = f"Error al guardar INSERT: {ex}"
            snackbar.open = True
            page.update()

    def subir_archivo(e: ft.FilePickerResultEvent):
        nonlocal filas_actuales, columnas_actuales, pagina_actual
        if e.files:
            if not nombre_tabla_input.value.strip():
                snackbar.content.value = "Debes ingresar el nombre de la tabla para los INSERT."
                snackbar.open = True
                page.update()
                return
            try:
                columnas, filas, insert_sql = procesar_excel(e.files[0].path, nombre_tabla_input.value.strip())
                columnas_actuales = columnas
                filas_actuales = filas
                pagina_actual = 0
                salida_insert.value = insert_sql
                mostrar_pagina(0)
            except Exception as ex:
                snackbar.content.value = f"Error procesando archivo: {ex}"
                snackbar.open = True
                salida_insert.value = ""
                tabla_container.visible = False
                page.update()

    def limpiar_editor_sql(e):
        entrada_sql.value = ""
        salida_formateado.value = ""
        salida_interpretado.value = ""
        page.update()

    def limpiar_inserts(e):
        salida_insert.value = ""
        nombre_tabla_input.value = ""
        tabla_container.visible = False
        page.update()

    file_picker = ft.FilePicker(on_result=guardar_archivo)
    file_picker_excel = ft.FilePicker(on_result=subir_archivo)
    file_picker_insert = ft.FilePicker(on_result=guardar_inserts)
    page.overlay.extend([file_picker, file_picker_excel, file_picker_insert])

    def estilo_boton(color_hex):
        return dict(bgcolor=color_hex, color=ft.Colors.WHITE)

    acciones_superiores = ft.Row([
        ft.ElevatedButton("Formatear SQL", icon=ft.Icons.FORMAT_ALIGN_LEFT, on_click=formatear, **estilo_boton("#0074E4")),
        ft.ElevatedButton("Copiar SQL", icon=ft.Icons.CONTENT_COPY, on_click=copiar_sql, **estilo_boton("#2ECC71")),
        ft.ElevatedButton("Exportar a TXT", icon=ft.Icons.SAVE_ALT, on_click=exportar_txt, **estilo_boton("#E67E22")),
        ft.Container(
            ft.ElevatedButton("Interpretar SQL", icon=ft.Icons.INSIGHTS, on_click=interpretar, **estilo_boton("#9B59B6")),
            margin=ft.margin.only(left=280)
        ),
        ft.ElevatedButton("Limpiar todo", icon=ft.Icons.DELETE, on_click=limpiar_editor_sql, **estilo_boton("#E74C3C")),
    ], spacing=10)

    acciones_insert = ft.Row([
        ft.ElevatedButton("Subir archivo Excel", icon=ft.Icons.UPLOAD_FILE, on_click=lambda _: file_picker_excel.pick_files(), **estilo_boton("#3498DB")),
        ft.ElevatedButton("Guardar INSERTs", icon=ft.Icons.SAVE_ALT, on_click=lambda _: file_picker_insert.save_file(file_name="insert_generados.sql"), **estilo_boton("#27AE60")),
        ft.ElevatedButton("Copiar INSERTs", icon=ft.Icons.CONTENT_COPY, on_click=copiar_inserts, **estilo_boton("#F39C12")),
        ft.ElevatedButton("Limpiar todo", icon=ft.Icons.DELETE, on_click=limpiar_inserts, **estilo_boton("#E74C3C")),
    ], spacing=10)

    tab_editor_sql = ft.Tab(
        text="Formateador SQL",
        icon=ft.Icons.CODE,
        content=ft.Column([
            entrada_sql,
            acciones_superiores,
            ft.Row([
                ft.Container(salida_formateado, expand=True),
                ft.Container(salida_interpretado, expand=True)
            ], spacing=20)
        ], spacing=6, tight=True)
    )

    tab_excel = ft.Tab(
        text="Generador INSERT",
        icon=ft.Icons.INSERT_DRIVE_FILE,
        content=ft.Column([
            nombre_tabla_input,
            acciones_insert,
            ft.Row([
                ft.Container(tabla_container, expand=True, height=360, padding=5),
                ft.Container(
                    ft.ListView(expand=True, controls=[salida_insert]),
                    expand=True, height=360, padding=5,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                )
            ], spacing=10)
        ], spacing=10)
    )

    tabs = ft.Tabs(tabs=[tab_editor_sql, tab_excel], animation_duration=300)

    page.add(tabs)


if __name__ == "__main__":
    ft.app(target=main)
