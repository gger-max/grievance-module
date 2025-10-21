'use client';
import { useEffect } from 'react';

export default function Page() {
  useEffect(() => {
    // Load Typebot embed
    const script = document.createElement('script');
    script.src = "https://cdn.typebot.io/typebot-embed.min.js";
    script.async = true;
    script.onload = () => {
      // @ts-ignore
      if (window.Typebot) {
        // Initialize a bubble. Replace 'grievance-intake' with your hosted typebot name/id
        // @ts-ignore
        window.Typebot.initBubble({ typebot: "grievance-intake", theme: { button: { size: 56 }}});
      }
    };
    document.body.appendChild(script);
    return () => { document.body.removeChild(script); };
  }, []);

  return (
    <main>
      <h2>Report a Grievance</h2>
      <p>
        Click the chat bubble (bottom-right) to start the guided, anonymous grievance form. 
        Or integrate a direct form here later.
      </p>
      <div style={{marginTop: 24, padding: 16, background: '#f8f8f8', borderRadius: 8}}>
        <h3>API endpoints</h3>
        <ul>
          <li>Create grievance: <code>POST {process.env.NEXT_PUBLIC_API_BASE_URL}/api/grievances</code></li>
          <li>Get by ID: <code>GET {process.env.NEXT_PUBLIC_API_BASE_URL}/api/grievances/{"{id}"}</code></li>
          <li>Receipt PDF: <code>GET {process.env.NEXT_PUBLIC_API_BASE_URL}/api/grievances/{"{id}"}/receipt.pdf</code></li>
        </ul>
      </div>
    </main>
  );
}
