// frontend/pages/api/generate.js
// frontend/pages/api/generate.js

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).end();
  }

  const backendUrl = process.env.BACKEND_URL;

  if (!backendUrl) {
    return res.status(500).json({ error: "BACKEND_URL not set" });
  }

  try {
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    const json = await response.json();

    // Directly forward backend response
    return res.status(200).json(json);

  } catch (err) {
    console.error("Proxy error:", err);
    return res.status(500).json({ error: String(err) });
  }
}


