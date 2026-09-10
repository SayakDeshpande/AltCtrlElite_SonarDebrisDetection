import { Link } from "react-router-dom";
import { UserCircle, Waves } from "lucide-react";

function Topbar() {
  const scrollToSection = (id) => {
    const section = document.getElementById(id);

    if (section) {
      section.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

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

        <button onClick={() => scrollToSection("about")}>About</button>

        <button onClick={() => scrollToSection("how-it-works")}>
          How It Works
        </button>
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
