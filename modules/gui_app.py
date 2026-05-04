import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from modules.configs import Config, _resource_base
from modules.connectors_manager import ConnectorManager


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.config = Config()
        self.connector = ConnectorManager(self.config)
        self.uploaded_files = []

        window_title = self.config.texts.get('ui.window.title', 'RPGuide')
        self.root.title(f"{window_title} - {self.config.AI_PERSONA}")
        self.root.geometry("800x600")

        icon_path = os.path.join(_resource_base(), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        main_frame = ttk.Frame(root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(fill=BOTH, expand=True, padx=0, pady=(0, 10))

        scrollbar = ttk.Scrollbar(chat_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.chat_display = ttk.Text(
            chat_frame,
            height=20,
            width=80,
            yscrollcommand=scrollbar.set,
            state=DISABLED,
            wrap=WORD
        )
        self.chat_display.pack(fill=BOTH, expand=True, side=LEFT)
        scrollbar.config(command=self.chat_display.yview)

        self.chat_display.tag_config("user", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="green", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("debug", foreground="orange", font=("Arial", 9, "italic"))
        self.chat_display.tag_config("message", font=("Arial", 10))

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=X, padx=0, pady=0)

        upload_button_text = self.config.texts.get('ui.button.upload', 'Upload Files')
        upload_button = ttk.Button(input_frame, text=upload_button_text, command=self.upload_files, bootstyle="primary")
        upload_button.pack(side=LEFT, padx=(0, 5))

        self.input_field = ttk.Entry(input_frame, width=60)
        self.input_field.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.send_message)

        send_button_text = self.config.texts.get('ui.button.send', 'Send')
        send_button = ttk.Button(input_frame, text=send_button_text, command=self.send_message, bootstyle="success")
        send_button.pack(side=LEFT, padx=(0, 5))

        config_button_text = self.config.texts.get('ui.button.config', 'Settings')
        config_button = ttk.Button(input_frame, text=config_button_text, command=self._open_config, bootstyle="secondary")
        config_button.pack(side=LEFT, padx=(0, 5))

        exit_button_text = self.config.texts.get('ui.button.exit', 'Exit')
        exit_button = ttk.Button(input_frame, text=exit_button_text, command=self.exit_app, bootstyle="danger")
        exit_button.pack(side=LEFT)

        self.show_initial_greeting()

    def _open_config(self):
        from modules.setup_app import run_setup_dialog

        if run_setup_dialog(self.root):
            self.root.after(100, self._restart)

    def _restart(self):
        self.root.destroy()
        # In a frozen EXE sys.argv[0] is already the executable path; in dev mode
        # prepend sys.executable so Python receives the script as the first real arg.
        args = sys.argv if getattr(sys, "frozen", False) else [sys.executable] + sys.argv
        os.execv(sys.executable, args)

    def upload_files(self):
        """Open file dialog to select files for upload."""
        filetypes = [
            ("All files", "*.*"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.doc *.docx"),
            ("Excel files", "*.xls *.xlsx"),
            ("Markdown files", "*.md"),
            ("HTML files", "*.html *.htm"),
            ("Rich Text files", "*.rtf"),
            ("CSV files", "*.csv")
        ]

        filenames = tk.filedialog.askopenfilenames(
            title="Select files to upload",
            filetypes=filetypes
        )

        if not filenames:
            return

        for filename in filenames:
            self.process_uploaded_file(filename)

    def process_uploaded_file(self, filepath):
        """Process and store an uploaded file."""
        from pathlib import Path

        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)

        filename = os.path.basename(filepath)
        destination = upload_dir / filename

        try:
            import shutil
            shutil.copy2(filepath, destination)
            self.uploaded_files.append(str(destination))
            self.display_message("System", f"Uploaded: {filename}", is_user=False)

            if self.config.DEBUG:
                print(f"[DEBUG] File uploaded: {destination}")
        except Exception as e:
            error_msg = self.config.texts.get('error.file.upload', f'Error uploading file: {str(e)}')
            self.display_message("System", error_msg, is_user=False)

    def show_initial_greeting(self):
        """Display initial greeting from the AI."""
        greeting_question = self.config.texts.get('initial.question', 'Introduce yourself.')
        self.input_field.config(state=DISABLED)

        thread = threading.Thread(target=self.get_greeting_response, args=(greeting_question,))
        thread.daemon = True
        thread.start()

    def get_greeting_response(self, question):
        """Get greeting response in background thread."""
        try:
            response = self.connector.call(question)
            self.root.after(0, lambda: self.display_message(self.config.AI_PERSONA, response, is_user=False))
        except Exception as e:
            error_msg = self.config.texts.get('error.connection', f'Error: {str(e)}')
            self.root.after(0, lambda: self.display_message('System', error_msg, is_user=False))
        finally:
            self.root.after(0, lambda: self.input_field.config(state=NORMAL))
            self.root.after(0, lambda: self.input_field.focus())

    def send_message(self, event=None):
        """Send user message and get response."""
        user_input = self.input_field.get().strip()
        if not user_input:
            return

        if user_input.lower() == self.config.texts['exit.term'].lower():
            self.exit_app()
            return

        self.display_message(self.config.texts['user.pronoun'], user_input, is_user=True)
        self.input_field.delete(0, END)
        self.input_field.config(state=DISABLED)

        thread = threading.Thread(target=self.get_response, args=(user_input,))
        thread.daemon = True
        thread.start()

    def get_response(self, question):
        """Get AI response in background thread."""
        try:
            response = self.connector.call(question)
            self.root.after(0, lambda: self.display_message(self.config.AI_PERSONA, response, is_user=False))
        except Exception as e:
            error_msg = self.config.texts.get('error.connection', f'Error: {str(e)}')
            self.root.after(0, lambda: self.display_message('System', error_msg, is_user=False))
        finally:
            self.root.after(0, lambda: self.input_field.config(state=NORMAL))
            self.root.after(0, lambda: self.input_field.focus())

    def display_message(self, sender, message, is_user=True):
        """Display a message in the chat window."""
        self.chat_display.config(state=NORMAL)
        tag = "user" if is_user else "assistant"
        self.chat_display.insert(END, f"{sender}: ", tag)
        self.chat_display.insert(END, f"{message}\n\n", "message")
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)

    def exit_app(self):
        """Show farewell and exit."""
        farewell_question = self.config.texts.get('final.question', 'Goodbye.')
        self.input_field.config(state=DISABLED)

        def close_app():
            try:
                response = self.connector.call(farewell_question)
                self.root.after(0, lambda: self.display_message(self.config.AI_PERSONA, response, is_user=False))
            except Exception as e:
                farewell_msg = self.config.texts.get('final.message', 'Goodbye!')
                self.root.after(0, lambda: self.display_message('System', farewell_msg, is_user=False))
            finally:
                self.root.after(1500, self.root.quit)

        thread = threading.Thread(target=close_app)
        thread.daemon = True
        thread.start()


def run_gui():
    """Run the GUI chat interface."""
    try:
        root = ttk.Window(themename="darkly")
        app = ChatApp(root)
        root.mainloop()
    except Exception as e:
        print(f"GUI Error: {str(e)}")
        print("The application encountered an error and will close.")
        sys.exit(1)
