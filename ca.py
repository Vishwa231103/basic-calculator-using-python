import tkinter as tk
from tkinter import font as tkfont
import re
from math import isfinite

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("vishwa's Calculator")
        self.root.geometry("480x500")
        self.root.resizable(False, False)
        
        # Initialize variables
        self.current_input = tk.StringVar()
        self.current_input.set("0")
        self.history = []
        self.dark_mode = False
        self.history_visible = True
        
        # Define fonts
        self.display_font = tkfont.Font(size=24, weight="bold")
        self.button_font = tkfont.Font(size=12)
        self.history_font = tkfont.Font(size=10)
        
        # Set initial colors
        self.set_theme()
        
        # Create UI elements
        self.create_widgets()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.handle_keypress)
        
    def set_theme(self):
        """Set the color scheme based on current theme mode"""
        if self.dark_mode:
            # Dark theme colors
            self.bg_color = "#2d2d2d"
            self.display_bg = "#3d3d3d"
            self.display_fg = "#ffffff"
            self.button_bg = "#4d4d4d"
            self.button_fg = "#ffffff"
            self.button_active_bg = "#5d5d5d"
            self.button_active_fg = "#ffffff"
            self.operator_bg = "#ff9500"
            self.operator_fg = "#ffffff"
            self.operator_active_bg = "#ffaa33"
            self.special_bg = "#a6a6a6"
            self.special_fg = "#000000"
            self.special_active_bg = "#bfbfbf"
            self.history_bg = "#3d3d3d"
            self.history_fg = "#ffffff"
            self.history_disabled_bg = "#3d3d3d"
        else:
            # Light theme colors
            self.bg_color = "#f0f0f0"
            self.display_bg = "#ffffff"
            self.display_fg = "#000000"
            self.button_bg = "#e0e0e0"
            self.button_fg = "#000000"
            self.button_active_bg = "#d0d0d0"
            self.button_active_fg = "#000000"
            self.operator_bg = "#ff9500"
            self.operator_fg = "#ffffff"
            self.operator_active_bg = "#ffaa33"
            self.special_bg = "#a6a6a6"
            self.special_fg = "#000000"
            self.special_active_bg = "#bfbfbf"
            self.history_bg = "#ffffff"
            self.history_fg = "#000000"
            self.history_disabled_bg = "#f0f0f0"
    
    def create_widgets(self):
        """Create all the widgets for the calculator"""
        # Configure root window background
        self.root.config(bg=self.bg_color)
        
        # Create main frames
        self.display_frame = tk.Frame(self.root, bg=self.bg_color)
        self.display_frame.pack(pady=(10, 5), padx=10, fill=tk.X)
        
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
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
        self.display.pack(fill=tk.X, ipady=10)
        
        # Create theme toggle button
        self.theme_btn = tk.Button(
            self.display_frame,
            text="☀️" if self.dark_mode else "🌙",
            command=self.toggle_theme,
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg,
            borderwidth=0,
            font=self.button_font,
            width=3,
            height=1
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Create history frame
        self.history_frame = tk.Frame(
            self.root,
            bg=self.history_bg,
            width=150,
            relief=tk.RIDGE,
            borderwidth=1
        )
        
        self.history_label = tk.Label(
            self.history_frame,
            text="History",
            bg=self.history_bg,
            fg=self.history_fg,
            font=self.button_font
        )
        self.history_label.pack(pady=(5, 0))
        
        self.history_text = tk.Text(
            self.history_frame,
            bg=self.history_disabled_bg,
            fg=self.history_fg,
            font=self.history_font,
            state=tk.DISABLED,
            wrap=tk.WORD,
            height=20,
            padx=5,
            pady=5,
            borderwidth=0
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Create history toggle button
        self.history_btn = tk.Button(
            self.button_frame,
            text="Hide History" if self.history_visible else "Show History",
            command=self.toggle_history,
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg,
            borderwidth=0,
            font=self.button_font
        )
        self.history_btn.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        # Create calculator buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('⌫', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('C', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('', 4, 4)
        ]
        
        for (text, row, col) in buttons:
            if not text:
                continue  # Skip empty buttons
                
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
                height=2
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Bind hover effects
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_button_hover_leave(e, b))
        
        # Configure grid weights
        for i in range(5):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_rowconfigure(i + 1, weight=1)
        
        # Position history frame
        self.position_history()
    
    def position_history(self):
        """Position the history frame based on visibility"""
        if self.history_visible:
            self.button_frame.pack_forget()
            self.history_frame.pack_forget()
            
            # Create a container frame for side-by-side layout
            self.main_frame = tk.Frame(self.root, bg=self.bg_color)
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Calculator buttons on the left
            self.button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # History on the right
            self.history_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        else:
            if hasattr(self, 'main_frame'):
                self.main_frame.pack_forget()
            self.history_frame.pack_forget()
            self.button_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
    
    def get_button_bg(self, text):
        """Get background color based on button type"""
        if text in {'+', '-', '*', '/', '='}:
            return self.operator_bg
        elif text in {'C', '⌫'}:
            return self.special_bg
        else:
            return self.button_bg
    
    def get_button_fg(self, text):
        """Get foreground color based on button type"""
        if text in {'+', '-', '*', '/', '='}:
            return self.operator_fg
        elif text in {'C', '⌫'}:
            return self.special_fg
        else:
            return self.button_fg
    
    def get_button_active_bg(self, text):
        """Get active background color based on button type"""
        if text in {'+', '-', '*', '/', '='}:
            return self.operator_active_bg
        elif text in {'C', '⌫'}:
            return self.special_active_bg
        else:
            return self.button_active_bg
    
    def on_button_hover(self, event, button):
        """Handle button hover effect"""
        text = button.cget('text')
        if text not in {'+', '-', '*', '/', '=', 'C', '⌫'}:
            button.config(bg=self.button_active_bg)
    
    def on_button_hover_leave(self, event, button):
        """Handle button hover leave effect"""
        text = button.cget('text')
        button.config(bg=self.get_button_bg(text))
    
    def on_button_click(self, text):
        """Handle button clicks"""
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
    
    def calculate(self):
        """Evaluate the expression and display result"""
        expression = self.current_input.get()
        
        try:
            # Replace × with * and ÷ with / for evaluation
            expression = expression.replace('×', '*').replace('÷', '/')
            
            # Validate expression
            if not re.match(r'^[\d+\-*/. ]+$', expression):
                raise ValueError("Invalid characters in expression")
            
            # Evaluate safely
            result = eval(expression, {'__builtins__': None}, {})
            
            # Check if result is finite (not inf or nan)
            if not isfinite(result):
                raise ValueError("Result is not finite")
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    # Limit to 10 decimal places
                    result = round(result, 10)
            
            # Update display and history
            self.current_input.set(str(result))
            self.add_to_history(expression, str(result))
        except Exception as e:
            self.current_input.set('Error')
    
    def add_to_history(self, expression, result):
        """Add calculation to history"""
        entry = f"{expression} = {result}"
        self.history.insert(0, entry)
        
        # Keep only last 10 entries
        if len(self.history) > 10:
            self.history = self.history[:10]
        
        # Update history display
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, '\n'.join(self.history))
        self.history_text.config(state=tk.DISABLED)
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.theme_btn.config(text="☀️" if self.dark_mode else "🌙")
        self.update_theme_colors()
    
    def update_theme_colors(self):
        """Update all widget colors based on current theme"""
        # Update root window
        self.root.config(bg=self.bg_color)
        
        # Update display
        self.display.config(
            bg=self.display_bg,
            fg=self.display_fg,
            readonlybackground=self.display_bg
        )
        
        # Update frames
        self.display_frame.config(bg=self.bg_color)
        self.button_frame.config(bg=self.bg_color)
        if hasattr(self, 'main_frame'):
            self.main_frame.config(bg=self.bg_color)
        
        # Update history frame
        self.history_frame.config(bg=self.history_bg)
        self.history_label.config(bg=self.history_bg, fg=self.history_fg)
        self.history_text.config(
            bg=self.history_disabled_bg,
            fg=self.history_fg
        )
        
        # Update theme button
        self.theme_btn.config(
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg
        )
        
        # Update history toggle button
        self.history_btn.config(
            bg=self.special_bg,
            fg=self.special_fg,
            activebackground=self.special_active_bg,
            activeforeground=self.special_fg
        )
        
        # Update all calculator buttons
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
        elif keysym == 'Left':
            # Move cursor left (not implemented as display is readonly)
            pass
        elif keysym == 'Right':
            # Move cursor right (not implemented as display is readonly)
            pass

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()