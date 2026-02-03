import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from modules.connectors_manager import ConnectorManager
from modules.configs import Config
import threading
import sys

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.config = Config()
        self.connector = ConnectorManager(self.config)
        
        # Use localized window title
        window_title = self.config.texts.get('ui.window.title', 'RPGuide')
        self.root.title(f"{window_title} - {self.config.AI_PERSONA}")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Chat display area
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
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="green", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("debug", foreground="orange", font=("Arial", 9, "italic"))
        self.chat_display.tag_config("message", font=("Arial", 10))
        
        # Input area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=X, padx=0, pady=0)
        
        self.input_field = ttk.Entry(input_frame, width=70)
        self.input_field.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.send_message)
        
        send_button_text = self.config.texts.get('ui.button.send', 'Send')
        send_button = ttk.Button(input_frame, text=send_button_text, command=self.send_message, bootstyle="success")
        send_button.pack(side=LEFT, padx=(0, 5))
        
        exit_button_text = self.config.texts.get('ui.button.exit', 'Exit')
        exit_button = ttk.Button(input_frame, text=exit_button_text, command=self.exit_app, bootstyle="danger")
        exit_button.pack(side=LEFT)
        
        # Show initial greeting
        self.show_initial_greeting()
    
    def show_initial_greeting(self):
        """Display initial greeting from the AI."""
        greeting_question = self.config.texts.get('initial.question', 'Introduce yourself.')
        self.input_field.config(state=DISABLED)
        
        # Run in thread to avoid blocking UI
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
        
        # Check for exit command
        if user_input.lower() == self.config.texts['exit.term'].lower():
            self.exit_app()
            return
        
        # Display user message
        self.display_message(self.config.texts['user.pronoun'], user_input, is_user=True)
        self.input_field.delete(0, END)
        self.input_field.config(state=DISABLED)
        
        # Get response in background thread
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
        
        # Add sender name
        tag = "user" if is_user else "assistant"
        self.chat_display.insert(END, f"{sender}: ", tag)
        
        # Add message content
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


def run_terminal():
    """Run the terminal-based chat interface."""
    try:
        config = Config()
        connector = ConnectorManager(config)
        
        # Show initial greeting
        greeting_question = config.texts.get('initial.question', 'Introduce yourself.')
        try:
            response = connector.call(greeting_question)
            print(f"{config.AI_PERSONA}: {response}\n")
        except Exception as e:
            error_msg = config.texts.get('error.connection', f'Error: {str(e)}')
            print(f"System: {error_msg}\n")
        
        # Chat loop
        while True:
            try:
                question = input(f"{config.texts['user.pronoun']}: ").strip()
                
                if not question:
                    continue
                
                # Check for exit command
                if question.lower() == config.texts['exit.term'].lower():
                    farewell_question = config.texts.get('final.question', 'Goodbye.')
                    try:
                        response = connector.call(farewell_question)
                        print(f"{config.AI_PERSONA}: {response}")
                    except Exception:
                        farewell_msg = config.texts.get('final.message', 'Goodbye!')
                        print(f"System: {farewell_msg}")
                    break
                
                # Get and display response
                try:
                    response = connector.call(question)
                    print(f"{config.AI_PERSONA}: {response}\n")
                except Exception as e:
                    error_msg = config.texts.get('error.connection', f'Error: {str(e)}')
                    print(f"System: {error_msg}\n")
            except KeyboardInterrupt:
                farewell_msg = config.texts.get('final.message', 'Goodbye!')
                print(f"\nSystem: {farewell_msg}")
                break
            except Exception as e:
                error_msg = config.texts.get('error.unexpected', f'Unexpected error: {str(e)}')
                print(f"System: {error_msg}\n")
    except Exception as e:
        print(f"Terminal Error: {str(e)}")
        print("The application encountered an error and will close.")
        sys.exit(1)


def main():
    try:
        config = Config()
        
        # Determine mode: command-line argument takes precedence over .env
        mode = config.MODE  # Default from .env
        
        if len(sys.argv) > 1:
            arg_mode = sys.argv[1].lower()
            if arg_mode in ("gui", "terminal"):
                mode = arg_mode
            else:
                print(f"Invalid mode argument: {arg_mode}")
                print("Usage: python3 main.py [gui|terminal]")
                print(f"Using default mode from .env: {mode}")
        
        if mode == "terminal":
            run_terminal()
        else:
            run_gui()
    except Exception as e:
        print(f"Fatal Error: {str(e)}")
        print("The application failed to start.")
        sys.exit(1)


if __name__ == "__main__":
    main()