import sys
from modules.connectors_manager import ConnectorManager
from modules.configs import Config

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
