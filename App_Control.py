import flet as ft
import random as rd

NO_OF_ROUND = 1
IMAGE_PATH = "./assets/cong.png"


def get_number(max_value, size):
    lst: list[int] = [rd.randint(0, max_value) for _ in range(size)]

    formatted_numbers = (
        ["{:03d}".format(num) for num in lst]
        if max_value <= 1000
        else ["{:04d}".format(num) for num in lst]
    )
    return formatted_numbers


def get_number_for_mul(max_value, size):
    lst: list[int] = [rd.randint(0, max_value) for _ in range(size)]
    lst.pop()
    lst.append(rd.randint(0, 10))
    formatted_numbers = (
        ["{:03d}".format(num) for num in lst]
        if max_value <= 1000
        else ["{:04d}".format(num) for num in lst]
    )
    return formatted_numbers


def print_addition_question(numbers: list[int], opr: str) -> str:
    formatted_numbers = [f"    {num}" for num in numbers]
    question = "\n".join(formatted_numbers)
    question += f"\n{opr}"
    return question


# Route Check Function
def check_route(rt_use: ft.TemplateRoute, page) -> ft.UserControl:
    match rt_use.id:
        # Starting of Every Level
        case "easy":
            # Parameter : Max number, size, page, next route
            return Addition(100, 3, page, "/esub")
        case "medium":
            return Addition(900, 4, page, "/msub")
        case "hard":
            return Addition(9999, 4, page, "/hsub")

        # Subtraction for all levels
        case "esub":
            return Subtraction(100, 2, page, "/emul")
        case "msub":
            return Subtraction(1000, 2, page, next_route="/mmul")
        case "hsub":
            return Subtraction(10000, 2, page, "/hmul")

        # Multiplication
        case "emul":
            return Multiplication(100, 2, page, "/medium")
        case "mmul":
            return Multiplication(1000, 2, page, "/hard")
        case "hmul":
            return Multiplication(2000, 2, page, "/completed")

        case "completed":
            pass


# Controls classes
class Addition(ft.UserControl):
    def __init__(self, max_value: int, size: int, page: ft.Page, next_route: str):
        super().__init__()
        self.max_value = max_value
        self.size = size
        self._page = page

        # Controls
        self.no = get_number(self.max_value, self.size)
        self.res = ft.TextField(
            label="Result",
            width=self._page.width / 3,
            text_align=ft.TextAlign.CENTER,
            text_size=30,
            content_padding=10,
            icon=ft.icons.EMOJI_EVENTS_ROUNDED,
        )
        self.res_text = ft.Text(size=40)
        self.nt_text = ft.Text(size=40)
        self.test = ft.Ref[ft.Text]()
        self.btn_next = ft.Ref[ft.ElevatedButton]()
        self.last_text = ft.Ref[ft.Text]()

        # Values
        self.title = "Round One\nAddition (+)"
        self.count = 0
        # self._pass = False
        self.rt_use = ft.TemplateRoute(page.route)
        self.next_rt = next_route
        self.image = IMAGE_PATH
        self.nt_round = "Go to next Round..."
        self.opr = "+"

    def sum(self) -> int:
        total = 0
        for element in self.no:
            if isinstance(element, int) or element.isdigit():
                total += int(element)
        return total

    def check(self, e) -> None:
        if self.res.value.isdigit():
            if self.sum() == int(self.res.value):
                self.res_text.bgcolor = ft.colors.SURFACE_VARIANT
                self.res_text.value = "CORRECT"
                self.btn_next.current.on_click = self.next_
                self.res_text.update()
            else:
                self.res_text.clean()
                self.res_text.value = "INCORRECT"
                self.res_text.bgcolor = ft.colors.RED_ACCENT_700
                self.res_text.update()

    def next_ui(self):
        btn_style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.INDIGO_900,
                ft.MaterialState.FOCUSED: ft.colors.INDIGO_900,
                ft.MaterialState.DEFAULT: ft.colors.INDIGO_500,
            },
            elevation={"pressed": 0, "": 10},
            overlay_color=ft.colors.TRANSPARENT,
            shape={
                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                ft.MaterialState.DEFAULT: ft.BeveledRectangleBorder(radius=10),
            },
            side={ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE)},
        )
        self.clean()
        self.page.views.append(
            ft.View(
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Image(self.image),
                            ft.ElevatedButton(
                                text=self.nt_round,
                                on_click=lambda _: self.page.go(self.next_rt),
                                bottom=260,
                                right=540,
                                style=btn_style,
                            ),
                        ]
                    )
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        if self.rt_use.match("/:id"):
            check_route(self.rt_use, page=self._page)
        self.page.update()

    def next_(self, e) -> None:
        if self.res_text.value == "CORRECT":
            self.no = get_number(self.max_value, self.size)
            # self.test.current.value = "\n".join(map(str, self.no))
            self.test.current.value = print_addition_question(self.no, self.opr)
            self.res_text.value = None
            self.res.value = None
            self.count += 1
            self.btn_next.current.data += 1
            self.last_text.current.value = self.btn_next.current.data
            self.update()
        if self.count == NO_OF_ROUND:
            self.next_ui()

    def build(self):
        ans_c = self.sum()
        res = self.res
        ans = ft.Text("")
        btn = ft.OutlinedButton(
            icon=ft.icons.CATCHING_POKEMON_ROUNDED, on_click=self.check
        )
        # print(ans_c)
        self.nt_text.value = None
        return [
            ft.Container(
                content=ft.Stack(
                    width=600,
                    height=self._page.height,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    ref=self.test,
                                    # value="\n".join(map(str, self.no)),
                                    value=print_addition_question(self.no, self.opr),
                                    size=40,
                                ),
                                res,
                                ft.Row(
                                    controls=[
                                        btn,
                                        ft.ElevatedButton(
                                            ref=self.btn_next, text="NEXT", data=0
                                        ),
                                        ft.Text(ref=self.last_text),
                                    ]
                                ),
                                self.res_text,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            controls=[
                                # ft.Card
                                ft.Container(
                                    content=ft.Stack(
                                        controls=[
                                            ft.Text(
                                                ref=self.last_text,
                                                size=20,
                                                color=ft.colors.GREEN_900,
                                            )
                                        ]
                                    ),
                                    width=20,
                                )
                            ],
                            bottom=200,
                            right=1,
                        ),
                    ],
                ),
                bgcolor=ft.colors.SURFACE_VARIANT,  # SURFACE_VARIANT, #2b2675c7
                alignment=ft.alignment.center,
                border_radius=10,
            ),
            ft.Container(
                content=ft.Stack(
                    controls=[
                        ft.Column(
                            controls=[TextGrd(self.title), TextGrd(self.nt_text.value)]
                        )
                    ]
                ),
                alignment=ft.alignment.center,
            ),
        ]


