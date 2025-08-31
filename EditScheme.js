import React, { useState } from 'react';
import axios from 'axios';

export default function EditScheme({ scheme, onDone }){
  const [form, setForm] = useState(scheme || { code:'', category:'', min_age:'', max_age:'', official_url:'', active:true });

  async function save(){
    if(scheme && scheme.id){
      await axios.put('/api/admin/schemes/'+scheme.id, form);
    } else {
      await axios.post('/api/admin/schemes', form);
    }
    if(onDone) onDone();
  }

  return (
    <div>
      <h3>{scheme ? 'Edit' : 'Create'} Scheme</h3>
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr', gap:8}}>
        <input placeholder="code" value={form.code} onChange={e=>setForm({...form, code:e.target.value})} />
        <input placeholder="category" value={form.category} onChange={e=>setForm({...form, category:e.target.value})} />
        <input placeholder="min_age" value={form.min_age} onChange={e=>setForm({...form, min_age:e.target.value})} />
        <input placeholder="max_age" value={form.max_age} onChange={e=>setForm({...form, max_age:e.target.value})} />
        <input placeholder="official_url" value={form.official_url} onChange={e=>setForm({...form, official_url:e.target.value})} />
      </div>
      <div style={{marginTop:8}}>
        <button onClick={save}>Save</button>
        <button style={{marginLeft:8}} onClick={()=>{ if(onDone) onDone(); }}>Cancel</button>
      </div>
    </div>
  )
}
