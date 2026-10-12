import tkinter as tk
from tkinter import messagebox
import math
import ast
import operator


class CalcPro:

    def __init__(self, root):

        self.root = root

        # Window
        self.root.title("CalcPro | Advanced Calculator")
        self.root.geometry("1000x680")
        self.root.minsize(900, 620)
        self.root.configure(bg="#0F172A")

        # Data
        self.expression = ""
        self.memory = 0
        self.history = []

        # Build application
        self.create_interface()
        self.bind_keyboard()

    # ===================================================
    # CREATE INTERFACE
    # ===================================================

    def create_interface(self):

        # ---------------- HEADER ----------------

        header = tk.Frame(
            self.root,
            bg="#0F172A"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(20, 5)
        )

        tk.Label(
            header,
            text="CalcPro",
            bg="#0F172A",
            fg="#F8FAFC",
            font=("Segoe UI", 28, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text="ADVANCED CALCULATOR",
            bg="#0F172A",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(
            side="left",
            padx=15,
            pady=12
        )

        # ---------------- MAIN CONTAINER ----------------

        main = tk.Frame(
            self.root,
            bg="#0F172A"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        # ================================================
        # LEFT CALCULATOR
        # ================================================

        calculator = tk.Frame(
            main,
            bg="#0F172A"
        )

        calculator.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ---------------- DISPLAY ----------------

        display_frame = tk.Frame(
            calculator,
            bg="#1E293B"
        )

        display_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.display = tk.Entry(
            display_frame,
            bg="#1E293B",
            fg="#F8FAFC",
            insertbackground="#F8FAFC",
            font=("Segoe UI", 30, "bold"),
            justify="right",
            bd=0,
            relief="flat"
        )

        self.display.pack(
            fill="x",
            padx=20,
            pady=(25, 5),
            ipady=10
        )

        # Prevent typing directly into display
        self.display.bind(
            "<Key>",
            lambda event: "break"
        )

        self.status = tk.Label(
            display_frame,
            text="Ready",
            bg="#1E293B",
            fg="#94A3B8",
            anchor="e",
            font=("Segoe UI", 9)
        )

        self.status.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # ================================================
        # MEMORY BUTTONS
        # ================================================

        memory_frame = tk.Frame(
            calculator,
            bg="#0F172A"
        )

        memory_frame.pack(
            fill="x",
            pady=(0, 8)
        )

        self.make_button(
            memory_frame,
            "MC",
            self.memory_clear,
            "#64748B"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=3,
            ipady=7
        )

        self.make_button(
            memory_frame,
            "MR",
            self.memory_recall,
            "#64748B"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=3,
            ipady=7
        )

        self.make_button(
            memory_frame,
            "M+",
            self.memory_add,
            "#64748B"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=3,
            ipady=7
        )

        self.make_button(
            memory_frame,
            "M-",
            self.memory_subtract,
            "#64748B"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=3,
            ipady=7
        )

        # =================================================
        # CALCULATOR BUTTONS
        # =================================================

        buttons_frame = tk.Frame(
            calculator,
            bg="#0F172A"
        )

        buttons_frame.pack(
            fill="both",
            expand=True
        )

        for row in range(5):
            buttons_frame.grid_rowconfigure(
                row,
                weight=1
            )

        for column in range(5):
            buttons_frame.grid_columnconfigure(
                column,
                weight=1
            )

        buttons = [

            # Row 1
            [
                ("C", self.clear, "#DC2626"),
                ("⌫", self.backspace, "#64748B"),
                ("(", lambda: self.add("("), "#64748B"),
                (")", lambda: self.add(")"), "#64748B"),
                ("÷", lambda: self.add("/"), "#2563EB")
            ],

            # Row 2
            [
                ("7", lambda: self.add("7"), "#334155"),
                ("8", lambda: self.add("8"), "#334155"),
                ("9", lambda: self.add("9"), "#334155"),
                ("%", self.percentage, "#2563EB"),
                ("×", lambda: self.add("*"), "#2563EB")
            ],

            # Row 3
            [
                ("4", lambda: self.add("4"), "#334155"),
                ("5", lambda: self.add("5"), "#334155"),
                ("6", lambda: self.add("6"), "#334155"),
                ("√", self.square_root, "#2563EB"),
                ("−", lambda: self.add("-"), "#2563EB")
            ],

            # Row 4
            [
                ("1", lambda: self.add("1"), "#334155"),
                ("2", lambda: self.add("2"), "#334155"),
                ("3", lambda: self.add("3"), "#334155"),
                ("x²", self.square, "#2563EB"),
                ("+", lambda: self.add("+"), "#2563EB")
            ],

            # Row 5
            [
                ("±", self.change_sign, "#64748B"),
                ("0", lambda: self.add("0"), "#334155"),
                (".", lambda: self.add("."), "#334155"),
                ("=", self.calculate, "#16A34A"),
                ("AC", self.clear, "#DC2626")
            ]
        ]

        for row_number, row in enumerate(buttons):

            for column_number, data in enumerate(row):

                text = data[0]
                command = data[1]
                color = data[2]

                btn = self.make_button(
                    buttons_frame,
                    text,
                    command,
                    color
                )

                btn.grid(
                    row=row_number,
                    column=column_number,
                    padx=4,
                    pady=4,
                    sticky="nsew"
                )

        # =================================================
        # HISTORY PANEL
        # =================================================

        history_panel = tk.Frame(
            main,
            bg="#111827",
            width=270,
            highlightbackground="#334155",
            highlightthickness=1
        )

        history_panel.pack(
            side="right",
            fill="y",
            padx=(20, 0)
        )

        history_panel.pack_propagate(False)

        tk.Label(
            history_panel,
            text="CALCULATION HISTORY",
            bg="#111827",
            fg="#F8FAFC",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 3)
        )

        tk.Label(
            history_panel,
            text="Recent calculations",
            bg="#111827",
            fg="#94A3B8",
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

        self.history_box = tk.Listbox(
            history_panel,
            bg="#111827",
            fg="#CBD5E1",
            selectbackground="#2563EB",
            selectforeground="#FFFFFF",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 9)
        )

        self.history_box.pack(
            fill="both",
            expand=True,
            padx=12
        )

        tk.Button(
            history_panel,
            text="Clear History",
            command=self.clear_history,
            bg="#DC2626",
            fg="#FFFFFF",
            activebackground="#B91C1C",
            activeforeground="#FFFFFF",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            fill="x",
            padx=12,
            pady=12,
            ipady=7
        )

        # ---------------- FOOTER ----------------

        tk.Label(
            self.root,
            text="CalcPro  •  Python + Tkinter  •  Keyboard Supported",
            bg="#0F172A",
            fg="#64748B",
            font=("Segoe UI", 8)
        ).pack(
            pady=(0, 12)
        )

    # =====================================================
    # BUTTON CREATOR
    # =====================================================

    def make_button(
        self,
        parent,
        text,
        command,
        color
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="#FFFFFF",
            activebackground="#475569",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 13, "bold"),
            bd=0,
            relief="flat",
            cursor="hand2"
        )

    # =====================================================
    # DISPLAY
    # =====================================================

    def refresh_display(self):

        self.display.delete(
            0,
            tk.END
        )

        self.display.insert(
            0,
            self.expression
        )

        self.display.icursor(
            tk.END
        )

    # =====================================================
    # ADD
    # =====================================================

    def add(self, value):

        self.expression += value

        self.refresh_display()

        self.status.config(
            text="Calculating..."
        )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.expression = ""

        self.refresh_display()

        self.status.config(
            text="Ready"
        )

    # =====================================================
    # BACKSPACE
    # =====================================================

    def backspace(self):

        self.expression = self.expression[:-1]

        self.refresh_display()

    # =====================================================
    # SAFE CALCULATOR
    # =====================================================

    def safe_eval(self, expression):

        node = ast.parse(
            expression,
            mode="eval"
        )

        return self.evaluate_node(
            node.body
        )

    def evaluate_node(self, node):

        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv
        }

        # Number
        if isinstance(
            node,
            ast.Constant
        ):

            if isinstance(
                node.value,
                (int, float)
            ):

                return node.value

            raise ValueError

        # Positive / negative number
        if isinstance(
            node,
            ast.UnaryOp
        ):

            value = self.evaluate_node(
                node.operand
            )

            if isinstance(
                node.op,
                ast.USub
            ):

                return -value

            if isinstance(
                node.op,
                ast.UAdd
            ):

                return value

            raise ValueError

        # Mathematical operation
        if isinstance(
            node,
            ast.BinOp
        ):

            left = self.evaluate_node(
                node.left
            )

            right = self.evaluate_node(
                node.right
            )

            operation = operations.get(
                type(node.op)
            )

            if operation is None:

                raise ValueError

            return operation(
                left,
                right
            )

        raise ValueError

    # =====================================================
    # CALCULATE
    # =====================================================

    def calculate(self):

        if not self.expression:
            return

        try:

            original = self.expression

            result = self.safe_eval(
                original
            )

            if (
                isinstance(result, float)
                and result.is_integer()
            ):

                result = int(result)

            history_item = (
                f"{original} = {result}"
            )

            self.history.append(
                history_item
            )

            self.expression = str(
                result
            )

            self.refresh_display()

            self.update_history()

            self.status.config(
                text="Calculation completed"
            )

        except ZeroDivisionError:

            messagebox.showerror(
                "Calculation Error",
                "Division by zero is not allowed."
            )

            self.status.config(
                text="Error"
            )

        except Exception:

            messagebox.showerror(
                "Calculation Error",
                "Please enter a valid expression."
            )

            self.status.config(
                text="Invalid expression"
            )

    # =====================================================
    # SQUARE
    # =====================================================

    def square(self):

        try:

            value = self.safe_eval(
                self.expression
            )

            result = value ** 2

            self.history.append(
                f"({value})² = {result}"
            )

            self.expression = str(
                result
            )

            self.refresh_display()

            self.update_history()

        except:

            messagebox.showerror(
                "Error",
                "Enter a valid number."
            )

    # =====================================================
    # SQUARE ROOT
    # =====================================================

    def square_root(self):

        try:

            value = self.safe_eval(
                self.expression
            )

            if value < 0:

                raise ValueError

            result = math.sqrt(
                value
            )

            self.history.append(
                f"√{value} = {result}"
            )

            self.expression = str(
                result
            )

            self.refresh_display()

            self.update_history()

        except:

            messagebox.showerror(
                "Error",
                "Square root requires a non-negative number."
            )

    # =====================================================
    # PERCENTAGE
    # =====================================================

    def percentage(self):

        try:

            value = self.safe_eval(
                self.expression
            )

            result = value / 100

            self.history.append(
                f"{value}% = {result}"
            )

            self.expression = str(
                result
            )

            self.refresh_display()

            self.update_history()

        except:

            messagebox.showerror(
                "Error",
                "Enter a valid number."
            )

    # =====================================================
    # CHANGE SIGN
    # =====================================================

    def change_sign(self):

        try:

            value = self.safe_eval(
                self.expression
            )

            self.expression = str(
                -value
            )

            self.refresh_display()

        except:

            messagebox.showerror(
                "Error",
                "Enter a valid number."
            )

    # =====================================================
    # MEMORY CLEAR
    # =====================================================

    def memory_clear(self):

        self.memory = 0

        self.status.config(
            text="Memory cleared"
        )

    # =====================================================
    # MEMORY RECALL
    # =====================================================

    def memory_recall(self):

        self.expression = str(
            self.memory
        )

        self.refresh_display()

        self.status.config(
            text="Memory recalled"
        )

    # =====================================================
    # MEMORY ADD
    # =====================================================

    def memory_add(self):

        try:

            value = self.safe_eval(
                self.expression
            )

            self.memory += value

            self.status.config(
                text=f"Memory: {self.memory}"
            )

        except:

            messagebox.showerror(
                "Error",
                "Invalid value."
            )

    # =====================================================
    # MEMORY SUBTRACT
    # =====================================================

    def memory_subtract(self):

        try:

            value = self.safe_eval(
                self.expression
            )

            self.memory -= value

            self.status.config(
                text=f"Memory: {self.memory}"
            )

        except:

            messagebox.showerror(
                "Error",
                "Invalid value."
            )

    # =====================================================
    # HISTORY
    # =====================================================

    def update_history(self):

        self.history_box.delete(
            0,
            tk.END
        )

        for item in reversed(
            self.history[-15:]
        ):

            self.history_box.insert(
                tk.END,
                item
            )

    def clear_history(self):

        self.history.clear()

        self.history_box.delete(
            0,
            tk.END
        )

        self.status.config(
            text="History cleared"
        )

    # =====================================================
    # KEYBOARD
    # =====================================================

    def bind_keyboard(self):

        self.root.bind(
            "<Key>",
            self.keyboard_handler
        )

    def keyboard_handler(self, event):

        key = event.keysym
        char = event.char

        if char in "0123456789.+-*/()":

            self.add(char)

        elif key == "Return":

            self.calculate()

        elif key == "BackSpace":

            self.backspace()

        elif key == "Escape":

            self.clear()

        elif char == "%":

            self.percentage()


# ========================================================
# START PROGRAM
# ========================================================

root = tk.Tk()

app = CalcPro(root)

root.mainloop()
