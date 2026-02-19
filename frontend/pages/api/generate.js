// frontend/pages/api/generate.js
export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  const { prompt } = req.body;
  const backendUrl = process.env.BACKEND_URL; // e.g. https://my-generator.example.com/generate

  if (!backendUrl) {
    return res.status(500).json({ error: "BACKEND_URL not set" });
  }

  try {
    // POST to your Python service which returns { html: "<!doctype html>..." } or { code: "<tsx ...>" }
    const r = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const json = await r.json();

    // Basic sanitization / normalization
    let html = json.html || json.code || "";
    // If your generator returns TSX/Angular: convert or wrap it into HTML shell for preview
    if (html && !html.trim().startsWith("<")) {
      // treat as raw component code — wrap so preview shows something clear
      html = `<pre style="white-space:pre-wrap;padding:16px;background:#f7f7f7">${escapeHtml(html)}</pre>`;
    }

    return res.status(200).json({ html });
  } catch (err) {
    console.error("proxy error:", err);
    return res.status(500).json({ error: String(err) });
  }
}

function escapeHtml(str = "") {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
