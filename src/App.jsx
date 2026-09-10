import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";

import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";

import Dashboard from "./pages/Dashboard";
import Analyze from "./pages/Analyze";
import Results from "./pages/Results";
import MapPage from "./pages/MapPage";
import Reports from "./pages/Reports";

function App() {
  const isGitHubPages = window.location.pathname.startsWith(
    "/AltCtrlElite_SonarDebrisDetection",
  );

  return (
    <BrowserRouter
      basename={isGitHubPages ? "/AltCtrlElite_SonarDebrisDetection" : "/"}
    >
      <div className="app">
        <Sidebar />

        <div className="main">
          <Topbar />

          <main className="content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analyze" element={<Analyze />} />
              <Route path="/results" element={<Results />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
