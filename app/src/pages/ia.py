import flet as ft
from google.genai import Client
from pages import home, ferramentas


def get_client():
    if ferramentas.arquivo_existe('GOOGLE_API_KEY.txt'):
        api_key = ferramentas.ler_arquivo('GOOGLE_API_KEY.txt').strip()
        if api_key:
            return Client(api_key=api_key)
    return None


def gerar_texto(texto):
    client = get_client()
    if not client:
        return "Erro: Chave de API não configurada."
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview',
            contents=texto
        )
        return response.text
    except Exception as e:
        return str(e)

#print(gerar_texto())

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
    if get_client() is None:
        snack = ft.SnackBar(ft.Text('Chave de API não encontrada! Adicione uma nas configurações!'), bgcolor=ft.Colors.RED)
        page.show_dialog(snack)
        page.update()
        return

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=5,
                    gradient=ft.LinearGradient(
                            begin=ft.Alignment.TOP_CENTER,
                            end=ft.Alignment.BOTTOM_CENTER,
                            colors=[ft.Colors.INDIGO_300, ft.Colors.INDIGO_900]
                        ),
                    border_radius=30,
                    width=page.width*0.97,
                    height=200,
                    content=(
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        ft.Container(padding=5,border=ft.border.all(1, ft.Colors.INDIGO_900),
                                            border_radius=20,bgcolor=ft.Colors.INDIGO,width=page.width*0.44,height=83,
                                            content=ft.Row(controls=[ft.Text('OI')])
                                        ),                                    
                                        ft.Container(padding=5,border=ft.border.all(1, ft.Colors.INDIGO_900),
                                            border_radius=20,bgcolor=ft.Colors.INDIGO,width=page.width*0.44,height=83,
                                            content=ft.Row(controls=[ft.Text('OI')])
                                        ),
                                ]),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        ft.Container(padding=5,border=ft.border.all(1, ft.Colors.INDIGO_900),
                                            border_radius=20,bgcolor=ft.Colors.INDIGO,width=page.width*0.44,height=83,
                                            content=ft.Row(controls=[ft.Text('OI')])
                                        ),                                    
                                        ft.Container(padding=5,border=ft.border.all(1, ft.Colors.INDIGO_900),
                                            border_radius=20,bgcolor=ft.Colors.INDIGO,width=page.width*0.44,height=83,
                                            content=ft.Row(controls=[ft.Text('OI')])
                                        ),
                                ]),
                            ]
                        )
                    )
                )
            ]
        )
    )


    page.update()