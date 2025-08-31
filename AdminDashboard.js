import React, { useEffect, useState } from 'react';
import axios from 'axios';
import EditScheme from './EditScheme';
import ManageTranslations from './ManageTranslations';

export default function AdminDashboard(){
  const [schemes, setSchemes] = useState([]);
  const [selected, setSelected] = useState(null);
  const [mode, setMode] = useState('list');

  useEffect(()=>{ fetchSchemes() }, []);

  async function fetchSchemes(){
    const res = await axios.get('/api/schemes', { params:{ per_page: 100 } });
    setSchemes(res.data.items || []);
  }

  return (
    <div style={{padding:20}}>
      <h2>Admin - Schemes</h2>
      <div style={{display:'flex', gap:20}}>
        <div style={{flex:1}}>
          <button onClick={()=>{ setSelected(null); setMode('create') }}>+ New Scheme</button>
          <ul>
            {schemes.map(s=>(
              <li key={s.id} style={{marginTop:8}}>
                <a href="#" onClick={(e)=>{e.preventDefault(); setSelected(s); setMode('edit')}}>{s.title || s.code}</a>
                <button style={{marginLeft:8}} onClick={async ()=>{ await axios.delete('/api/admin/schemes/'+s.id); fetchSchemes(); }}>Delete</button>
                <button style={{marginLeft:8}} onClick={()=>{ setSelected(s); setMode('translations') }}>Translations</button>
              </li>
            ))}
          </ul>
        </div>
        <div style={{flex:2}}>
          {mode==='list' && <div>Select a scheme to edit</div>}
          {mode==='create' && <EditScheme onDone={()=>{ setMode('list'); fetchSchemes(); }} />}
          {mode==='edit' && selected && <EditScheme scheme={selected} onDone={()=>{ setMode('list'); fetchSchemes(); }} />}
          {mode==='translations' && selected && <ManageTranslations scheme={selected} />}
        </div>
      </div>
    </div>
  )
}
