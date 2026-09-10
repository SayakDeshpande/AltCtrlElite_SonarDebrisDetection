import { UserCircle, Waves } from "lucide-react";
import { Link } from "react-router-dom";

function Topbar() {
  return (
    <header className="topbar">
      <Link to="/" className="topbar-brand">
        <Waves size={21} />

        <div>
          <strong>AquaScan AI</strong>
          <span>Underwater Marine Intelligence</span>
        </div>
      </Link>

      <nav className="topbar-nav">
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#how-it-works">How It Works</a>
      </nav>

      <div className="topbar-actions">
        <div className="status">
          <span className="status-dot"></span>
          System Ready
        </div>

        <button className="profile-button" title="Profile">
          <UserCircle size={30} />
        </button>
      </div>
    </header>
  );
}

export default Topbar;
