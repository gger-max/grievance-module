export const metadata = {
  title: "Grievance System",
  description: "Anonymous grievance intake and tracking"
};
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{fontFamily: 'Inter, system-ui, Arial', margin: 0}}>
        <div style={{maxWidth: 900, margin: '0 auto', padding: '24px'}}>
          <header style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 24}}>
            <h1 style={{margin: 0}}>Grievance FrontEnd</h1>
            <nav style={{display:'flex', gap: 16}}>
              <a href="/" style={{textDecoration:'none'}}>Report</a>
              <a href="/track" style={{textDecoration:'none'}}>Track</a>
            </nav>
          </header>
          {children}
          <footer style={{marginTop: 48, fontSize: 12, color: '#666'}}>
            <hr/>
            <div>© {new Date().getFullYear()} Grievance System</div>
          </footer>
        </div>
      </body>
    </html>
  );
}
