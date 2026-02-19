import re
from bs4 import BeautifulSoup  # add to notebook requirements; or use html.parser

class ComponentValidator:
    def __init__(self, design_system_path):
        import json
        from pathlib import Path
        if isinstance(design_system_path, (str,)):
            design_system_path = Path(design_system_path)
        with open(design_system_path, "r", encoding="utf-8") as f:
            self.design_system = json.load(f)

        # collect only valid hex color tokens for comparison
        self.allowed_hex = [
            v for v in self.design_system.get("tokens", {}).values()
            if isinstance(v, str) and re.fullmatch(r'#[0-9a-fA-F]{6}', v)
        ]
        # also allow rgba or token names if present
        self.allowed_values = list(self.design_system.get("tokens", {}).values())

    def check_hex_usage(self, code: str):
        hex_colors = re.findall(r'#[0-9a-fA-F]{6}', code)
        invalid = [h for h in hex_colors if h not in self.allowed_hex]
        return invalid

    def check_token_presence(self, text: str):
        # Ensure at least one design token is present (color, font, or border-radius)
        found = []
        for k, v in self.design_system.get("tokens", {}).items():
            if isinstance(v, str) and v in text:
                found.append(k)
        return found

    def check_html_valid(self, markup: str):
        # use BeautifulSoup to parse — ensures markup is not completely broken
        try:
            soup = BeautifulSoup(markup, "html.parser")
            # if the markup is essentially empty, flag it
            if not soup.find():
                return ["preview markup seems empty or unparsable"]
            return []
        except Exception as e:
            return [f"HTML parse error: {e}"]

    def check_brackets(self, code: str):
        stack = []
        pairs = {"{": "}", "(": ")", "[": "]"}
        for ch in code:
            if ch in pairs:
                stack.append(pairs[ch])
            elif ch in pairs.values():
                if not stack or ch != stack.pop():
                    return False
        return not stack

    def validate_structured(self, generated: dict):
        """
        Accepts dict with keys 'angular_code' and 'preview_markup'.
        Returns list of error strings (empty if ok).
        """
        errors = []

        angular_code = generated.get("angular_code", "") or ""
        preview_markup = generated.get("preview_markup", "") or ""

        # check brackets in code
        if not self.check_brackets(angular_code):
            errors.append("Bracket / brace mismatch in angular_code.")

        # invalid raw hex in either artifact
        invalid_hex_code = self.check_hex_usage(angular_code)
        invalid_hex_preview = self.check_hex_usage(preview_markup)
        if invalid_hex_code:
            errors.append(f"Invalid hex color used in angular_code: {invalid_hex_code}")
        if invalid_hex_preview:
            errors.append(f"Invalid hex color used in preview_markup: {invalid_hex_preview}")

        # require presence of at least one design token somewhere (guard against token omission)
        found_tokens = set(self.check_token_presence(angular_code) + self.check_token_presence(preview_markup))
        if not found_tokens:
            errors.append("No design tokens from design_system.json found in output (colors/fonts/border-radius).")

        # html validity
        errors.extend(self.check_html_valid(preview_markup))

        return errors
