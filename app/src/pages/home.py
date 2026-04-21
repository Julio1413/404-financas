import flet as ft
import flet_charts as fch
from pages import configs, ferramentas,ia,todas_transacoes
from datetime import datetime
import json as js
import re

versao_atual = "1.0"
print("Importando home...")

def inicial (page):
    page.clean()

    if ferramentas.arquivo_existe('bright_mode.txt'):
        bright_mode = ferramentas.ler_arquivo("bright_mode.txt").strip()
    else:
        ferramentas.criar_arquivo("bright_mode.txt","0")
        bright_mode = "0"

    if bright_mode == "1":
        page.theme_mode = ft.ThemeMode.DARK
    elif bright_mode == "2":
        page.theme_mode = ft.ThemeMode.LIGHT



    if ferramentas.arquivo_existe(nome="TRANSAÇÕES.json"):
        transacoes = js.loads(ferramentas.ler_arquivo("TRANSAÇÕES.json"))
        print(js.dumps(transacoes,indent=4, ensure_ascii=False))
    else:
        ferramentas.criar_arquivo("TRANSAÇÕES.json",'[]')
        transacoes = []
        print(transacoes)


    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    data_atual = datetime.now()
    mes_atual = meses[data_atual.month - 1]

    #tipos
    if ferramentas.arquivo_existe("tipoS.txt"):
        tipos = ferramentas.ler_arquivo("tipoS.txt").splitlines()
    else:
        tipos = ["Alimentação", "Transporte", "Moradia"]
        ferramentas.criar_arquivo("tipoS.txt", "\n".join(tipos))










    def adicionar_transacao():
        valor_centavos = 0

        def formatar_brasileiro(centavos: int) -> str:
            reais = centavos // 100
            cents = centavos % 100
            partes = []
            for i, chunk in enumerate(reversed(str(reais))):
                if i and i % 3 == 0:
                    partes.append('.')
                partes.append(chunk)
            reais_formatados = ''.join(reversed(partes)) or '0'
            return f"R$ {reais_formatados},{cents:02d}"

        def on_change_valor(e):
            nonlocal valor_centavos
            texto = re.sub(r'\D', '', e.control.value or '')
            if texto == '':
                valor_centavos = 0
            else:
                valor_centavos = int(texto)
            formatted = formatar_brasileiro(valor_centavos)
            if e.control.value != formatted:
                e.control.value = formatted
                e.control.cursor_position = len(formatted)
                e.control.update()

        #campos de entrada
        valor = ft.TextField(
            expand=True,
            focused_border_color=ft.Colors.DEEP_PURPLE_600,
            border_radius=40,
            label="Valor (R$)",
            value="R$ 0,00",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=on_change_valor
        )
        tipo = ft.Dropdown(expand=True,focused_border_color=ft.Colors.DEEP_PURPLE_600,border_radius=40,label="Tipo", options=[ft.dropdown.Option("Receita"), ft.dropdown.Option("Despesa")])
        tipo_categoria = ft.Dropdown(expand=True,focused_border_color=ft.Colors.DEEP_PURPLE_600,border_radius=40,label="Tipo Categoria", options=[ft.dropdown.Option(i) for i in tipos])
        descricao = ft.TextField(expand=True,focused_border_color=ft.Colors.DEEP_PURPLE_600,border_radius=40,label="Descrição", multiline=True, keyboard_type=ft.KeyboardType.TEXT)

        dlg = ferramentas.dialog(
                page=page,
                titulo='Adicionar transação',
                icone_d=ft.Icons.ADD_ROUNDED,
                icone_e=ft.Icons.MONEY_ROUNDED,
                texto_btn='Salvar',
                funcao_btn=lambda _:salvar(),
                conteudo=[
                    valor,
                    descricao,
                    tipo,
                    tipo_categoria
                ],
            )


        def salvar():
            if valor_centavos > 0 and tipo.value and descricao.value:
                transacoes.append({
                    "periodo":f"{data_atual.month}.{data_atual.year}",
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "valor": valor_centavos / 100.0,
                    "tipo": tipo.value,
                    "descricao": descricao.value,
                    "tipo_categoria": tipo_categoria.value
                })
                ferramentas.criar_arquivo("TRANSAÇÕES.json", js.dumps(transacoes,indent=4, ensure_ascii=False))
                page.show_dialog(ft.SnackBar(ft.Text("Transação adicionada com sucesso!"), bgcolor=ft.Colors.GREEN))
                ferramentas.fechar_dialog(page,dlg)
                inicial(page)
                page.update()
            else:
                page.show_dialog(ft.SnackBar(ft.Text("Preencha todos os campos!"), bgcolor=ft.Colors.RED))

        page.show_dialog(
            dlg
        )
        page.update()

    saldo = 0 
    receita = 0
    despesa = 0
    for t in transacoes:
        if t["periodo"] == f"{data_atual.month}.{data_atual.year}":
            if t["tipo"] == "Receita":
                saldo += t["valor"]
                receita += t["valor"]
            else:
                saldo -= t["valor"]
                despesa += t["valor"]

    page.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=lambda _: adicionar_transacao(),bgcolor=ft.Colors.DEEP_PURPLE_600,shape=ft.RoundedRectangleBorder(radius=40))
    page.add(
        ferramentas.color_header(page=page,
                                 controles=[
                                    ferramentas.header(titulo='404 Finanças',icone=ft.Icons.HOME,page=page,icone_btn=ft.Icons.SETTINGS,destino=lambda _:configs.configs(page)),
                                    ft.Text('    Saldo:',size=13,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(f"R$ {(saldo):.2f}".replace(".", ","),size=55,weight=ft.FontWeight.BOLD,color=ft.Colors.GREEN_700 if saldo > 0 else (ft.Colors.WHITE if saldo == 0 else ft.Colors.RED)),
                                        ]
                                    ),
                                    ft.Divider(ft.Colors.WHITE_24, height=1, thickness=1),
                                    ft.Text(f'    Resumo do mês de {mes_atual}:',size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE),
                                    
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            ft.Column(
                                                spacing=5,
                                                controls=[
                                                    ft.Text(f'+ R$ {receita:.2f}'.replace(".", ","),weight=ft.FontWeight.BOLD,color=ft.Colors.GREEN_700,size=25),
                                                    ft.Text(f'- R$ {despesa:.2f}'.replace(".", ","),weight=ft.FontWeight.BOLD,color=ft.Colors.RED,size=25),
                                                ]
                                            ),
                                            fch.PieChart(
                                                start_degree_offset=90,
                                                margin=-20,
                                                center_space_radius=0,
                                                width=100,
                                                height=100,
                                                sections=[
                                                    fch.PieChartSection(
                                                        value=receita if receita > 0 else 1,
                                                        color=ft.Colors.GREEN,
                                                        badge=ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.GREEN),
                                                        title=f"{(receita/(receita+despesa)*100):.0f}%" if receita+despesa > 0 else "0%",
                                                    ),
                                                    fch.PieChartSection(
                                                        value=despesa if despesa > 0 else 1,
                                                        color=ft.Colors.RED,
                                                        badge=ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.RED),
                                                        title=f"{(despesa/(receita+despesa)*100):.0f}%" if receita+despesa > 0 else "0%",
                                                    ),
                                                ],
                                            ),
                                        ]
                                    )
                                 ]
                            )
    )

    #histórico de transações
    historico = []
    for t in reversed(transacoes):
        if t["periodo"] == f"{data_atual.month}.{data_atual.year}":
            historico.append(
                ft.Column(
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(t["tipo"],weight=ft.FontWeight.BOLD),
                                    ft.Text(t["data"],size=10)
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(t["descricao"],size=12),
                                    ft.Text(f'R$ {t["valor"]:.2f}'.replace(".", ","),weight=ft.FontWeight.BOLD,color=ft.Colors.GREEN_700 if t["tipo"] == "Receita" else ft.Colors.RED)
                                ]
                            )
                        ]
                    )
            )







    page.add(ft.Placeholder(height=1,color=ft.Colors.TRANSPARENT))
    page.add(
        #titulo
        ft.Text("   Histórico de transações do mês:",size=12,weight=ft.FontWeight.BOLD),
        #container do histórico
        ft.Container(
            border_radius=30,
            padding=ft.Padding.only(left=20, right=20,top=20),
            margin=10,
            width=page.width,
            height=page.height-550,
            bgcolor=ft.Colors.with_opacity(0.1,ft.Colors.GREY),
            content=ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
                controls=historico,
            )

        )
    )
    page.add(
        ft.Container(
            border_radius=30,
            padding=ft.Padding.only(left=14,top=10,bottom=10),
            margin=10,
            on_click=lambda _: todas_transacoes.todas_transacoes(page),
            width=page.width,
            height=50,
            bgcolor=ft.Colors.with_opacity(0.1,ft.Colors.GREY),
            content=ft.Row(
                controls=[
                    ft.Icon(icon=ft.Icons.MONEY_ROUNDED,color=ft.Colors.DEEP_PURPLE),
                    ft.Text('Todas as transações',weight=ft.FontWeight.BOLD)
                ],
            )
        )
    )
    page.add(
        ft.Container(
            border_radius=30,
            padding=ft.Padding.only(left=14,top=10,bottom=10),
            margin=10,
            on_click=lambda _: ia.ia(page),
            width=page.width,
            height=50,
            bgcolor=ft.Colors.with_opacity(0.1,ft.Colors.GREY),
            content=ft.Row(
                controls=[
                    ft.Icon(icon=ft.Icons.ADB_ROUNDED,color=ft.Colors.DEEP_PURPLE),
                    ft.Text('Recursos de IA',weight=ft.FontWeight.BOLD)
                ],
            )
        )
    )
    page.add(
        ft.Placeholder(height=10,color=ft.Colors.TRANSPARENT)
    )
    page.add(
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text("Desenvolvido por 404 Studios",size=10,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE_60)
                ]
            )
        )

    
 

    page.update()
 