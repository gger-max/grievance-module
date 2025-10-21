import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'

export default function TrackPage() {
  const router = useRouter()
  const { id } = router.query
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!id) return
    fetch(`http://localhost:8000/api/grievances/${id}`)
      .then(res => {
        if (!res.ok) throw new Error('Not found')
        return res.json()
      })
      .then(setData)
      .catch(err => setError(err.message))
  }, [id])

  if (!id) return <p>Loading...</p>
  if (error) return <p style={{color:'red'}}>Error: {error}</p>
  if (!data) return <p>Loading grievance {id}...</p>

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Grievance Status</h1>
      <p><strong>ID:</strong> {data.id}</p>
      <p><strong>Status:</strong> {data.external_status || 'Pending'}</p>
      <p><strong>Note:</strong> {data.external_status_note || '-'}</p>
      <p><strong>Created:</strong> {new Date(data.created_at).toLocaleString()}</p>
    </div>
  )
}
