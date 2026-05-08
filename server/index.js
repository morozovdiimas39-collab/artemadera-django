const express = require('express');
const cors = require('cors');
const db = require('./database');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 3001;

// --- GALLERY API ---

app.get('/api/gallery', (req, res) => {
  db.all('SELECT * FROM gallery', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post('/api/gallery', (req, res) => {
  const { src, title, category, span } = req.body;
  if (!src || !title || !category) return res.status(400).json({ error: 'Missing required fields' });
  
  const spanValue = span || 'col-span-1 row-span-1';
  db.run('INSERT INTO gallery (src, title, category, span) VALUES (?, ?, ?, ?)', [src, title, category, spanValue], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ id: this.lastID, src, title, category, span: spanValue });
  });
});

app.delete('/api/gallery/:id', (req, res) => {
  const id = req.params.id;
  db.run('DELETE FROM gallery WHERE id = ?', id, function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ deleted: this.changes > 0 });
  });
});


// --- BLOG API ---

app.get('/api/blog', (req, res) => {
  db.all('SELECT * FROM blog', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post('/api/blog', (req, res) => {
  const { title, excerpt, date, img, readTime, content } = req.body;
  if (!title || !excerpt || !img) return res.status(400).json({ error: 'Missing required fields' });
  
  const postDate = date || new Date().toLocaleDateString('ru-RU');
  const postReadTime = readTime || '5 мин';
  
  db.run('INSERT INTO blog (title, excerpt, date, img, readTime, content) VALUES (?, ?, ?, ?, ?, ?)', 
    [title, excerpt, postDate, img, postReadTime, content || ''], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ id: this.lastID, title, excerpt, date: postDate, img, readTime: postReadTime });
  });
});

app.delete('/api/blog/:id', (req, res) => {
  const id = req.params.id;
  db.run('DELETE FROM blog WHERE id = ?', id, function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ deleted: this.changes > 0 });
  });
});

// --- LEADS API ---

app.post('/api/lead', (req, res) => {
  const { phone, type } = req.body;
  if (!phone || !type) return res.status(400).json({ error: 'Missing phone or type' });
  
  db.run('INSERT INTO leads (phone, type) VALUES (?, ?)', [phone, type], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ id: this.lastID, phone, type, status: 'new' });
  });
});

app.get('/api/leads', (req, res) => {
  db.all('SELECT * FROM leads ORDER BY created_at DESC', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.patch('/api/lead/:id', (req, res) => {
  const { status } = req.body;
  const id = req.params.id;
  db.run('UPDATE leads SET status = ? WHERE id = ?', [status, id], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ updated: this.changes > 0 });
  });
});

// --- START SERVER ---
app.listen(PORT, () => {
  console.log(`Admin Backend Server is running on http://localhost:${PORT}`);
});
