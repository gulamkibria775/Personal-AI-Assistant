class PromptController:

    ROLE_MAP = {
        "sentiment": "You are an NLP expert. Analyze sentiment clearly.",
        "translation": "You are a language translator. Translate accurately into Bangla.",
        "detection": "You are a linguist. Detect the language."
    }

    TASK_INSTRUCTION = {
        "sentiment": "Give me the sentiment of this sentence.",
        "translation": "Give me Bangla translation of this sentence.",
        "detection": "Detect the language of this sentence."
    }

    def build_prompt(self, task, user_input, memory):
        system_prompt = self.ROLE_MAP.get(task, "You are a helpful assistant.")
        instruction = self.TASK_INSTRUCTION.get(task, "Respond to the user input.")

        history = ""
        for msg in memory.get_history():
            history += f"{msg['role'].upper()}: {msg['message']}\n"

        final_prompt = f"""
SYSTEM:
{system_prompt}

TASK:
{instruction}

CONVERSATION HISTORY:
{history}

USER INPUT:
{user_input}

ASSISTANT:
"""
        return final_prompt.strip()
