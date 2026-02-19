import json


class ComponentGenerator:
    def __init__(self, llm_client, design_system_path):
        self.llm = llm_client
        if isinstance(design_system_path, (str,)):
            from pathlib import Path
            design_system_path = Path(design_system_path)
        with open(design_system_path, "r", encoding="utf-8") as f:
            self.design_system = json.load(f)

    def build_prompt(self, user_prompt: str) -> str:
        # Force LLM to output JSON only with two fields:
        return f"""
        You are a deterministic JSON generator.

        CRITICAL:
        You MUST output a valid JSON object.
        You MUST NOT output markdown.
        You MUST NOT output explanations.
        You MUST NOT output text before or after JSON.
        If you violate this, the system will reject your response.

        Output schema:
        {{
        "angular_code": string,
        "preview_markup": string
        }}

        Design tokens:
        {json.dumps(self.design_system["tokens"], indent=2)}

        User request:
        {user_prompt}
        """

    def generate(self, user_prompt: str) -> dict:
        system_prompt = "You generate production-ready Angular components and a small HTML preview fragment."
        prompt = self.build_prompt(user_prompt)
        raw = self.llm.generate(system_prompt, prompt, temperature=0.2)

        # The LLM should return a JSON object. Parse robustly.
        try:
            return json.loads(raw)
        except Exception:
            # recover: find first '{' and last '}' and parse substring
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1:
                try:
                    return json.loads(raw[start:end+1])
                except Exception as e:
                    raise RuntimeError("LLM returned non-JSON output and recovery failed.") from e
            raise RuntimeError("LLM returned non-JSON output.")
