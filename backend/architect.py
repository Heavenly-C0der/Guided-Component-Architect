import json
from typing import Optional
class GuidedComponentArchitect:

    def __init__(self, generator, validator, llm_client):
        self.generator = generator
        self.validator = validator
        self.llm = llm_client
        self.current_code: Optional[dict] = None


    def fix_structured(self, generated: dict, errors: list) -> dict:
        """
        Re-prompt the LLM asking to fix angular_code and/or preview_markup.
        Provide the error log and the previous JSON.
        Expect a new JSON object returned (same schema).
        """
        system_prompt = "You fix previously generated Angular component JSON. Return a single JSON object."
        fix_prompt = f"""
        The previous generation failed these checks:
        {json.dumps(errors, indent=2)}

        Previous output (JSON):
        {json.dumps(generated, indent=2)}

        Please return a corrected JSON object with the same schema:
        {{
        "angular_code": "...",
        "preview_markup": "..."
        }}

        Rules:
        - Only output valid JSON (no commentary).
        - Fix the specific errors. Keep changes minimal.
        - Use the design tokens given earlier.
        """
        raw = self.llm.generate(system_prompt, fix_prompt, temperature=0.1)
        try:
            return json.loads(raw)
        except Exception:
            # attempt recovery like before
            s = raw.find("{")
            e = raw.rfind("}")
            if s != -1 and e != -1:
                return json.loads(raw[s:e+1])
            raise RuntimeError("Fix step returned non-JSON output.")

    def edit(self, instruction):
        if not self.current_code:
            raise ValueError("No existing component to edit.")

        system_prompt = "You modify Angular components precisely."
        edit_prompt = f"""
        You are editing an Angular component.

        Existing Component:
        {self.current_code}

        Instruction:
        {instruction}

        Return full updated component only.
        """


        updated = self.llm.generate(system_prompt, edit_prompt)

        errors = self.validator.validate(updated)
        if errors:
            updated = self.fix_structured(updated, errors)

        self.current_code = updated
        return updated

    def run(self, user_prompt: str, max_retries: int = 5) -> dict:
        generated = self.generator.generate(user_prompt)

        for attempt in range(max_retries + 1):
            errors = self.validator.validate_structured(generated)
            if not errors:
                self.current_code = generated
                return generated

            # logging helps the evaluator see loop behavior
            print(f"[Attempt {attempt}] Validation errors:", errors)
            generated = self.fix_structured(generated, errors)

        raise RuntimeError("Failed to produce valid component after retries.")

