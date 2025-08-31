import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ManageTranslations({ scheme }){
  const [translations, setTranslations] = useState([]);
  const [newLang, setNewLang] = useState('hi');

  useEffect(()=>{ fetchTranslations() }, [scheme]);

  async function fetchTranslations(){
    if(!scheme) return;
    // naive: fetch scheme translations by getting scheme details from /api/schemes
    const res = await axios.get('/api/schemes/'+scheme.id);
    setTranslations(res.data ? (res.data.translations || []) : []);
  }

  async function addTranslation(){
    await axios.post('/api/admin/schemes/'+scheme.id+'/auto_translate', { lang: newLang });
    fetchTranslations();
  }

  return (
    <div>
      <h3>Translations for {scheme.title || scheme.code}</h3>
      <div>
        <label>Add language (auto-translate stub): </label>
        <select value={newLang} onChange={e=>setNewLang(e.target.value)}>
          <option value="hi">hi</option>
          <option value="ta">ta</option>
          <option value="en">en</option>
        </select>
        <button onClick={addTranslation}>Auto-translate</button>
      </div>

      <div style={{marginTop:12}}>
        <h4>Existing Translations (view-only in this stub)</h4>
        <ul>
          {translations.length===0 && <li>No translations found.</li>}
          {translations.map(t=>(
            <li key={t.lang}>
              <strong>{t.lang}</strong>: {t.title || '(no title)'}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
