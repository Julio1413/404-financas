fch.PieChart(
        width=100,
        height=100,
        sections=[
            fch.PieChartSection(
                value=receita if receita > 0 else 1,
                color=ft.Colors.GREEN,
                title="receita",
                badge=ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.GREEN),
            ),
            fch.PieChartSection(
                value=despesa if despesa > 0 else 1,
                color=ft.Colors.RED,
                title="despesa",
                badge=ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.RED),
            ),
        ],
    )