class Subtraction(Addition):
    def __init__(self, max_value, size, page, next_route):
        super().__init__(max_value, size, page, next_route)
        self.max_value = max_value
        self.size = size
        # print(self.sum())
        self.title = "Round Two \n Subtraction(-)"
        self.opr = "-"

    def sum(self):
        self.no.sort(reverse=True)
        result = int(self.no[0])
        for i in range(1, len(self.no)):
            result -= int(self.no[i])
        return result

    def check(self, e):
        if self.res.value.isdigit():
            if str(self.sum()).removeprefix("-") == str(self.res.value):
                self.res_text.value = "CORRECT"
                self.res_text.bgcolor = ft.colors.SURFACE_VARIANT
                self.btn_next.current.on_click = self.next_
                self.res_text.update()
            else:
                self.res_text.value = "INCORRECT"
                self.res_text.bgcolor = ft.colors.RED_ACCENT_700
                self.res_text.update()


class Multiplication(Addition):
    def __init__(self, max_value, size, page, next_route):
        super().__init__(max_value, size, page, next_route)
        self.max_value = max_value
        self.size = size
        # print(self.sum())
        self.title = "Round Three (x)"
        self.nt_round = "Go to Medium Round"
        self.opr = "x"
        self.no = get_number_for_mul(self.max_value, self.size)
        self.image = "./assets/Level2.png"

    def sum(self):
        total = 1
        for element in self.no:
            if isinstance(element, int) or element.isdigit():
                total *= int(element)
        return total


class TextGrd(ft.UserControl):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def build(self):
        return ft.Stack(
            controls=[
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            self.text,
                            ft.TextStyle(
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                font_family="Lucida Calligraphy",
                                shadow=ft.BoxShadow(
                                    spread_radius=40,
                                    blur_radius=10,
                                    color=ft.colors.BLACK38,
                                ),
                                foreground=ft.Paint(
                                    ft.colors.INDIGO_700,
                                    anti_alias=True,
                                    blend_mode=ft.BlendMode.MULTIPLY,
                                ),
                            ),
                        )
                    ]
                )
            ]
        )
