import flet as ft
from pages import home, ferramentas,login_page
print("Importando configs...")
def configs(page):
    page.clean()
    #configuração da cor do fundo da página
    def deslogar(_):
        def sair():
            ferramentas.deletar_arquivo("NOME.txt")
            ferramentas.deletar_arquivo("TELEFONE.txt")
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

        
    page.add(ferramentas.header(titulo='Configurações',icone=ft.Icons.SETTINGS,page=page))
    
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
        page.update()

    bright_options = ft.CupertinoSlidingSegmentedButton(
        width=page.width,
        selected_index=0,
        on_change=definir_tema,thumb_color=ft.Colors.BLUE_700,
        padding=ft.padding.symmetric(7, 7),
        controls=[
            ft.Text("Auto"),
            ft.Text("Escuro"),
            ft.Text("Claro"),
        ],
    )
    bright_options.selected_index =  int(ferramentas.ler_arquivo("bright_mode.txt").strip())
        
    def abrir_termos():
        page.launch_url("https://sites.google.com/view/cubepy/nossos-apps/glicapp/termos-de-uso-e-pol%C3%ADtica-de-privacidade-glicapp")
        page.update()
    #construção da página
    page.add(ft.Column(expand=True,spacing=10,controls=[
        bright_options,
        ft.Divider(height=0.5),
        ft.Placeholder(expand=True,color=ft.Colors.TRANSPARENT),
        #termos de uso e privacidade
        ft.Column(alignment=ft.MainAxisAlignment.END,expand=True,controls=[
            ft.ElevatedButton(content=ft.Text('Sair'),bgcolor=ft.Colors.RED_600,icon=ft.Icons.COLOR_LENS_ROUNDED,width=page.width,on_click=deslogar),
            ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
            ft.Text('404 Studios - 2025',text_align=ft.TextAlign.CENTER,size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.GREY),
                ]),
            ft.Text('\n',size=1)
        ])
    ]))
    page.update()
