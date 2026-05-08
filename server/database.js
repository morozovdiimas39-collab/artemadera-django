const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const dbPath = path.resolve(__dirname, 'database.sqlite');
const isNewDb = !fs.existsSync(dbPath);

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database', err.message);
  } else {
    console.log('Connected to SQLite database.');
    if (isNewDb) {
      initDatabase();
    }
  }
});

function initDatabase() {
  db.serialize(() => {
    // Create Gallery Table
    db.run(`CREATE TABLE IF NOT EXISTS gallery (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      src TEXT NOT NULL,
      title TEXT NOT NULL,
      category TEXT NOT NULL,
      span TEXT
    )`);

    // Create Blog Table
    db.run(`CREATE TABLE IF NOT EXISTS blog (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      excerpt TEXT NOT NULL,
      date TEXT NOT NULL,
      img TEXT NOT NULL,
      readTime TEXT NOT NULL,
      content TEXT
    )`);

    // Create Leads Table
    db.run(`CREATE TABLE IF NOT EXISTS leads (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      phone TEXT NOT NULL,
      type TEXT NOT NULL,
      status TEXT DEFAULT 'new',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // Insert Initial Data
    const initialGallery = [
      { src: '/portfolio-1.jpg', title: 'Шлифовка сруба', category: 'Шлифовка', span: 'col-span-1 md:col-span-2 row-span-2' },
      { src: '/portfolio-2.jpg', title: 'Покраска фасада', category: 'Покраска', span: 'col-span-1 row-span-1' },
      { src: '/portfolio-3.jpg', title: 'Теплый шов', category: 'Герметизация', span: 'col-span-1 row-span-1' },
      { src: '/before.jpg', title: 'До обработки', category: 'Реставрация', span: 'col-span-1 row-span-2' },
      { src: '/after.jpg', title: 'После обработки', category: 'Реставрация', span: 'col-span-1 md:col-span-2 row-span-1' },
      { src: '/service-1.jpg', title: 'Подготовка бруса', category: 'Шлифовка', span: 'col-span-1 row-span-1' },
    ];

    const stmtGallery = db.prepare('INSERT INTO gallery (src, title, category, span) VALUES (?, ?, ?, ?)');
    for (const item of initialGallery) {
      stmtGallery.run(item.src, item.title, item.category, item.span);
    }
    stmtGallery.finalize();

    const initialBlog = [
      { title: 'Как выбрать масло для дерева: топ-5 ошибок', excerpt: 'Разбираем популярные бренды и частые ошибки при самостоятельной покраске фасада.', date: '12 Апреля 2026', img: '/service-2.jpg', readTime: '5 мин' },
      { title: 'Когда лучше делать теплый шов?', excerpt: 'Сезонность работ по герметизации: почему весна и осень — идеальное время.', date: '08 Апреля 2026', img: '/service-3.jpg', readTime: '4 мин' },
      { title: 'Почему сруб темнеет и как это остановить', excerpt: 'Влияние УФ-лучей и влаги на древесину. Эффективные методы защиты.', date: '02 Апреля 2026', img: '/before.jpg', readTime: '6 мин' },
    ];

    const stmtBlog = db.prepare('INSERT INTO blog (title, excerpt, date, img, readTime) VALUES (?, ?, ?, ?, ?)');
    for (const post of initialBlog) {
      stmtBlog.run(post.title, post.excerpt, post.date, post.img, post.readTime);
    }
    stmtBlog.finalize();
    console.log('Database initialized with default data.');
  });
}

module.exports = db;
