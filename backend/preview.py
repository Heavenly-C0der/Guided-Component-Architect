def wrap_preview(preview_markup: str, design_tokens: dict) -> str:
    # Use Tailwind CDN for quick styling. Keep scripts out.
    font_family = design_tokens.get("font-family", "Inter, system-ui, sans-serif")
    primary = design_tokens.get("primary-color", "#6366f1")
    background_glass = design_tokens.get("background-glass", "rgba(255,255,255,0.15)")

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <style>
    :root {{
      --primary-color: {primary};
      --background-glass: {background_glass};
      font-family: {font_family};
    }}
    body {{ font-family: var(--font-family, {font_family}); background: linear-gradient(120deg,#f3f4f6,#fff); padding: 28px; }}
    /* small safety CSS: prevent huge images */
    img {{ max-width: 100%; height: auto; }}
  </style>
</head>
<body>
  <div class="min-h-screen flex items-center justify-center">
    {preview_markup}
  </div>
</body>
</html>"""
    return html
