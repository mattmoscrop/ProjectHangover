import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import threading
import subprocess
from tkinter import ttk
import openai

# Set up OpenAI GPT API credentials
openai.api_key = 'Add Your Open AI API Here'

class NmapGPTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nmap GPT GUI")
        self.root.configure(bg="#333333")  # Set background color of the root window

        # Set the title color to green
        self.root.option_add('*Dialog.msg.font', 'Helvetica 14 bold')
        self.root.option_add('*Dialog.msg.foreground', 'green')

        # Set font size
        font_size = ("Helvetica", 14)

        # Top Widget
        self.top_frame = tk.Frame(self.root, bg='black')
        self.top_frame.grid(row=0, column=0, sticky="ew")

        self.user_label_gpt = tk.Label(self.top_frame, text="You: ", bg='black', fg='green', font=font_size)
        self.user_label_gpt.pack(side=tk.LEFT)

        self.entry_field_gpt = tk.Entry(self.top_frame, bg='black', fg='green', insertbackground='green', font=font_size)
        self.entry_field_gpt.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.entry_field_gpt.bind("<Return>", self.generate_instructions)
        self.entry_field_gpt.bind("<KP_Enter>", self.generate_instructions)

        self.text_area_gpt = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg='black', fg='green', insertbackground='green', font=font_size)
        self.text_area_gpt.grid(row=1, column=0, sticky="nsew")

        self.reply_button_gpt = tk.Button(self.root, text="Reply to Morpheus", command=self.generate_instructions, bg='black', fg='green', font=font_size)
        self.reply_button_gpt.grid(row=2, column=0, pady=10)

        self.clear_button_gpt = tk.Button(self.root, text="Clear GPT Text", command=self.clear_gpt_text, bg='black', fg='green', font=font_size)
        self.clear_button_gpt.grid(row=3, column=0, pady=10)

        # Separator
        self.separator = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.separator.grid(row=4, column=0, sticky="ew", pady=10)

        # Bottom Widget
        self.bottom_frame = tk.Frame(self.root, bg='black')
        self.bottom_frame.grid(row=5, column=0, sticky="ew")

        self.nmap_label = tk.Label(self.bottom_frame, text="Nmap: ", bg='black', fg='green', font=font_size)
        self.nmap_label.pack(side=tk.LEFT)

        # Define a list of pre-populated nmap commands
        self.nmap_commands = [
            'nmap -sS', # SYN scan
            'nmap -sV', # Version scan
            'nmap -sP', # Ping scan
            'nmap -sT', # TCP connect scan
            'nmap -A',  # All-ports scan
            'nmap -O',  # OS detection scan
            'nmap -v',  # Verbose scan
            'nmap -p',  # Port scan
            'nmap -iL', # Read hosts/IPs from file
            'nmap -iR'  # Scan IP range
        ]

        # Define a StringVar variable to hold the selected command
        self.selected_command = tk.StringVar(self.root)
        self.selected_command.set(self.nmap_commands[0])  # set the default option

        # Entry field to edit the command
        self.entry_field_nmap = tk.Entry(self.bottom_frame, bg='black', fg='green', insertbackground='green', font=font_size)
        self.entry_field_nmap.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.entry_field_nmap.bind("<Return>", self.run_nmap_command)
        self.entry_field_nmap.bind("<KP_Enter>", self.run_nmap_command)

        self.entry_field_nmap.insert(0, self.nmap_commands[0])  # Populate the entry field with the first command

        self.dropdown_nmap = tk.OptionMenu(self.bottom_frame, self.selected_command, *self.nmap_commands, command=self.update_entry)
        self.dropdown_nmap.config(bg='black', fg='green')
        self.dropdown_nmap["menu"].config(bg='black', fg='green')
        self.dropdown_nmap.pack(fill=tk.X, side=tk.LEFT)

        # Create text_area_nmap BEFORE creating reply_button_nmap
        self.text_area_nmap = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg='black', fg='green', insertbackground='green', font=font_size)
        self.text_area_nmap.grid(row=6, column=0, sticky="nsew")

        self.reply_button_nmap = tk.Button(self.root, text="Run Nmap Command", command=self.run_nmap_command, bg='black', fg='green', font=font_size)
        self.reply_button_nmap.grid(row=7, column=0, pady=10)

        self.clear_button_nmap = tk.Button(self.root, text="Clear Nmap Text", command=self.clear_nmap_text, bg='black', fg='green', font=font_size)
        self.clear_button_nmap.grid(row=8, column=0, pady=10)

        # Start the instruction process
        self.text_area_gpt.insert(tk.END, 'Morpheus: Hello Neo. How can I help you with Nmap?')

        # Configure resizing behavior
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def clear_gpt_text(self):
        self.text_area_gpt.delete('1.0', tk.END)

    def clear_nmap_text(self):
        self.text_area_nmap.delete('1.0', tk.END)

    def update_entry(self, value):
        # This function updates the entry field when a command is selected from the dropdown
        self.entry_field_nmap.delete(0, tk.END)  # Remove the current command
        self.entry_field_nmap.insert(0, value)  # Insert the selected command

    def run_nmap_command(self, event=None):
        command = self.entry_field_nmap.get()  # Get the command from the entry field instead of the dropdown
        self.text_area_nmap.insert(tk.END, f"\nMorpheus: Running command: {command}\n")

        try:
            output = subprocess.check_output(command, shell=True).decode()
            self.text_area_nmap.insert(tk.END, f"Morpheus: {output}\n")
        except Exception as e:
            self.text_area_nmap.insert(tk.END, f"\nMorpheus: Error: {str(e)}\n")

        self.entry_field_nmap.delete(0, tk.END)

    def generate_instructions(self, event=None):
        input_text = self.entry_field_gpt.get()
        self.text_area_gpt.insert(tk.END, f"\nYou: {input_text}\n")

        # Start a new thread to generate the instructions.
        threading.Thread(target=self.generate_instructions_thread, args=(input_text,)).start()

    def generate_instructions_thread(self, input_text):
        try:
            messages = [
                {"role": "system", "content": "You are Morpheus, a helpful assistant."},
                {"role": "user", "content": input_text}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=200
            )

            generated_text = response['choices'][0]['message']['content']
            self.text_area_gpt.insert(tk.END, f"Morpheus: {generated_text}\n")
        except Exception as e:
            self.text_area_gpt.insert(tk.END, f"\nMorpheus: Error: {str(e)}\n")

        self.entry_field_gpt.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')  # set background color of the root window
    nmap_gpt_gui = NmapGPTGUI(root)
    root.mainloop()
