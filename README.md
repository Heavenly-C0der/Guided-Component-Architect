# Guided Component Architect

An agentic, governed code-generation system that transforms natural language descriptions into styled Angular components while strictly enforcing a predefined design system.
---

## Overview

This project demonstrates a structured, production-oriented approach to LLM-based code generation. Instead of simple prompt-to-code behavior, it implements:

* Design system enforcement
* Structured JSON output
* Validation + self-correction loop
* Deployment-ready backend
* Live frontend preview
* Export functionality (.tsx download)

The system is built to resemble the architectural foundations of tools like Lovable or Bolt.new — with governance layers and deterministic validation.

---

## Architecture

```
User Prompt
    ↓
Next.js Frontend (Vercel)
    ↓
API Proxy (/api/generate)
    ↓
Flask Backend (Render)
    ↓
Hugging Face (Qwen2.5-Coder-7B-Instruct)
    ↓
Structured JSON Output
    ↓
Validator + Retry Loop
    ↓
Preview Wrapper
    ↓
Sandboxed iframe Render
```

---

## Core Features

### 1. Design System Governance

A JSON-based design system defines tokens such as:

* Primary color
* Glass background
* Border radius
* Typography

All generated components are validated against these tokens.

---

### 2. Structured LLM Output

The model is forced to return:

```json
{
  "angular_code": "...",
  "preview_html": "..."
}
```

Outputs are parsed and rejected if invalid.

---

### 3. Validation + Self-Correction Loop

The system validates:

* Syntax integrity
* Design token compliance
* Structural correctness

If validation fails:

* The model is re-prompted with structured error logs.
* Retries are attempted.
* If still invalid → request is rejected.

This prevents uncontrolled generation.

---

### 4. Live Preview

The generated component is rendered inside a sandboxed iframe.

Live deployment:
[https://guided-component-architect.vercel.app/](https://guided-component-architect.vercel.app/)

---

### 5. Export Feature

Users can download the generated component as:

```
GeneratedComponent.tsx
```

This allows local integration or further development.

---

## Repository Structure

```
backend/
    app.py
    architect.py
    generator.py
    validator.py
    llm_client.py
    preview.py
    system_design.json
    requirements.txt
    runtime.txt

frontend/
    pages/
        index.js
        api/generate.js
    package.json
    next.config.mjs
```

---

## Deployment

### Backend

* Hosted on Render
* Python 3.11
* Gunicorn
* Hugging Face inference API

### Frontend

* Hosted on Vercel
* Next.js (Pages Router)
* Serverless API proxy

---

## Security & Prompt Injection Mitigation

The system prevents prompt injection through:

* System-level instruction separation
* Strict JSON schema enforcement
* Output validation
* Retry-based correction
* No direct model output execution
* Sandboxed preview rendering

User input is treated strictly as data, never as control logic.

---

## Future Enhancements

* Multi-turn editing
* AST-based validation
* Dependency whitelisting
* Component registry enforcement
* Role-based multi-agent orchestration
* Full-page application synthesis

---

## Technical Stack

* Python (Flask)
* Hugging Face (Qwen2.5-Coder-7B-Instruct)
* aisuite
* Next.js
* Vercel
* Render
