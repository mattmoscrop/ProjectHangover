import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import threading
import subprocess
from tkinter import ttk
import openai
import os

# Set up OpenAI GPT API credentials
openai.api_key = 'Add Your Open AI API Here'

class TracerouteGPTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traceroute GPT GUI")
        self.root.configure(bg="#333333")  # Set background color of the root window

        # Set the title color to green
        self.root.option_add('*Dialog.msg.font', 'Helvetica 12 bold')
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

        self.clear_button_gpt = tk.Button(self.root, text="Clear GPT Text", command=self.clear_text_gpt, bg='black', fg='green', font=font_size)
        self.clear_button_gpt.grid(row=3, column=0, pady=10)

        # Separator
        self.separator = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.separator.grid(row=4, column=0, sticky="ew", pady=10)

        # Bottom Widget
        self.bottom_frame = tk.Frame(self.root, bg='black')
        self.bottom_frame.grid(row=5, column=0, sticky="ew")

        self.user_label_traceroute = tk.Label(self.bottom_frame, text="IP Address or DNS: ", bg='black', fg='green', font=font_size)
        self.user_label_traceroute.pack(side=tk.LEFT)

        self.text_area_traceroute = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg='black', fg='green', insertbackground='green', font=font_size)
        self.text_area_traceroute.grid(row=6, column=0, sticky="nsew")

        self.run_button_traceroute = tk.Button(self.root, text="Run Traceroute", command=self.run_traceroute, bg='black', fg='green', font=font_size)
        self.run_button_traceroute.grid(row=7, column=0, pady=10)

        self.clear_button_traceroute = tk.Button(self.root, text="Clear Traceroute Text", command=self.clear_text_traceroute, bg='black', fg='green', font=font_size)
        self.clear_button_traceroute.grid(row=8, column=0, pady=10)

        # Entry field to edit the option
        self.entry_field_traceroute = tk.Entry(self.bottom_frame, bg='black', fg='green', insertbackground='green', font=font_size)
        self.entry_field_traceroute.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.entry_field_traceroute.bind("<Return>", self.run_traceroute)
        self.entry_field_traceroute.bind("<KP_Enter>", self.run_traceroute)


        # Start the instruction process
        self.text_area_gpt.insert(tk.END, 'Morpheus: Hello Neo. How can I help you with Traceroute?')

        # Configure resizing behavior
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def run_traceroute(self, event=None):
        ip_address = self.entry_field_traceroute.get()
        self.text_area_traceroute.insert(tk.END, f"\nMorpheus: Running Traceroute on IP: {ip_address}\n")

        try:
            # Run traceroute command
            traceroute_process = subprocess.Popen(['tracert', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = traceroute_process.communicate()

            # Decode the output
            output = output.decode('utf-8')

            self.text_area_traceroute.insert(tk.END, f"Morpheus: {output}\n")
        except Exception as e:
            self.text_area_traceroute.insert(tk.END, f"\nMorpheus: Error: {str(e)}\n")

        self.entry_field_traceroute.delete(0, tk.END)

    def update_entry_traceroute(self, value):
        # This function updates the entry field when an option is selected from the dropdown
        self.entry_field_traceroute.delete(0, tk.END)  # Remove the current option
        self.entry_field_traceroute.insert(0, value)  # Insert the selected option

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

    def clear_text_gpt(self):
        self.text_area_gpt.delete(1.0, tk.END)

    def clear_text_traceroute(self):
        self.text_area_traceroute.delete(1.0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')  # set background color of the root window
    traceroute_gpt_gui = TracerouteGPTGUI(root)
    root.mainloop()
