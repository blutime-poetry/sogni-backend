
const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const app = express();

app.use(cors());
app.use(express.json());

const POESIE_FILE = path.join(__dirname, 'poesie.json');

// Assicura che il file esista
if (!fs.existsSync(POESIE_FILE)) fs.writeFileSync(POESIE_FILE, '[]');

// Rotta di test
app.get('/api/status', (req, res) => {
  res.json({ status: 'online', message: 'API funzionante!', endpoints: { salva: 'POST /api/poesia', lista: 'GET /api/poesie' } });
});

// Rotta per salvare una poesia
app.post('/api/poesia', (req, res) => {
  const { nome, testo } = req.body;
  if (!testo) return res.status(400).json({ error: 'Testo mancante' });

  const poesie = JSON.parse(fs.readFileSync(POESIE_FILE));
  poesie.unshift({ nome: nome || 'Anonimo', testo, data: new Date().toISOString() });
  fs.writeFileSync(POESIE_FILE, JSON.stringify(poesie, null, 2));
  res.json({ success: true });
});

// Rotta per leggere le poesie
app.get('/api/poesie', (req, res) => {
  const poesie = JSON.parse(fs.readFileSync(POESIE_FILE));
  res.json(poesie);
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`Server attivo sulla porta ${PORT}`);
});
