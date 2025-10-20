import tkinter as tk
from tkinter import PhotoImage
from chatbot import get_response


class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Matrix Chat")
        self.geometry("1000x700")
        self.configure(bg="black")

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = PhotoImage(file="japanese-neon.png")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.chat_panel = tk.Frame(self, bg="black")

        self.scrollbar = tk.Scrollbar(self.chat_panel)
        self.scrollbar.pack(side="right", fill="y")

        self.output_section = tk.Text(
            self.chat_panel,
            fg="#008529",
            bg="black",
            width=100,
            height=25,
            wrap="word",
            yscrollcommand=self.scrollbar.set,
            state="disabled"
        )
        self.output_section.pack(pady=(10, 5))
        self.scrollbar.config(command=self.output_section.yview)

        self.bottom_frame = tk.Frame(self.chat_panel, bg="black")

        self.input_section = tk.Text(
            self.bottom_frame,
            width=79,
            height=5,
            bg="black",
            fg="#008529"
        )
        self.input_section.grid(row=0, column=0, padx=5, pady=5)

        self.button = tk.Button(
            self.bottom_frame,
            text="Ask",
            width=5,
            height=2,
            bg="black",
            fg="#008529",
            command=self.on_submit
        )
        self.button.grid(row=0, column=1, padx=5, pady=5)

        self.bottom_frame.pack(pady=(0, 10))

        self.chat_panel_id = self.canvas.create_window(0, 0, window=self.chat_panel)
        self.canvas.bind("<Configure>", self.center_widgets)

    def center_widgets(self, event=None):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.coords(self.chat_panel_id, width / 2, height / 2)

    def on_submit(self):
        user_input = self.input_section.get("1.0", tk.END).strip()
        if user_input:
            self.display_output(f"You: {user_input}\n", "user")
            response = get_response(user_input)
            self.display_output(f"Bot: {response}\n\n", "bot")
            self.input_section.delete("1.0", tk.END)

    def display_output(self, text, tag):
        self.output_section.config(state="normal")
        self.output_section.insert(tk.END, text, tag)
        self.output_section.config(state="disabled")
        self.output_section.see(tk.END)





