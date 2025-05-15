
import tkinter as tk
from tkinter import font as tkfont
import re
from math import isfinite
from datetime import datetime

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Vishwa's Ultimate Calculator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # Initialize variables
        self.current_input = tk.StringVar()
        self.current_input.set("0")
        self.history = []
        self.memory = 0.0
        self.dark_mode = False
        self.history_visible = True

        # Define fonts
        self.display_font = tkfont.Font(family="Arial", size=28, weight="bold")
        self.button_font = tkfont.Font(family="Arial", size=14)
        self.history_font = tkfont.Font(family="Arial", size=11)

        # Set initial theme
        self.set_theme()

        # Create UI elements
        self.create_widgets()

        # Bind keyboard events
        self.root.bind('<Key>', self.handle_keypress)

    def set_theme(self):
        """Set the color scheme based on current theme mode"""
        if self.dark_mode:
            self.bg_color = "#1c2526"
            self.display_bg = "#2e3537"
            self.display_fg = "#e0e6e8"
            self.button_bg = "#3a4345"
            self.button_fg = "#e0e6e8"
            self.button_active_bg = "#4e5a5d"
            self.button_active_fg = "#e0e6e8"
            self.operator_bg = "#ff6f61"
            self.operator_fg = "#ffffff"
            self.operator_active_bg = "#ff8a80"
            self.special_bg = "#6b7280"
            self.special_fg = "#ffffff"
            self.special_active_bg = "#8b95a1"
            self.history_bg = "#2e3537"
            self.history_fg = "#c4cdd5"
            self.history_disabled_bg = "#2e3537"
        else:
            self.bg_color = "#f3f4f6"
            self.display_bg = "#ffffff"
            self.display_fg = "#111827"
            self.button_bg = "#e5e7eb"
            self.button_fg = "#111827"
            self.button_active_bg = "#d1d5db"
            self.button_active_fg = "#111827"
            self.operator_bg = "#ff6f61"
            self.operator_fg = "#ffffff"
            self.operator_active_bg = "#ff8a80"
            self.special_bg = "#9ca3af"
            self.special_fg = "#111827"
            self.special_active_bg = "#b9c1cc"
            self.history_bg = "#ffffff"
            self.history_fg = "#374151"
            self.history_disabled_bg = "#f9fafb"

    def create_widgets(self):
        """Create all the widgets for the calculator"""
        self.root.config(bg=self.bg_color)

        # Create main frames
        self.display_frame = tk.Frame(self.root, bg=self.bg_color)
        self.display_frame.pack(pady=(15, 10), padx=15, fill=tk.X)

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

        # Create display
        self.display = tk.Entry(
            self.display_frame,
            textvariable=self.current_input,
            font=self.display_font,
            bg=self.display_bg,
            fg=self.display_fg,
            borderwidth=0,
            relief=tk.FLAT,
            justify=tk.RIGHT,
            insertwidth=0,
            readonlybackground=self.display_bg,
            state='readonly'
        )
        self.display.pack(fill=tk.X, ipady=12)

        # Create control buttons frame
        self.control_frame = tk.Frame(self.display_frame, bg=self.bg_color)
        self.control_frame.pack(fill=tk.X, pady=(5, 0))

        # Create theme toggle button
        self.theme_btn = tk.Button(
            self.control_frame,
            text="☀️" if self.dark_mode else "🌙",
            command=self.toggle_theme,
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg,
            borderwidth=0,
            font=self.button_font,
            width=4,
            relief="flat"
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Create history toggle button
        self.history_btn = tk.Button(
            self.control_frame,
            text="Hide History" if self.history_visible else "Show History",
            command=self.toggle_history,
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg,
            borderwidth=0,
            font=self.button_font,
            relief="flat"
        )
        self.history_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Create clear history button
        self.clear_history_btn = tk.Button(
            self.control_frame,
            text="Clear Hist",
            command=self.clear_history,
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg,
            borderwidth=0,
            font=self.button_font,
            relief="flat"
        )
        self.clear_history_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Create history frame
        self.history_frame = tk.Frame(self.root, bg=self.history_bg, relief=tk.RIDGE, borderwidth=1)
        self.history_label = tk.Label(
            self.history_frame,
            text="Calculation History",
            bg=self.history_bg,
            fg=self.history_fg,
            font=self.button_font
        )
        self.history_label.pack(pady=(5, 2))

        self.history_text = tk.Text(
            self.history_frame,
            bg=self.history_disabled_bg,
            fg=self.history_fg,
            font=self.history_font,
            state=tk.DISABLED,
            wrap=tk.WORD,
            height=8,
            padx=8,
            pady=8,
            borderwidth=0
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_text.configure(yscrollcommand=scrollbar.set)

        # Create calculator buttons
        buttons = [
            ('M+', 0, 0), ('M-', 0, 1), ('MR', 0, 2), ('MC', 0, 3), ('⌫', 0, 4),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('C', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('', 4, 4)
        ]

        for (text, row, col) in buttons:
            if not text:
                continue
            btn = tk.Button(
                self.button_frame,
                text=text,
                command=lambda t=text: self.on_button_click(t),
                bg=self.get_button_bg(text),
                fg=self.get_button_fg(text),
                activebackground=self.get_button_active_bg(text),
                activeforeground=self.get_button_fg(text),
                font=self.button_font,
                borderwidth=0,
                width=4,
                height=2,
                relief="flat"
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_button_hover_leave(e, b))

        # Configure grid weights
        for i in range(5):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)

        # Position history
        self.position_history()

    def position_history(self):
        """Position the history frame based on visibility"""
        if self.history_visible:
            self.button_frame.pack_forget()
            self.history_frame.pack_forget()
            self.main_frame = tk.Frame(self.root, bg=self.bg_color)
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
            self.button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.history_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        else:
            if hasattr(self, 'main_frame'):
                self.main_frame.pack_forget()
            self.history_frame.pack_forget()
            self.button_frame.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

    def get_button_bg(self, text):
        """Get background color based on button type"""
        if text in {'+', '-', '*', '/', '='}:
            return self.operator_bg
        elif text in {'C', '⌫', 'M+', 'M-', 'MR', 'MC'}:
            return self.special_bg
        else:
            return self.button_bg

    def get_button_fg(self, text):
        """Get foreground color based on button type"""
        if text in {'+', '-', '*', '/', '='}:
            return self.operator_fg
        elif text in {'C', '⌫', 'M+', 'M-', 'MR', 'MC'}:
            return self.special_fg
        else:
            return self.button_fg

    def get_button_active_bg(self, text):
        """Get active background color based on button type"""
        if text in {'+', '-', '*', '/', '='}:
            return self.operator_active_bg
        elif text in {'C', '⌫', 'M+', 'M-', 'MR', 'MC'}:
            return self.special_active_bg
        else:
            return self.button_active_bg

    def on_button_hover(self, event, button):
        """Handle button hover effect"""
        button.config(relief="raised")

    def on_button_hover_leave(self, event, button):
        """Handle button hover leave effect"""
        button.config(relief="flat")

    def on_button_click(self, text):
        """Handle button clicks"""
        if text in {'M+', 'M-', 'MR', 'MC'}:
            self.handle_memory(text)
            return
        current = self.current_input.get()
        if text.isdigit() or text == '.':
            if current == '0' or current == 'Error':
                self.current_input.set(text)
            else:
                self.current_input.set(current + text)
        elif text in {'+', '-', '*', '/'}:
            if current == 'Error':
                self.current_input.set('0' + text)
            else:
                self.current_input.set(current + text)
        elif text == '⌫':
            if current == 'Error':
                self.current_input.set('0')
            else:
                self.current_input.set(current[:-1] if len(current) > 1 else '0')
        elif text == 'C':
            self.current_input.set('0')
        elif text == '=':
            self.calculate()

    def handle_memory(self, operation):
        """Handle memory operations"""
        try:
            current = float(self.current_input.get())
            if operation == 'M+':
                self.memory += current
            elif operation == 'M-':
                self.memory -= current
            elif operation == 'MR':
                self.current_input.set(str(self.memory))
            elif operation == 'MC':
                self.memory = 0.0
        except ValueError:
            self.current_input.set("Error")

    def calculate(self):
        """Evaluate the expression and display result"""
        expression = self.current_input.get()
        try:
            expression = expression.replace('×', '*').replace('÷', '/')
            if not re.match(r'^[\d+\-*/. ]+$', expression):
                raise ValueError("Invalid characters in expression")
            result = eval(expression, {'__builtins__': None}, {})
            if not isfinite(result):
                raise ValueError("Result is not finite")
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            self.current_input.set(str(result))
            self.add_to_history(expression, str(result))
        except Exception:
            self.current_input.set('Error')

    def add_to_history(self, expression, result):
        """Add calculation to history"""
        entry = f"{datetime.now().strftime('%H:%M:%S')}: {expression} = {result}"
        self.history.insert(0, entry)
        if len(self.history) > 10:
            self.history = self.history[:10]
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, '\n'.join(self.history))
        self.history_text.config(state=tk.DISABLED)

    def clear_history(self):
        """Clear the history"""
        self.history = []
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.theme_btn.config(text="☀️" if self.dark_mode else "🌙")
        self.update_theme_colors()

    def update_theme_colors(self):
        """Update all widget colors based on current theme"""
        self.root.config(bg=self.bg_color)
        self.display.config(bg=self.display_bg, fg=self.display_fg, readonlybackground=self.display_bg)
        self.display_frame.config(bg=self.bg_color)
        self.button_frame.config(bg=self.bg_color)
        if hasattr(self, 'main_frame'):
            self.main_frame.config(bg=self.bg_color)
        self.history_frame.config(bg=self.history_bg)
        self.history_label.config(bg=self.history_bg, fg=self.history_fg)
        self.history_text.config(bg=self.history_disabled_bg, fg=self.history_fg)
        self.theme_btn.config(
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg
        )
        self.history_btn.config(
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg
        )
        self.clear_history_btn.config(
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg
        )
        for child in self.button_frame.winfo_children():
            if isinstance(child, tk.Button):
                text = child.cget('text')
                child.config(
                    bg=self.get_button_bg(text),
                    fg=self.get_button_fg(text),
                    activebackground=self.get_button_active_bg(text),
                    activeforeground=self.get_button_fg(text)
                )

    def toggle_history(self):
        """Toggle history panel visibility"""
        self.history_visible = not self.history_visible
        self.history_btn.config(text="Hide History" if self.history_visible else "Show History")
        self.position_history()

    def handle_keypress(self, event):
        """Handle keyboard input"""
        key = event.char
        keysym = event.keysym
        if key.isdigit() or key in '+-*/.':
            self.on_button_click(key)
        elif keysym == 'Return':
            self.on_button_click('=')
        elif keysym == 'BackSpace':
            self.on_button_click('⌫')
        elif keysym == 'Escape':
            self.on_button_click('C')

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
