import sys
import os
import pickle
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, \
    QTextEdit, QWidget, QInputDialog, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QParallelAnimationGroup, QSequentialAnimationGroup, QEasingCurve
from functools import partial
import subprocess


class ScriptRunner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Hangover")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()

        ascii_text = '''
               _   .-')       ('-.   ('-.         .-') _  
              ( '.( OO )_   _(  OO) ( OO ).-.    ( OO ) ) 
                ,--.   ,--.)(,------./ . --. /,--./ ,--,'  
                |   `.'   |  |  .---'| \-.  \ |   \ |  |\  
                |         |  |  |  .-'-'  |  ||    \|  | ) 
                |  |'.'|  | (|  '--.\| |_.'  ||  .     |/  
                |  |   |  |  |  .--' |  .-.  ||  |\    |   
                |  |   |  |  |  `---.|  | |  ||  | \   |   
                `--'   `--'  `------'`--' `--'`--'  `--'                              
                '''

        ascii_label = QLabel()
        ascii_label.setFont(QFont("Courier", 12, QFont.Weight.Bold))
        ascii_label.setText(ascii_text)
        self.layout.addWidget(ascii_label)

        title_label = QLabel("Welcome to SOCBox")
        title_label.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Add this line to center the label
        self.layout.addWidget(title_label)

        subtitle_label = QLabel("")
        font = QFont("Helvetica", 10)
        font.setItalic(True)
        subtitle_label.setFont(font)
        self.layout.addWidget(subtitle_label)

        button_layout = QHBoxLayout()  # Create a QHBoxLayout for the buttons
        self.add_button = QPushButton("Add Tool", clicked=self.add_script)
        button_layout.addWidget(self.add_button)  # Add the "Add" button to the button layout

        self.remove_button = QPushButton("Remove Tool", clicked=self.remove_script)
        button_layout.addWidget(self.remove_button)  # Add the "Remove" button to the button layout

        self.layout.addLayout(button_layout)  # Add the button layout to the main layout

        self.subtitle_label = QLabel()
        self.subtitle_label.setText(
            "Developers: Matt, Eddie, Andre, Nate (M.E.A.N)<br>Fullstack Academy - Cohort 2212-FCB-ET-CYB-PT<br>May 2023<br>")
        self.subtitle_label.setWordWrap(True)
        self.layout.addWidget(self.subtitle_label)

        self.load_script_buttons()

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def add_script(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Python file", "", "Python Files (*.py)")

        if file_path:
            file_name = os.path.basename(file_path)
            button_name, ok = QInputDialog.getText(self, "Button Name", "Enter the button name:", text=file_name)
            if ok and button_name:
                button = QPushButton(button_name)
                button.clicked.connect(partial(self.run_script, file_path))
                self.layout.insertWidget(self.layout.count() - 2, button)  # Add button above the text widget

                # Save to persistent storage
                self.save_script_button(button_name, file_path)

    def remove_script(self):
        print("In remove_script")
        script_buttons = self.load_script_buttons()
        button_name, ok = QInputDialog.getItem(self, "Remove Tool", "Select the tool to remove:",
                                               list(script_buttons.keys()), 0, False)
        print(f"button_name: {button_name}, ok: {ok}")
        if ok and button_name:
            confirm_options = ["Yes", "No"]
            confirm_choice, _ = QInputDialog.getItem(self, "Confirm Removal",
                                                     "Are you sure you want to remove this tool?", confirm_options, 0,
                                                     False)
        if confirm_choice == "Yes":
            print(f"Removing {button_name}")
            self.remove_script_button(button_name)
            self.reload_script_buttons()
        else:
            print(
                "No button_name or ok is False")  # This line will print if ok is False or button_name is None or an empty string

    def run_script(self, file_path):
        # Run the selected script file in a subprocess using the appropriate Python interpreter
        python_interpreter = sys.executable
        try:
            subprocess.check_call([python_interpreter, file_path])
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while executing script: {e}")

    def load_script_buttons(self):
        try:
            with open('script_buttons.pkl', 'rb') as f:
                script_buttons = pickle.load(f)
        except FileNotFoundError:
            script_buttons = {}

        current_buttons = [self.layout.itemAt(i).widget().text() for i in range(self.layout.count()) if
                           isinstance(self.layout.itemAt(i).widget(), QPushButton)]
        for button_name, file_path in script_buttons.items():
            try:
                if button_name not in current_buttons:
                    button = QPushButton(button_name)
                    button.clicked.connect(partial(self.run_script, file_path))
                    self.layout.insertWidget(self.layout.count() - 2, button)  # Add button above the text widget
            except Exception as e:
                print(f"Error in creating button {button_name}: {e}")

        return script_buttons

    def save_script_button(self, button_name, file_path):
        try:
            with open('script_buttons.pkl', 'rb') as f:
                script_buttons = pickle.load(f)
        except FileNotFoundError:
            script_buttons = {}

        script_buttons[button_name] = file_path

        with open('script_buttons.pkl', 'wb') as f:
            pickle.dump(script_buttons, f)

    def remove_script_button(self, button_name):
        print(f"In remove_script_button with {button_name}")
        try:
            with open('script_buttons.pkl', 'rb') as f:
                script_buttons = pickle.load(f)
        except FileNotFoundError:
            return

        if button_name in script_buttons:
            del script_buttons[button_name]

        with open('script_buttons.pkl', 'wb') as f:
            pickle.dump(script_buttons, f)

        print(f"In remove_script_button with button_name: {button_name}")  # Add this line

        # Find and remove the button from the layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text() == button_name:
                print(f"Found button {button_name} in layout")
                self.layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()

    def reload_script_buttons(self):
        # Save a reference to the add and remove buttons
        reserved_buttons = {self.add_button, self.remove_button}

        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget not in reserved_buttons:
                # Remove the button from the layout and delete it
                self.layout.removeWidget(widget)
                widget.setParent(None)
        self.load_script_buttons()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ScriptRunner()
    window.show()

    sys.exit(app.exec())
