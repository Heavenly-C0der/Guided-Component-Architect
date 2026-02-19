// frontend/pages/index.js
import { useState } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [codeHtml, setCodeHtml] = useState("");

  async function onGenerate() {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
  
    const json = await res.json();
  
    console.log("API RESPONSE:", json);
  
    if (json.preview_html) {
      setCodeHtml(json.preview_html);
    } else {
      console.error("Backend error:", json);
      setCodeHtml("<div style='padding:20px;color:red;'>Error generating preview</div>");
    }
}


  return (
    <div style={{ padding: 20 }}>
      <h2>Guided Component Architect — Live Preview</h2>
      <textarea
        rows={4}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe the component (e.g. 'A login card with glassmorphism')"
        style={{ width: "100%", marginBottom: 10 }}
      />
      <div style={{ display: "flex", gap: 8 }}>
        <button onClick={onGenerate}>Generate & Preview</button>
      </div>

      <h3>Preview</h3>
      <iframe
        title="preview"
        srcDoc={codeHtml}
        style={{ width: "100%", height: 500 }}
      />
    </div>
  );
}




