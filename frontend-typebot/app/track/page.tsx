'use client';
import { useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function TrackPage() {
  const [id, setId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [data, setData] = useState<any>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(''); setData(null); setLoading(true);
    try {
      const res = await fetch(`${API}/api/grievances/${encodeURIComponent(id)}`);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      const json = await res.json();
      setData(json);
    } catch (err: any) {
      setError(err?.message || 'Request failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <h2>Track a Grievance</h2>
      <form onSubmit={onSubmit} style={{display:'flex', gap: 12, marginTop: 12}}>
        <input
          type="text"
          placeholder="Enter your Grievance ID (e.g., GRV-01H...)"
          value={id}
          onChange={(e)=>setId(e.target.value)}
          style={{flex:1, padding: 10, border: '1px solid #ccc', borderRadius: 8}}
          required
        />
        <button type="submit" style={{padding: '10px 16px', borderRadius: 8, border: '1px solid #222', background:'#222', color:'#fff'}}>
          {loading ? 'Checking…' : 'Check'}
        </button>
      </form>

      {error && <div style={{marginTop:16, color: 'crimson'}}>Error: {error}</div>}
      {data && (
        <div style={{marginTop: 24, padding: 16, background:'#f8f8f8', borderRadius: 8}}>
          <h3>Status</h3>
          <p><b>ID:</b> {data.id}</p>
          <p><b>Created:</b> {new Date(data.created_at).toLocaleString()}</p>
          <p><b>External Status:</b> {data.external_status ?? 'N/A'}</p>
          <p><b>Note:</b> {data.external_status_note ?? '-'}</p>
          <p><b>Summary:</b> {data.summary ?? '-'}</p>
          <div style={{marginTop: 12}}>
            <a href={`${API}/api/grievances/${encodeURIComponent(data.id)}/receipt.pdf`} target="_blank">Download receipt (PDF)</a>
          </div>
        </div>
      )}
    </main>
  );
}
