from langchain_core.prompts import ChatPromptTemplate

class PromptsManager:
    def __init__(self, config):
        self.config = config
        system_prompt_template = self._load_prompt("system")
        # Ensure config.AI_PERSONA is a string and config.texts['exit.term'] exists
        persona_desc = getattr(config, 'AI_PERSONA', '') or ''
        if hasattr(config, 'texts') and isinstance(config.texts, dict):
            exit_command = config.texts.get('exit.term', '') or ''
        else:
            exit_command = ''
        self.system_prompt = system_prompt_template.replace("{PERSONA_DESCRIPTION}", persona_desc).replace("{EXIT_COMMAND}", exit_command)
        self.human_prompt = self._load_prompt("human")
        try:
            self.analyzer_prompt = self._load_prompt("analyzer")
        except FileNotFoundError:
            self.analyzer_prompt = None

    def _load_prompt(self, prompt_type):
        import os
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "prompts", f"{prompt_type}_en_us.txt")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def get_prompts(self):
        return ChatPromptTemplate.from_messages([("system", self.system_prompt), ("human", self.human_prompt)])

    def get_analyzer_prompt(self):
        return self.analyzer_prompt