import flet as ft
from pages import home, ferramentas,login_page
import time
print("Importando configs...")
def configs(page):
    page.clean()
    
    #Fun,ões essenciais
    def deslogar(_):
        def sair():
            ferramentas.deletar_arquivo("NOME.txt")
            ferramentas.deletar_arquivo("TELEFONE.txt")
            ferramentas.deletar_arquivo("CATEGORIAS.txt")
            ferramentas.deletar_arquivo("TRANSAÇÕES.json")
            page.clean()
            login_page.login_page_2(page)
            dlg.open = False
            page.update()
            
        dlg = ferramentas.dialog(
            page=page,
            titulo='Sair',
            texto_btn='Sair',
            funcao_btn=lambda _:sair(),
            icone_d=ft.Icons.DELETE_FOREVER_ROUNDED,
            icone_e=ft.Icons.DELETE_FOREVER_ROUNDED,
            conteudo=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Text('Tem certeza de que deseja\nsair da sua conta 6X2?',weight=ft.FontWeight.BOLD)]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Icon(icon=ft.Icons.DELETE_FOREVER_ROUNDED,color=ft.Colors.RED,size=100)]),
            ]
        )
        page.show_dialog(dlg)
        page.update()

    def definir_tema(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.theme_mode = ft.ThemeMode.SYSTEM
        elif selected_index == 1:
            page.theme_mode = ft.ThemeMode.DARK
            page.brightness = ft.Brightness.DARK
        elif selected_index == 2:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.brightness = ft.Brightness.LIGHT
        ferramentas.criar_arquivo(nome="bright_mode.txt",conteudo=str(selected_index))
        time.sleep(0.2)
        page.clean()
        configs(page)
        page.update()

    def editar_categorias(e):
        if ferramentas.arquivo_existe("CATEGORIAS.txt"):
            categorias = ferramentas.ler_arquivo("CATEGORIAS.txt").splitlines()
        else:
            categorias = ["Alimentação", "Transporte", "Moradia"]
            ferramentas.criar_arquivo("CATEGORIAS.txt", "\n".join(categorias))

        def apagar_categoria(e,categoria):
            if categoria in categorias:
                categorias.remove(categoria)
                ferramentas.criar_arquivo("CATEGORIAS.txt", "\n".join(categorias))
                ferramentas.fechar_dialog(page, dlg)
                editar_categorias(e)

        def adicionar_categoria(e):
            campo_nome = ft.TextField(label="Nome da categoria", autofocus=True)
            def salvar(e):
                nome = campo_nome.value.strip() if campo_nome.value else ""
                if nome and nome not in categorias:
                    categorias.append(nome)
                    ferramentas.criar_arquivo("CATEGORIAS.txt", "\n".join(categorias))
                    ferramentas.fechar_dialog(page, dlg_add)
                    ferramentas.fechar_dialog(page, dlg)
                    editar_categorias(e)
                else:
                    campo_nome.error_text = "Nome inválido ou já existe"
                    page.update()

            dlg_add = ferramentas.dialog(
                page=page,
                icone_d=ft.Icons.ADD_ROUNDED,
                icone_e=ft.Icons.CATEGORY_ROUNDED,
                titulo='Nova Categoria',
                texto_btn='Adicionar',
                funcao_btn=salvar,
                conteudo=[campo_nome]
            )
            page.show_dialog(dlg_add)
            page.update()


        conteudo =[]
        for c in categorias:
            conteudo.append(
                ft.Container(
                    border_radius=40,
                    height=50,
                    padding=ft.Padding.only(left=10,right=5),
                    bgcolor=ft.Colors.with_opacity(0.1,ft.Colors.GREY),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(value=c,weight=ft.FontWeight.BOLD,size=15),
                            ft.IconButton(icon=ft.Icons.DELETE_ROUNDED,icon_color=ft.Colors.RED,on_click=lambda e, cat=c: apagar_categoria(e, cat)),
                        ]
                    )
                )
            )

        dlg = ferramentas.dialog(
            page=page,
            icone_d=ft.Icons.EDIT_ROUNDED,
            icone_e=ft.Icons.CATEGORY_ROUNDED,
            titulo='Editar categorias',
            texto_btn='Adicionar',
            funcao_btn=adicionar_categoria,
            conteudo=[
                ft.Column(
                    scroll=ft.ScrollMode.ADAPTIVE,
                    alignment=ft.MainAxisAlignment.START,
                    controls=conteudo
                )
            ]
            )
        page.show_dialog(dlg)
        page.update()
        
    page.add(
        ferramentas.color_header(
            page=page,
            altura=63,
            controles=[
                ferramentas.header(titulo='Configurações',icone=ft.Icons.SETTINGS,page=page)
            ]
        )
    )
    

    bright_options = ft.CupertinoSlidingSegmentedButton(
        width=page.width,
        bgcolor=ft.Colors.TRANSPARENT,
        selected_index=0,
        on_change=definir_tema,thumb_color=ft.Colors.PURPLE_700,
        padding=ft.padding.symmetric(7, 7),
        controls=[
            ft.Text("Auto"),
            ft.Text("Escuro"),
            ft.Text("Claro"),
        ],
    )
    bright_options.selected_index =  int(ferramentas.ler_arquivo("bright_mode.txt").strip())
        
    #Configurações
    page.add(ft.Column(expand=True,spacing=10,controls=[
        ft.Placeholder(color=ft.Colors.TRANSPARENT,height=1),
        bright_options,
        ft.Divider(height=0.5),
        ft.ElevatedButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Icon(icon=ft.Icons.CATEGORY_ROUNDED,color=ft.Colors.PURPLE),
                    ft.Text('Editar categorias',color=ferramentas.brightness_text(page),weight=ft.FontWeight.BOLD),
                ]
            ),
            on_click=lambda _:editar_categorias(page),
            width=page.width,
        ),
        ft.Divider(height=0.5),


        ft.Placeholder(expand=True,color=ft.Colors.TRANSPARENT),
        
    ]))
    


    #Rodapé
    page.add(
        ft.Column(alignment=ft.MainAxisAlignment.END,expand=True,controls=[
            ft.ElevatedButton(content=ft.Text('Sair'),bgcolor=ft.Colors.RED_600,icon=ft.Icons.COLOR_LENS_ROUNDED,width=page.width,on_click=deslogar),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
            ft.Text('404 Studios - 2026',text_align=ft.TextAlign.CENTER,size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                ]),
            ft.Text('\n',size=1)
        ])
    )
    page.update()
