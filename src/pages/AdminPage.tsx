import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Trash2, Plus, Image as ImageIcon, FileText, CheckCircle2 } from 'lucide-react';
import { applySeo } from '../seo';

const API_URL = 'http://localhost:3001/api';

export default function AdminPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  
  const [activeTab, setActiveTab] = useState<'gallery' | 'blog'>('gallery');
  const [gallery, setGallery] = useState<any[]>([]);
  const [blog, setBlog] = useState<any[]>([]);

  // New item states
  const [newGalleryItem, setNewGalleryItem] = useState({ src: '', title: '', category: '', span: 'col-span-1 row-span-1' });
  const [newBlogPost, setNewBlogPost] = useState({ title: '', excerpt: '', img: '', readTime: '5 мин' });

  useEffect(() => {
    applySeo({ title: 'Панель управления | ArteMadera', description: 'Административная панель' });
    if (isAuthenticated) {
      fetchData();
    }
  }, [isAuthenticated]);

  const fetchData = async () => {
    try {
      const galRes = await fetch(`${API_URL}/gallery`);
      const galData = await galRes.json();
      setGallery(galData);

      const blogRes = await fetch(`${API_URL}/blog`);
      const blogData = await blogRes.json();
      setBlog(blogData);
    } catch (err) {
      console.error('Error fetching admin data:', err);
    }
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === 'admin123') { // Simple hardcoded auth for demonstration
      setIsAuthenticated(true);
    } else {
      alert('Неверный пароль');
    }
  };

  const handleAddGallery = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_URL}/gallery`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newGalleryItem)
      });
      if (res.ok) {
        setNewGalleryItem({ src: '', title: '', category: '', span: 'col-span-1 row-span-1' });
        fetchData();
      }
    } catch (err) { console.error(err); }
  };

  const handleDeleteGallery = async (id: number) => {
    if (!confirm('Удалить фото?')) return;
    try {
      const res = await fetch(`${API_URL}/gallery/${id}`, { method: 'DELETE' });
      if (res.ok) fetchData();
    } catch (err) { console.error(err); }
  };

  const handleAddBlog = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_URL}/blog`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newBlogPost)
      });
      if (res.ok) {
        setNewBlogPost({ title: '', excerpt: '', img: '', readTime: '5 мин' });
        fetchData();
      }
    } catch (err) { console.error(err); }
  };

  const handleDeleteBlog = async (id: number) => {
    if (!confirm('Удалить статью?')) return;
    try {
      const res = await fetch(`${API_URL}/blog/${id}`, { method: 'DELETE' });
      if (res.ok) fetchData();
    } catch (err) { console.error(err); }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-stone-950 flex items-center justify-center p-4 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-amber-500/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="glass-panel p-8 rounded-3xl w-full max-w-md relative z-10 border border-white/10">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Вход в Панель управления</h2>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-gray-400 text-sm mb-2">Пароль (admin123)</label>
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-black/50 border border-white/10 focus:border-amber-500 text-white outline-none"
              />
            </div>
            <button className="w-full bg-amber-600 hover:bg-amber-500 text-white py-3 rounded-xl font-bold transition-colors">
              Войти
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-stone-950 pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="flex flex-col sm:flex-row justify-between items-center mb-10 gap-4">
          <h1 className="text-4xl font-black text-white">Панель <span className="text-amber-500">управления</span></h1>
          <div className="flex gap-2 p-1 bg-white/5 rounded-full border border-white/10">
            <button onClick={() => setActiveTab('gallery')} className={`px-6 py-2 rounded-full text-sm font-bold transition-all ${activeTab === 'gallery' ? 'bg-amber-500 text-stone-950' : 'text-gray-400 hover:text-white'}`}>Галерея</button>
            <button onClick={() => setActiveTab('blog')} className={`px-6 py-2 rounded-full text-sm font-bold transition-all ${activeTab === 'blog' ? 'bg-amber-500 text-stone-950' : 'text-gray-400 hover:text-white'}`}>Блог</button>
          </div>
        </div>

        {activeTab === 'gallery' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1">
              <div className="glass-panel p-6 rounded-3xl border border-white/10 sticky top-24">
                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2"><ImageIcon className="w-5 h-5 text-amber-500" /> Добавить фото</h3>
                <form onSubmit={handleAddGallery} className="space-y-4">
                  <input placeholder="URL изображения (напр. /after.jpg)" value={newGalleryItem.src} onChange={e => setNewGalleryItem({...newGalleryItem, src: e.target.value})} required className="w-full px-4 py-3 rounded-xl bg-black/50 border border-white/10 focus:border-amber-500 text-white outline-none text-sm" />
                  <input placeholder="Название" value={newGalleryItem.title} onChange={e => setNewGalleryItem({...newGalleryItem, title: e.target.value})} required className="w-full px-4 py-3 rounded-xl bg-black/50 border border-white/10 focus:border-amber-500 text-white outline-none text-sm" />
                  <input placeholder="Категория" value={newGalleryItem.category} onChange={e => setNewGalleryItem({...newGalleryItem, category: e.target.value})} required className="w-full px-4 py-3 rounded-xl bg-black/50 border border-white/10 focus:border-amber-500 text-white outline-none text-sm" />
                  <select value={newGalleryItem.span} onChange={e => setNewGalleryItem({...newGalleryItem, span: e.target.value})} className="w-full px-4 py-3 rounded-xl bg-black/50 border border-white/10 focus:border-amber-500 text-white outline-none text-sm">
                    <option value="col-span-1 row-span-1">Обычная (1x1)</option>
                    <option value="col-span-1 md:col-span-2 row-span-1">Широкая (2x1)</option>
                    <option value="col-span-1 row-span-2">Высокая (1x2)</option>
                    <option value="col-span-1 md:col-span-2 row-span-2">Большая (2x2)</option>
                  </select>
                  <button type="submit" className="w-full bg-amber-500/20 text-amber-400 hover:bg-amber-500 hover:text-stone-950 py-3 rounded-xl font-bold transition-all border border-amber-500/50 flex items-center justify-center gap-2">
                    <Plus className="w-4 h-4" /> Добавить
                  </button>
                </form>
              </div>
            </div>
            <div className="lg:col-span-2">
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {gallery.map(item => (
                  <div key={item.id} className="glass-panel p-2 rounded-2xl border border-white/10 group relative">
                    <img src={item.src} alt={item.title} className="w-full h-32 object-cover rounded-xl mb-2" />
                    <div className="px-2 pb-2">
                      <p className="text-sm font-bold text-white truncate">{item.title}</p>
                      <p className="text-xs text-gray-500">{item.category}</p>
                    </div>
                    <button onClick={() => handleDeleteGallery(item.id)} className="absolute top-4 right-4 w-8 h-8 bg-red-500/80 hover:bg-red-500 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'blog' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1">
              <div className="glass-panel p-6 rounded-3xl border border-white/10 sticky top-24">
                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2"><FileText className="w-5 h-5 text-amber-500" /> Новая статья</h3>
                <form onSubmit={handleAddBlog} className="space-y-4">
                  <input placeholder="URL обложки" value={newBlogPost.img} onChange={e => setNewBlogPost({...newBlogPost, img: e.target.value})} required className="w-full px-4 py-3 rounded-xl bg-black/50 border border-white/10 focus:border-amber-500 text-white outline-none text-sm" />
                  <input placeholder="Заголовок" value={newBlogPost.title} onChange={e => setNewBlogPost({...newBlogPost, title: e.target.value})} required className="w-full px-4 py-3 rounded-xl bg-black/50 border border-white/10 focus:border-amber-500 text-white outline-none text-sm" />
                  <textarea placeholder="Краткое описание" value={newBlogPost.excerpt} onChange={e => setNewBlogPost({...newBlogPost, excerpt: e.target.value})} required className="w-full px-4 py-3 rounded-xl bg-black/50 border border-white/10 focus:border-amber-500 text-white outline-none text-sm h-24 resize-none" />
                  <button type="submit" className="w-full bg-amber-500/20 text-amber-400 hover:bg-amber-500 hover:text-stone-950 py-3 rounded-xl font-bold transition-all border border-amber-500/50 flex items-center justify-center gap-2">
                    <Plus className="w-4 h-4" /> Опубликовать
                  </button>
                </form>
              </div>
            </div>
            <div className="lg:col-span-2 space-y-4">
              {blog.map(post => (
                <div key={post.id} className="glass-panel p-4 rounded-2xl border border-white/10 flex items-center justify-between group">
                  <div className="flex items-center gap-4">
                    <img src={post.img} alt={post.title} className="w-16 h-16 object-cover rounded-xl" />
                    <div>
                      <p className="text-xs text-amber-500 mb-1">{post.date} • {post.readTime}</p>
                      <h4 className="text-white font-bold">{post.title}</h4>
                    </div>
                  </div>
                  <button onClick={() => handleDeleteBlog(post.id)} className="w-10 h-10 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-xl flex items-center justify-center transition-colors">
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
