from modules.connectors_manager import ConnectorManager
from modules.configs import Config

def main ():
    config = Config()
    connector = ConnectorManager(config)
    print(f"{config.AI_PERSONA}: {connector.call(config.texts['initial.question'])}")
    while True:
        question = input(f"{config.texts['user.pronoun']}: ")
        if question.lower() == config.texts['exit.term'].lower():
            print(f"{config.AI_PERSONA}: {connector.call(config.texts['final.question'])}")
            break
        resp = connector.call(question)
        print(f"{config.AI_PERSONA}: {resp}")
    exit(0)

if __name__ == "__main__":
    main()