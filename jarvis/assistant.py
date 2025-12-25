class JarvisAssistant:
    def __init__(self, engine, prompt_controller, memory):
        self.engine = engine
        self.prompt_controller = prompt_controller
        self.memory = memory

    def run_task(self, task, user_input):
        prompt = self.prompt_controller.build_prompt(
            task,
            user_input,
            self.memory
        )
        response = self.engine.generate(prompt)
        return response
