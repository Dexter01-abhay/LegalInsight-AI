import { useState } from 'react';
import './index.css';

export default function App() {
  return (
    <div className="app-container landing-mode">
      <header>
        <div className="brand">
          <div className="brand-badge">AI</div>
          <div>
            <div className="brand-title">LegalInsight AI</div>
            <div className="brand-subtitle">Automated Legal Risk Analysis & Ingestion</div>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="hero-section">
          <h1>Enterprise Legal Document Intelligence</h1>
          <p>Scaffolding initialized. Multi-tenant authentication and analysis pipeline ready for integration.</p>
        </div>
      </main>
    </div>
  );
}
