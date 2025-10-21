export default function Home() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '2rem' }}>
      <h1>Grievance / Feedback Form</h1>
      <p>Please fill in the form below. You may submit anonymously.</p>
      <iframe
        src="/typebot-grievance-flow.html"
        width="100%"
        height="700px"
        style={{ border: '1px solid #ccc', borderRadius: '8px' }}
      />
    </div>
  )
}
