import tkinter as tk
import math


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        root.title("Scientific Calculator")
        root.geometry("380x560")
        root.resizable(False, False)

        self.expr = ""
        self.ans = 0
        self.mode = "DEG"
        self.just_done = False

        # Display
        self.hist_var = tk.StringVar()
        self.disp_var = tk.StringVar(value="0")

        tk.Label(
            root,
            textvariable=self.hist_var,
            anchor="e",
            fg="gray40",
            font=("Arial", 11)
        ).pack(fill="x", padx=15, pady=(10, 0))

        entry = tk.Entry(
            root,
            textvariable=self.disp_var,
            font=("Arial", 26),
            justify="right",
            state="readonly",
            readonlybackground="white",
            relief="solid"
        )
        entry.pack(fill="x", padx=15, pady=5, ipady=8)

        # Keypad layout
        keys = [
            ["Deg", "sin", "cos", "tan", "C"],
            ["asin", "acos", "atan", "(", ")"],
            ["ln", "log", "e^x", "sqrt", "x^2"],
            ["7", "8", "9", "/", "DEL"],
            ["4", "5", "6", "*", "^"],
            ["1", "2", "3", "-", "pi"],
            ["0", ".", "x!", "+", "e"],
            ["1/x", "abs", "Ans", "=", "10^x"]
        ]

        pad = tk.Frame(root)
        pad.pack(padx=10, pady=10)

        for r, row in enumerate(keys):
            for c, lbl in enumerate(row):
                b = tk.Button(
                    pad,
                    text=lbl,
                    width=5,
                    height=2,
                    font=("Arial", 12),
                    command=lambda t=lbl: self.key_pressed(t)
                )
                b.grid(row=r, column=c, padx=2, pady=2)

                if lbl == "Deg":
                    self.mode_btn = b

                if lbl == "=":
                    b.config(font=("Arial", 12, "bold"))

    # Button handling
    def key_pressed(self, lbl):

        if lbl == "C":
            self.expr = ""
            self.hist_var.set("")
            self.just_done = False
            self.refresh()
            return

        if lbl == "DEL":
            self.expr = self.expr[:-1]
            self.refresh()
            return

        if lbl in ("Deg", "Rad"):
            if self.mode == "DEG":
                self.mode = "RAD"
                self.mode_btn.config(text="Rad")
            else:
                self.mode = "DEG"
                self.mode_btn.config(text="Deg")
            return

        if lbl == "=":
            self.calculate()
            return

        # Start new expression after result
        if self.just_done and lbl not in (
            "+", "-", "*", "/", "^", "x^2"
        ):
            self.expr = ""

        self.just_done = False
        self.expr += self.insert_text(lbl)
        self.refresh()

    def insert_text(self, lbl):
        table = {
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "asin": "asin(",
            "acos": "acos(",
            "atan": "atan(",
            "ln": "ln(",
            "log": "log(",
            "e^x": "exp(",
            "sqrt": "sqrt(",
            "x^2": "**2",
            "^": "**",
            "x!": "fact(",
            "1/x": "1/(",
            "abs": "abs(",
            "10^x": "10**("
        }

        return table.get(lbl, lbl)

    # Calculation
    def calculate(self):
        if not self.expr:
            return

        deg = self.mode == "DEG"

        to_rad = math.radians if deg else (lambda x: x)
        from_rad = math.degrees if deg else (lambda x: x)

        def fact(x):
            if x != int(x) or x < 0:
                raise ValueError("factorial")
            return math.factorial(int(x))

        env = {
            "__builtins__": {},
            "sin": lambda x: math.sin(to_rad(x)),
            "cos": lambda x: math.cos(to_rad(x)),
            "tan": lambda x: math.tan(to_rad(x)),
            "asin": lambda x: from_rad(math.asin(x)),
            "acos": lambda x: from_rad(math.acos(x)),
            "atan": lambda x: from_rad(math.atan(x)),
            "ln": math.log,
            "log": math.log10,
            "exp": math.exp,
            "sqrt": math.sqrt,
            "fact": fact,
            "abs": abs,
            "pi": math.pi,
            "e": math.e,
            "Ans": self.ans
        }

        try:
            val = eval(self.expr, env)

            if not isinstance(val, (int, float)) or not math.isfinite(val):
                raise ValueError("math")

        except (ZeroDivisionError, ValueError, OverflowError):
            self.show_error("Math Error")
            return

        except Exception:
            self.show_error("Syntax Error")
            return

        self.hist_var.set(self.expr + " =")
        self.ans = val
        self.expr = format(val, ".10g")
        self.just_done = True
        self.refresh()

    def show_error(self, msg):
        self.disp_var.set(msg)
        self.expr = ""
        self.just_done = False

    def refresh(self):
        self.disp_var.set(self.expr if self.expr else "0")


if __name__ == "__main__":
    root = tk.Tk()
    ScientificCalculator(root)
    root.mainloop()
