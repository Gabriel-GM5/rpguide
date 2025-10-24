from langchain_core.prompts import ChatPromptTemplate

class PromptsManager:
    def __init__(self, config):
        self.config = config
        system_prompt_template = self._load_prompt("system")
        self.system_prompt = system_prompt_template.replace("{PERSONA_DESCRIPTION}", self.config.AI_PERSONA).replace("{EXIT_COMMAND}", self.config.texts['exit.term'])
        self.human_prompt = self._load_prompt("human")

    def _load_prompt(self, prompt_type):
        import os
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "prompts", f"{prompt_type}_{self.config.LANGUAGE}.txt")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def get_prompts(self):
        return ChatPromptTemplate.from_messages([("system", self.system_prompt), ("human", self.human_prompt)])