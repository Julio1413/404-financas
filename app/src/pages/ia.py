import flet as ft
from pages import home, ferramentas
import google.generativeai as genai

def ia(page):
    page.clean()
    page.add(
        ferramentas.color_header(
            page=page,
            altura=63,
            controles=[
                ferramentas.header(titulo='Recursos de IA',icone=ft.Icons.ADB_ROUNDED,page=page)
            ]
        )
    )
    page.update()