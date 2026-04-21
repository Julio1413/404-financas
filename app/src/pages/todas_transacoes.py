from flet.controls import border
import flet as ft
from pages import home,ferramentas
import json as js

def todas_transacoes(page,tipo='',descricao='',periodo=''):
    #Limpando a página
    page.clean()
    page.floating_action_button = None

    #Funções essenciais


    def listar_tipos():
        if ferramentas.arquivo_existe("tipoS.txt"):
            tipos = ferramentas.ler_arquivo("tipoS.txt").splitlines()
        else:
            tipos = []
        return tipos

    #Listando todas as transações
    if ferramentas.arquivo_existe("TRANSAÇÕES.json"):
        transacoes = js.loads(ferramentas.ler_arquivo("TRANSAÇÕES.json"))
    else:
        transacoes = []
    
    lista_separada = []
    for t in transacoes:
        if (tipo == '' or tipo == 'Todas' or t['tipo'] == tipo) and (descricao.lower() == '' or descricao.lower() in t['descricao'].lower()) and (periodo == '' or periodo == 'Todos' or t['periodo'] == periodo):
            lista_separada.append(t)
    

    #Para o container
    transacoes_filtradas = []
    for t in reversed(lista_separada):
        transacoes_filtradas.append(
            ft.Column(
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(t["descricao"],weight=ft.FontWeight.BOLD),
                                    ft.Text(t["data"],size=10)
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(t["tipo"],size=12),
                                    ft.Text(f'R$ {t["valor"]:.2f}'.replace(".", ","),weight=ft.FontWeight.BOLD,color=ft.Colors.GREEN_700 if t["tipo"] == "Receita" else ft.Colors.RED)
                                ]
                            )
                        ]
                    )
            )
        transacoes_filtradas.append(ft.Divider())   
            
            
    
    #Listando perídos
    periodos=[]
    for t in transacoes:
        if t["periodo"] not in periodos:
            periodos.append(t["periodo"])
            
    #Construção da página
    page.add(
        ferramentas.color_header(
            page=page,
            altura=63,
            controles=[
                ferramentas.header(titulo='Todas as transações',icone=ft.Icons.MONEY_ROUNDED,page=page)
            ]
        )
    )


    page.add(ft.Placeholder(height=1,color=ft.Colors.TRANSPARENT))

    dropdown_tipo = ft.Dropdown(
        label="tipo",
        width=130,
        border_color=ft.Colors.DEEP_PURPLE,
        border_radius=40,
        options=[ft.dropdown.Option("Todas")] + [ft.dropdown.Option(i) for i in listar_tipos()],
        value=tipo if (tipo and tipo != '') else "Todas",
    )
    
    search_bar = ft.TextField(
        border_radius=40,
        border_color=ft.Colors.DEEP_PURPLE,
        label="Descrição",
        width=130,
        focused_border_width=1,
        
    )

    dropdown_periodo = ft.Dropdown(
        label="Período",
        width=130,
        border_color=ft.Colors.DEEP_PURPLE,
        border_radius=40,
        options=[ft.dropdown.Option("Todos")] + [ft.dropdown.Option(i) for i in periodos],
        value=periodo if (periodo and periodo != '') else "Todos",
    )

    page.add(ft.Row(
        height=70,
        scroll=ft.ScrollMode.HIDDEN,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.IconButton(icon=ft.Icons.SEARCH_ROUNDED, on_click=lambda _: todas_transacoes(page, dropdown_tipo.value,search_bar.value,dropdown_periodo.value), bgcolor=ft.Colors.DEEP_PURPLE,width=50,height=50),
            dropdown_tipo,
            dropdown_periodo,
            search_bar
            ]
        )
    )
    page.add(ft.Divider())

    #Transações
    page.add(
        ft.Container(
            width=page.width,
            height=page.height*0.68,
            bgcolor=ft.Colors.with_opacity(0.1,ft.Colors.GREY),
            padding=ft.Padding.only(left=20, right=20,top=20),
            margin=10,
            border_radius=30,
            content=ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
                alignment=ft.MainAxisAlignment.START,
                controls=transacoes_filtradas
            )
        )
    )
    if tipo != '' or descricao != '':
        page.show_dialog(
            ft.SnackBar(ft.Text(f'Foram encontradas {int(len(transacoes_filtradas)/2)} transações!'),bgcolor=ft.Colors.DEEP_PURPLE)
        )
    


    page.update()