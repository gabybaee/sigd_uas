const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/data/ekspedisi', (req, res) => {
  const filePath = path.join(__dirname, 'data', 'ekspedisi_east.geojson');
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  res.json(data);
});

app.get('/api/stats/penyedia', (req, res) => {
  const filePath = path.join(__dirname, 'data', 'ekspedisi_east.geojson');
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

  const jumlah = {
    Pos: 0,
    JNE: 0,
    'J&T': 0,
    SiCepat: 0,
    lainnya: 0
  };

  data.features.forEach((fitur) => {
    const penyedia = fitur.properties.penyedia;

    if (penyedia === 'Pos' || penyedia === 'JNE' || penyedia === 'J&T' || penyedia === 'SiCepat') {
      jumlah[penyedia] += 1;
    } else {
      jumlah.lainnya += 1;
    }
  });

  res.json(jumlah);
});

app.post('/api/feature/zona', (req, res) => {
  const fitur = req.body;

  if (!fitur || fitur.type !== 'Feature' || !fitur.geometry || fitur.geometry.type !== 'Polygon') {
    return res.status(400).json({ error: 'Body harus berupa GeoJSON Feature dengan geometri Polygon.' });
  }

  if (!fitur.properties) {
    fitur.properties = {};
  }

  const filePath = path.join(__dirname, 'data', 'zona_logistik.geojson');
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

  data.features.push(fitur);
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));

  res.status(201).json(fitur);
});

app.listen(PORT, () => {
  console.log(`Server jalan di http://localhost:${PORT}`);
});