"use client";

async function checkHealth() {
  const response = await fetch("http://localhost:8000/health");
  const data = await response.json();
  console.log(data);
}

export default function Home() {
  return (
    <main className="hero-section">
      <h1 className="hero-title">Welcome to the Future</h1>
      <p className="hero-subtitle">
        A stunning Next.js baseline template engineered for ultimate performance and visual excellence.
        Start building your next masterpiece.
      </p>

      <button className="btn btn-primary" onClick={checkHealth}>
        Check Health
      </button>

      <div className="button-group">
        <button className="btn btn-primary">Get Started</button>
        <button className="btn btn-secondary">Read Docs</button>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <span className="feature-icon">✨</span>
          <h3 className="feature-title">Premium Design</h3>
          <p className="text-muted">
            Carefully crafted gradient typography, sleek glassmorphism panels, and smooth animations right out of the box.
          </p>
        </div>

      
        <div className="feature-card">
          <span className="feature-icon">⚡</span>
          <h3 className="feature-title">Next.js App Router</h3>
          <p className="text-muted">
            Utilizes the latest features of Next.js for blazing fast rendering and a smooth developer experience.
          </p>
        </div>

        <div className="feature-card">
          <span className="feature-icon">🎨</span>
          <h3 className="feature-title">Vanilla CSS Architecture</h3>
          <p className="text-muted">
            Engineered with a powerful CSS variables system that avoids unneeded dependencies and keeps your build lean.
          </p>
        </div>
      </div>
    </main>
  );
}
