const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

// Inside docker-compose, "backend" resolves via the shared network.
// When running outside Docker, set BACKEND_URL=http://localhost:5000
const BACKEND_URL = process.env.BACKEND_URL || "http://backend:5000";

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/submittodoitem", async (req, res) => {
  const { itemName, itemDescription } = req.body;

  try {
    const response = await axios.post(`${BACKEND_URL}/submittodoitem`, {
      itemName,
      itemDescription
    });

    res.send(`
      <!DOCTYPE html>
      <html>
      <head><title>Submitted</title></head>
      <body style="font-family: sans-serif; max-width: 600px; margin: 60px auto;">
        <h2>Item submitted successfully</h2>
        <p><strong>Backend response:</strong></p>
        <pre>${JSON.stringify(response.data, null, 2)}</pre>
        <a href="/">Add another item</a>
      </body>
      </html>
    `);
  } catch (err) {
    res.status(500).send(`
      <!DOCTYPE html>
      <html>
      <head><title>Error</title></head>
      <body style="font-family: sans-serif; max-width: 600px; margin: 60px auto;">
        <h2>Error submitting item</h2>
        <p>${err.message}</p>
        <a href="/">Go back</a>
      </body>
      </html>
    `);
  }
});

app.listen(PORT, () => {
  console.log(`Frontend server running on port ${PORT}`);
  console.log(`Forwarding submissions to backend at ${BACKEND_URL}`);
});
