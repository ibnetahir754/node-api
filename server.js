const express = require('express');
const cors = require('cors');

const app = express();
const port = 3001;

app.use(cors());

const servers = [
  { id: 1, title: 'Server A', status: 'healthy', region: 'us-east-1' },
  { id: 2, title: 'Server B', status: 'warning', region: 'eu-west-1' },
  { id: 3, title: 'Server C', status: 'healthy', region: 'ap-south-1' },
  { id: 4, title: 'Server D', status: 'critical', region: 'us-west-2' }
];

app.get('/health', (req, res) => {
  res.json({
    service: 'node-api',
    status: 'ok',
    time: new Date().toISOString()
  });
});

app.get('/data', (req, res) => {
  res.json({
    source: 'node-api',
    time: new Date().toISOString(),
    items: servers
  });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`node-api running on port ${port}`);
});