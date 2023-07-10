import flet as ft
import App_Control


def main(page: ft.Page):
    page.title = "Math Game"
    page.window_resizable = False
    # page.window_full_screen = True
    page.window_maximized = True
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.DEEP_PURPLE_900,
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.FADE_UPWARDS
        ),
    )

    def route_change(route):
        page.views.clear()
        rt_use = ft.TemplateRoute(page.route)

        easy = ft.Checkbox(
            label="Easy",
            on_change=lambda _: page.go("/easy"),
            fill_color=ft.colors.BLUE,
        )
        medium = ft.Checkbox(
            label="Medium",
            on_change=lambda _: page.go("/medium"),
            fill_color=ft.colors.ORANGE,
        )
        hard = ft.Checkbox(
            label="Hard",
            on_change=lambda _: page.go("/hard"),
            fill_color=ft.colors.RED_900,
        )

        levels = ft.Container(
            content=ft.Row([easy, medium, hard], alignment=ft.MainAxisAlignment.CENTER)
        )

        btn = ft.Ref[ft.OutlinedButton]()
        open_window = ft.Stack(
            controls=[
                ft.Image(
                    src="./assets/Start.png", fit=ft.ImageFit.CONTAIN
                ),  # "./assets/Get started in Canva (2).png"
                # ft.OutlinedButton("ok click me"),
                ft.Row(
                    controls=[ft.OutlinedButton(ref=btn)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )

        animated_switcher = ft.AnimatedSwitcher(
            open_window,
            transition=ft.AnimatedSwitcherTransition.ROTATION,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.EASE_IN_CUBIC,
            switch_out_curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC,
        )

        def main_page(e) -> None:
            page.clean()
            win = ft.Container(
                content=ft.Stack(
                    [
                        ft.Image(
                            "assets/bg.svg",
                            fit=ft.ImageFit.CONTAIN,
                            width=page.window_width,
                            height=page.window_height,
                        ),
                        ft.Card(
                            content=levels,
                            top=page.window_height / 2,
                            width=page.window_width / 3,
                            left=page.window_width / 3,
                        ),
                    ]
                )
            )
            # ft.Card(content=levels)
            animated_switcher.content = (
                win if animated_switcher.content == open_window else open_window
            )
            page.update()

        btn.current.text = "Begin"
        btn.current.on_click = main_page
        appbar = ft.AppBar(
            leading=ft.Image(src="./assets/logo_ico.ico"),
            title=ft.Text("MATH PRACTICE", size=30),
            bgcolor="#D0BCFF",
        )

        page.views.append(
            ft.View(
                "/",
                [
                    animated_switcher
                ],
                appbar=appbar,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        page.update()

        if rt_use.match("/:id"):
            page.views.append(
                ft.View(
                    f"/{rt_use.id}", controls=[App_Control.check_route(rt_use, page)]
                )
            )

            page.update()

    def view_pop(view) -> None:
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
