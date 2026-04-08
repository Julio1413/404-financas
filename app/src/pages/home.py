
import flet as ft
from pages import configs, ferramentas,login_page
from datetime import datetime
import json as js

# Funções do calendário
versao_atual = "1.0"
print("Importando home...")

def inicial (page):
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    data_atual = datetime.now()
    mes_atual = meses[data_atual.month - 1]

    saldo = 0 


    page.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.ADD,bgcolor=ft.Colors.BLUE_600,shape=ft.RoundedRectangleBorder(radius=40))
    page.add(
        ferramentas.color_header(page=page,
                                 controles=[
                                    ferramentas.header(titulo='404 Finanças',icone=ft.Icons.HOME,page=page,icone_btn=ft.Icons.SETTINGS),
                                    ft.Text('    Saldo:',size=13,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(f"R$ {saldo:.2f}".replace(".", ","),size=55,weight=ft.FontWeight.BOLD,color=ft.Colors.GREEN if saldo > 0 else ft.Colors.BLUE if saldo == 0 else ft.Colors.RED),
                                        ]
                                    ),
                                    ft.Divider(ft.Colors.WHITE_24, height=1, thickness=1),
                                    ft.Text(f'    Resumo do mês de {mes_atual}:',size=13,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Column(
                                                alignment=ft.Alignment.TOP_CENTER,
                                            ),
                                            ft.Column(
                                                alignment=ft.Alignment.TOP_CENTER,
                                            )
                                        ]
                                    )
                                 ]
                            )
    )

    #histórico de transações
    page.add(ft.Placeholder(height=1,color=ft.Colors.TRANSPARENT))
    page.add(
        #titulo
        ft.Text("   Histórico de transações:",size=12,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE),
        #container do histórico
        ft.Container(
            border_radius=30,
            padding=5,
            margin=10,
            width=page.width,
            height=page.height-550,
            bgcolor=ft.Colors.with_opacity(0.1,ft.Colors.GREY),

        )
    )



    page.update()
 
