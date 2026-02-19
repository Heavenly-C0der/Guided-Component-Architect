import aisuite as ai

class LLMClient:
    def __init__(
        self,
        model="huggingface:Qwen/Qwen2.5-Coder-7B-Instruct",
        api_key=None,
        max_retries=2,
    ):
        self.model = model
        self.max_retries = max_retries

        self.client = ai.Client(
            provider_configs={
                "huggingface": {
                    "api_key": api_key,  # set via env var
                    "timeout": 300,
                }
            }
        )

    def generate(self, system_prompt: str, user_prompt: str, temperature=0.1) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        last_error = None

        for _ in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                )

                content = response.choices[0].message.content.strip()

                # Strip markdown fences if model adds them
                if content.startswith("```"):
                    parts = content.split("```")
                    if len(parts) >= 2:
                        content = parts[1]

                return content.strip()

            except Exception as e:
                last_error = str(e)

        raise RuntimeError(f"LLM generation failed: {last_error}")
