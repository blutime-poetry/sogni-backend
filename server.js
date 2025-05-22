
const express = require('express');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

const FILE_PATH = 'poesie.json';

// Rotta per ricevere poesie
app.post('/api/poesie', (req, res) => {
  const nuovaPoesia = req.body;
  if (!nuovaPoesia || !nuovaPoesia.testo) {
    return res.status(400).json({ message: "Poesia mancante" });
  }

  let poesie = [];
  if (fs.existsSync(FILE_PATH)) {
    poesie = JSON.parse(fs.readFileSync(FILE_PATH));
  }

  poesie.unshift({
    testo: nuovaPoesia.testo.trim(),
    data: new Date().toISOString()
  });

  fs.writeFileSync(FILE_PATH, JSON.stringify(poesie, null, 2));
  res.status(201).json({ message: "Poesia salvata" });
});

// Rotta per leggere tutte le poesie
app.get('/api/poesie', (req, res) => {
  if (!fs.existsSync(FILE_PATH)) {
    return res.json([]);
  }
  const poesie = JSON.parse(fs.readFileSync(FILE_PATH));
  res.json(poesie);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server attivo sulla porta ${port}`);
});
