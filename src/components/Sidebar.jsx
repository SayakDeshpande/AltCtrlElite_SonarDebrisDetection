import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  ScanLine,
  FileSearch,
  Map,
  FileText,
  Waves,
} from "lucide-react";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">
          <Waves size={24} />
        </div>

        <div>
          <h2>AquaScan AI</h2>
          <span>Marine Intelligence</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/" className="nav-item">
          <LayoutDashboard size={20} />
          Dashboard
        </NavLink>

        <NavLink to="/analyze" className="nav-item">
          <ScanLine size={20} />
          Analyze Sonar
        </NavLink>

        <NavLink to="/results" className="nav-item">
          <FileSearch size={20} />
          Results
        </NavLink>

        <NavLink to="/map" className="nav-item">
          <Map size={20} />
          Detection Map
        </NavLink>

        <NavLink to="/reports" className="nav-item">
          <FileText size={20} />
          Reports
        </NavLink>
      </nav>

      <div className="sidebar-bottom">
        <span>AI-Powered</span>
        <strong>Cleaner Oceans</strong>
      </div>
    </aside>
  );
}

export default Sidebar;
