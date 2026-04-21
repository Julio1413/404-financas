import flet as ft
import os
from http.cookies import SimpleCookie

#padding geral da ui
print("Ferramentas utilizadas")

PASTA = None

def set_pasta(path: str):
    global PASTA
    PASTA = path


def get_pasta() -> str:
    global PASTA
    if PASTA is None:
        raise RuntimeError("PASTA ainda não foi inicializada")
    return PASTA




#funções adaptadas para web
def criar_arquivo(nome:str,conteudo:str,metodo='w'):
    if PASTA: #local
        with open(os.path.join(PASTA,nome), metodo, encoding="utf-8") as f:
            f.write(conteudo)
    else: #web
        cookie = SimpleCookie()
        cookie_name = nome.replace('.', '_')
        cookie[cookie_name] = conteudo
        cookie[cookie_name]["max-age"] = 31536000 
        cookie[cookie_name]["path"] = "/"
        
def ler_arquivo(nome:str, cookie_header:str='404 Studios'):
    if PASTA: #local
        if os.path.exists(os.path.join(PASTA,nome)):
            with open(os.path.join(PASTA,nome), "r", encoding="utf-8") as f:
                retorno = f.read()
        else:
            retorno =  None
    else: #web 
        cookie = SimpleCookie()
        cookie.load(cookie_header)
        cookie_name = nome.replace('.', '_')
        retorno =  cookie[cookie_name].value if cookie_name in cookie else None           
    return retorno

def deletar_arquivo(nome:str):
    if PASTA:
        if os.path.exists(os.path.join(PASTA,nome)):
            os.remove(os.path.join(PASTA,nome))
    else:
        cookie = SimpleCookie()
        cookie_name = nome.replace('.', '_')
        cookie[cookie_name] = ""
        cookie[cookie_name]["max-age"] = 0
        cookie[cookie_name]["path"] = "/"
        
def arquivo_existe(nome:str, cookie_header:str='404 Studios'):
    if PASTA:
        return os.path.exists(os.path.join(PASTA,nome))
    else:
        cookie = SimpleCookie()
        cookie.load(cookie_header)
        cookie_name = nome.replace('.', '_')
        return cookie_name in cookie

#ferramentas de interface (header e container)
def header( 
            titulo,
            icone,
            page,
            destino=None,
            icone_btn=ft.Icons.ARROW_BACK_IOS_ROUNDED,
            desabilitar_btn=False
           ):
    # Importação obrigatória de home
    from pages import home
    if destino is None:
        destino = home.inicial
    return ft.Column(controls=[ft.Container(height=45,padding=-10,
        content=ft.Container(alignment=ft.Alignment.BOTTOM_CENTER,
            padding=ft.Padding.only(left=padding(), right=padding(),bottom=10),
            blur=(0,0),
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        disabled=desabilitar_btn,
                        icon_color=ft.Colors.WHITE,
                        icon=icone_btn,
                        on_click=lambda _:destino(page),
                        icon_size=25,
                    ),
                    ft.Text(
                        value=titulo,
                        color=ft.Colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(icone, color=ft.Colors.WHITE,size=30),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            height=50,
            margin=ft.Margin.all(-10),
        ),
    ),
    ft.Placeholder(height=10,color=ft.Colors.TRANSPARENT)
                               ])


def color_header(
        page,
        controles=[],
        altura=330
        ):
    return ft.Column(
        controls=[
            ft.Placeholder(color=ft.Colors.TRANSPARENT,height=14),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment.TOP_CENTER,
                            end=ft.Alignment.BOTTOM_CENTER,
                            colors=[ft.Colors.DEEP_PURPLE_900, ft.Colors.DEEP_PURPLE_300]
                        ),
                        width=page.width*0.97,
                        height=altura,
                        padding=ft.padding.only(left=12, right=12),
                        border_radius=ft.BorderRadius.only(bottom_left=30, bottom_right=30,top_left=30,top_right=30),
                        margin=ft.Margin.all(-5),
                        content=ft.Column(
                            controls=controles,
                        )
                    )
                ]
            )
        ]
    )


def container(page,
              controles=[],
              ):
    return ft.Container(
            expand=True,
            margin=ft.margin.all(-10),
            padding=ft.padding.all(17),
            border_radius=ft.border_radius.only(top_left=42, top_right=42),
            bgcolor=brightness(page),
            alignment=ft.Alignment.TOP_CENTER,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                alignment=ft.MainAxisAlignment.START,
                controls=controles
            )
        )
    
def bottom_sheet(page,
                 icone_d,
                 icone_e,
                 titulo,
                 controles:list = []
                 ):
    sheet = ft.BottomSheet(
        bgcolor=ft.Colors.with_opacity(0.0, ft.Colors.WHITE),
        content=ft.Container(
            blur=(10,10),
            bgcolor=ft.Colors.with_opacity(0.2, brightness(page)),
            margin=ft.margin.only(top=0,left=0,right=0,bottom=0),
            border_radius=ft.border_radius.all(30),
            expand=True,
            height=400,
            width=page.width*0.8,
            padding=ft.padding.all(15),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    # título
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Icon(icon=icone_d),
                            ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD),
                            ft.Icon(icon=icone_e),
                        ]
                    ), 
                    ft.Divider(),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        controls=controles,
                    )
                ]
            )
        )
    )
    return sheet


    
def dialog(page,
    titulo,
    icone_e=None,
    icone_d=None,
    funcao_btn='',
    texto_btn='',
    conteudo=[]
):
    if funcao_btn and texto_btn: btn2 = ft.TextButton(texto_btn, on_click=funcao_btn)
    else: btn2=ft.Text('')
    
   
    dlg = ft.AlertDialog(
        modal=True,
        content_padding=ft.padding.all(0),
        bgcolor=ft.Colors.with_opacity(0.0, ft.Colors.WHITE),
        barrier_color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        content=ft.Container(
            blur=(10, 10),
            bgcolor=ft.Colors.with_opacity(0.2, brightness(page)),
            margin=ft.margin.only(top=0,left=0,right=0,bottom=0),
            border_radius=ft.border_radius.all(20),
            expand=True,
            height=450,
            width=400,
            padding=ft.padding.all(6),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # título
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Icon(icon=icone_d),
                            ft.Text(titulo, size=17, weight=ft.FontWeight.BOLD),
                            ft.Icon(icon=icone_e),
                        ]
                    ), 
                    ft.Divider(height=1),
                    ft.Column(width=400,
                        scroll=ft.ScrollMode.AUTO,
                        alignment=ft.MainAxisAlignment.START,
                        expand=True,
                        controls=[       
                            ft.Text('\n', size=3),
                            # conteúdo do dialog
                            ft.Column(controls=conteudo, alignment=ft.MainAxisAlignment.START),
                            ft.Text('\n', size=3),
                        ]
                    ),
                    ft.Divider(height=1),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(page, dlg)),
                            btn2
                        ]
                    )
                ]
            )
        )
    )


    return dlg

def padding():
    return 17
import flet as ft
#cor para janela
def brightness(page):
    if page.theme_mode == ft.ThemeMode.LIGHT:
        container_color = ft.Colors.WHITE
    else:
        container_color = ft.Colors.BLACK87
    page.update()
    return container_color

#cor para texto
def brightness_text(page):
    if page.theme_mode == ft.ThemeMode.LIGHT:
        text_color = ft.Colors.BLACK87
    else:
        text_color = ft.Colors.WHITE
    page.update()
    return text_color

def fechar_dialog(page, dlg):
    dlg.open = False
    page.update()