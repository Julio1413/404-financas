fch.PieChart(
        width=100,
        height=100,
        sections=[
            fch.PieChartSection(
                value=Receita if Receita > 0 else 1,
                color=ft.Colors.GREEN,
                title="Receita",
                badge=ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.GREEN),
            ),
            fch.PieChartSection(
                value=Despesa if Despesa > 0 else 1,
                color=ft.Colors.RED,
                title="Despesa",
                badge=ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.RED),
            ),
        ],
    )