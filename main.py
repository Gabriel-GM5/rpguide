"import sys
from modules.configs import Config

def main():
    try:
        config = Config()
        
        # Determine mode: command-line argument takes precedence over .env
        mode = config.MODE  # Default from .env
        
        if len(sys.argv) > 1:
            arg_mode = sys.argv[1].lower()
            if arg_mode in (\"gui\", \"terminal\"):
                mode = arg_mode
            else:
                print(f\"Invalid mode argument: {arg_mode}\")
                print(\"Usage: python3 main.py [gui|terminal]\")
                print(f\"Using default mode from .env: {mode}\")
        
        if mode == \"terminal\":
            from modules.terminal_app import run_terminal
            run_terminal()
        else:
            from modules.gui_app import run_gui
            run_gui()
    except Exception as e:
        print(f\"Fatal Error: {str(e)}\")
        print(\"The application failed to start.\")
        sys.exit(1)


if __name__ == \"__main__\":
    main()"
