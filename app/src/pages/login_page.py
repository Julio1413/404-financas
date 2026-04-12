import flet as ft
import re, datetime
from pages import ferramentas, home
print("Importando login_page...")

def login_sucesso(page):
    page.clean()
    page.controls.clear()
    page.update()
    home.inicial(page)

def login_page_2(page):


    def validacao(nome, telefone):
        def validar_nome(nome):
            nome = nome.strip()
            
            if len(nome) < 2:
                return False
            
            # Aceita letras (incluindo acentos) e espaços
            padrao = r'^[A-Za-zÀ-ÿ\s]+$'
            
            return bool(re.match(padrao, nome))
        pass

        def validar_telefone(telefone):
            # Remove tudo que não for número
            numeros = re.sub(r'\D', '', telefone)
            
            # Telefone brasileiro: 10 ou 11 dígitos
            if len(numeros) not in [10, 11]:
                return False
            
            return True
        
        if validar_nome(nome) and validar_telefone(telefone):
            ferramentas.criar_arquivo(nome="NOME.txt",conteudo=nome)
            ferramentas.criar_arquivo(nome="TELEFONE.txt",conteudo=telefone)
            login_sucesso(page)
            page.show_dialog(
                ft.SnackBar(
                    content=ft.Text("Login bem sucedido!"),
                    bgcolor=ft.Colors.GREEN,
                )
            )
        else:
            page.show_dialog(ft.SnackBar(
                content=ft.Text("Nome ou telefone inválido!"),
                bgcolor=ft.Colors.RED,
            ))
            page.update()

    
    page.add(
        ferramentas.color_header(page=page,
            controles=[
                ferramentas.header(titulo='Login',icone=ft.Icons.LOGIN,page=page,icone_btn=ft.Icons.CREDIT_CARD_ROUNDED,destino=None,desabilitar_btn=True),
                    ft.Placeholder(height=20,color=ft.Colors.TRANSPARENT),
                    ft.Text("404 Finanças", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Faça login para acessar sua conta local", size=16, color=ft.Colors.WHITE),
            ]
        )
    )


    page.add(ft.Placeholder(height=20,color=ft.Colors.TRANSPARENT))
    #Campos de entrada
    nome = ft.TextField(label="Nome", border_radius=40, focused_border_color=ft.Colors.PURPLE_300,expand=True,hint_text="Digite seu nome",keyboard_type=ft.KeyboardType.TEXT)
    telefone = ft.TextField(label="Telefone", border_radius=40, focused_border_color=ft.Colors.PURPLE_300,expand=True,hint_text="Digite seu telefone",keyboard_type=ft.KeyboardType.PHONE)

    # Adiciona os campos e o botão à página
    page.add(nome, telefone)

    page.add(ft.Placeholder(height=170,color=ft.Colors.TRANSPARENT))

    page.add(ft.ElevatedButton(
        on_click=lambda _:validacao(nome.value, telefone.value),
        content=ft.Text("Entrar"),
        width=page.width,
        height=50,
        
        bgcolor=ft.Colors.PURPLE_300,
        color=ft.Colors.WHITE,
    ))
    
    page.add(
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text("Desenvolvido por 404 Studios",size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE_60)
                ]
            )
        )

    page.update()
    


