import flet as ft
import math

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text # ボタンに表示するテキスト
        self.expand = expand # ボタンの幅を指定
        self.on_click = button_clicked # ボタンがクリックされたときに呼び出す関数
        self.data = text # ボタンのデータを設定


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    # application's root control (i.e. "view") containing all other controls
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 10
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),

                ft.Row(
                    controls=[
                        ExtraActionButton(text="x^2", button_clicked=self.button_clicked),
                        ExtraActionButton(text="x^3", button_clicked=self.button_clicked),
                        ExtraActionButton(text="x^y", button_clicked=self.button_clicked),
                        ExtraActionButton(text="e^x", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=(
                        ExtraActionButton(text="√", button_clicked=self.button_clicked),
                        ExtraActionButton(text="∛", button_clicked=self.button_clicked),
                        ExtraActionButton(text="log", button_clicked=self.button_clicked),
                        ExtraActionButton(text="x!", button_clicked=self.button_clicked),
                    ) 
                ),
                ft.Row(
                    controls=(
                        ExtraActionButton(text="sin", button_clicked=self.button_clicked),
                        ExtraActionButton(text="cos", button_clicked=self.button_clicked),
                        ExtraActionButton(text="tan", button_clicked=self.button_clicked),
                        ExtraActionButton(text="π", button_clicked=self.button_clicked),
                    )
                ),
                


                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        elif data in ("x^2"):
            # ユーザーが「x^2」ボタンを押したら、現在の値を 2 乗して表示
            self.result.value = self.format_number(float(self.result.value) ** 2)
            self.reset()
            
        elif data in ("x^3"):
            # ユーザーが「x^3」ボタンを押したら、現在の値を 3 乗して表示
            self.result.value = self.format_number(float(self.result.value) ** 3)
            self.reset()
        
        elif data in ("x^y"):
            # ユーザーが「x^y」ボタンを押したら、現在の値を operand1 に格納
            self.operand1 = float(self.result.value)
            self.operator = "^"  # 演算子を "^" に設定
            self.new_operand = True  # 新しいオペランド入力を待つ状態にする
            self.result.value = "0"  # 次の入力を待機

        elif data in ("e^x"):
            # ユーザーが「e^x」ボタンを押したら、ネイピア数の x 乗を表示
            self.result.value = self.format_number(2.718281828459045 ** float(self.result.value))
            self.reset()
        
        elif data in ("√"):
            # ユーザーが「√」ボタンを押したら、現在の値の平方根を表示
            self.result.value = self.format_number(float(self.result.value) ** 0.5)
            self.reset()
        
        elif data in ("∛"):
            # ユーザーが「∛」ボタンを押したら、現在の値の立方根を表示
            self.result.value = self.format_number(float(self.result.value) ** (1/3))
            self.reset()
        
        elif data in ("log"):
            # ユーザーが「log」ボタンを押したら、現在の値の常用対数を表示
            self.result.value = self.format_number(math.log10(float(self.result.value)))
            self.reset()
        
        elif data in ("x!"):
            # ユーザーが「x!」ボタンを押したら、現在の値の階乗を表示
            try:
                value = float(self.result.value)
                # 入力が非負整数であることを確認
                if value < 0 or not value.is_integer():
                    self.result.value = "Error"  # 負数や小数の場合はエラーを表示
                else:
                    # 階乗を計算 (整数部分を使う)
                    self.result.value = self.format_number(math.factorial(int(value)))
            except (ValueError, OverflowError):
                self.result.value = "Error"  # 大きすぎる数値の場合もエラー
            self.reset()

        elif data in ("sin"):
            # ユーザーが「sin」ボタンを押したら、現在の値の正弦を表示
            # 度をラジアンに変換
            radians = math.radians(float(self.result.value))
            self.result.value = self.format_number(math.sin(radians))
            self.reset()

        elif data in ("cos"):
            # 度をラジアンに変換
            radians = math.radians(float(self.result.value))
            self.result.value = self.format_number(math.cos(radians))
            self.reset()

        elif data in ("tan"):
            # 度をラジアンに変換
            radians = math.radians(float(self.result.value))
            try:
                self.result.value = self.format_number(math.tan(radians))
            except ValueError:
                self.result.value = "Error"  # tan(90°)などの未定義ケースに対応
            self.reset()

        elif data in ("π"):
            # ユーザーが「π」ボタンを押したら、円周率を表示
            self.result.value = self.format_number(math.pi)
            self.reset()
            
        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)
        elif operator == "^":  # ここで x^y を処理
            return self.format_number(operand1 ** operand2)
        else:
            return "Error"


    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()

    # add application's root control to the page
    page.add(calc)


ft.app(target=main)
