import React, { useState } from 'react';
import './i18n';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

function App(){
  const { t, i18n } = useTranslation();
  const [q, setQ] = useState('');
  const [items, setItems] = useState([]);
  const [lang, setLang] = useState('en');

  async function search(){
    const res = await axios.get('/api/schemes', { params: { q, lang } });
    setItems(res.data.items || []);
  }

  async function recommend(){
    const profile = { age: 24, income: 50000, state: 'TN', lang };
    const res = await axios.post('/api/recommend', profile);
    setItems(res.data.items || []);
  }

  function changeLang(l){
    i18n.changeLanguage(l);
    setLang(l);
    search();
  }

  return (
    <div style={{padding:20, maxWidth:900, margin:'0 auto'}}>
      <header style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <h1>Smart Scheme Advisor</h1>
        <select value={lang} onChange={e=>changeLang(e.target.value)}>
          <option value="en">English</option>
          <option value="hi">हिंदी</option>
        </select>
      </header>

      <div style={{display:'flex',gap:8, marginTop:12}}>
        <input style={{flex:1,padding:8}} placeholder={t('search_placeholder')} value={q} onChange={e=>setQ(e.target.value)}/>
        <button onClick={search}>{t('search')}</button>
        <button onClick={recommend}>{t('recommend_button')}</button>
      </div>

      <main style={{marginTop:16}}>
        {items.length === 0 ? <div>{t('no_results')}</div> : items.map(s=>(
          <article key={s.id} style={{padding:12,border:'1px solid #ddd', borderRadius:6, marginBottom:8}}>
            <h2 style={{fontWeight:700}}>{s.title}</h2>
            <p>{s.short_desc}</p>
            {s.official_url && <a href={s.official_url} target="_blank" rel="noreferrer">Official page</a>}
          </article>
        ))}
      </main>
    </div>
  )
}

export default App;
