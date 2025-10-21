export const dynamic = 'force-dynamic';
const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

async function getData(id: string) {
  const res = await fetch(`${API}/api/grievances/${encodeURIComponent(id)}`, { cache: 'no-store' });
  if (!res.ok) {
    return null;
  }
  return res.json();
}

export default async function TrackIdPage({ params }: { params: { id: string }}) {
  const data = await getData(params.id);
  return (
    <main>
      <h2>Track: {params.id}</h2>
      {!data ? (
        <p>Not found or error fetching this grievance.</p>
      ) : (
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
      <div style={{marginTop: 24}}>
        <a href="/track">Go to Track search</a>
      </div>
    </main>
  );
}
