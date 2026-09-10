import { Link } from "react-router-dom";
import { UserCircle, Waves } from "lucide-react";

function Topbar() {
  return (
    <header className="topbar">
      <div className="topbar-brand">
        <Waves size={21} />

        <div>
          <strong>AquaScan AI</strong>
          <span>Underwater Marine Intelligence</span>
        </div>
      </div>

      <nav className="topbar-nav">
        <Link to="/">Home</Link>
        <a href="/#about">About</a>
        <a href="/#how-it-works">How It Works</a>
      </nav>

      <div className="topbar-actions">
        <div className="status">
          <span className="status-dot"></span>
          System Ready
        </div>

        <button className="profile-button" title="Profile" type="button">
          <UserCircle size={30} />
        </button>
      </div>
    </header>
  );
}

export default Topbar;
