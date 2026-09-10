import {
  Upload,
  ScanSearch,
  MapPin,
  FileText,
  ArrowRight,
  Activity,
  Waves,
  ShieldCheck,
  Database,
} from "lucide-react";
import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div className="dashboard">
      {/* HOME SECTION */}
      <section className="hero" id="home">
        <div className="hero-content">
          <span className="eyebrow">UNDERWATER MARINE INTELLIGENCE</span>

          <h1>
            Detect Marine Debris
            <br />
            <span>with AI-powered sonar analysis.</span>
          </h1>

          <p>
            Upload side-scan sonar imagery and automatically identify underwater
            debris and anomalies with confidence scoring and geospatial
            information.
          </p>

          <Link to="/analyze" className="primary-btn">
            <Upload size={19} />
            Analyze Sonar
            <ArrowRight size={18} />
          </Link>
        </div>

        <div className="hero-visual">
          <div className="sonar-circle circle-one"></div>
          <div className="sonar-circle circle-two"></div>
          <div className="sonar-circle circle-three"></div>
          <div className="sonar-line"></div>
          <div className="sonar-point"></div>

          <div className="scan-label">
            <Activity size={16} />
            SONAR SCAN
          </div>
        </div>
      </section>

      {/* QUICK FEATURES */}
      <section className="dashboard-stats">
        <div className="stat-card">
          <div className="stat-icon">
            <ScanSearch size={22} />
          </div>

          <div>
            <strong>AI Detection</strong>
            <span>Automated object detection</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <MapPin size={22} />
          </div>

          <div>
            <strong>Geo-tagging</strong>
            <span>Location from sonar metadata</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <FileText size={22} />
          </div>

          <div>
            <strong>Smart Reports</strong>
            <span>JSON and CSV export</span>
          </div>
        </div>
      </section>

      {/* ABOUT SECTION */}
      <section className="dashboard-section about-section" id="about">
        <div className="section-heading">
          <div>
            <span className="eyebrow">ABOUT AQUASCAN AI</span>
            <h2>Making underwater detection smarter</h2>
          </div>
        </div>

        <div className="about-content">
          <div className="about-text">
            <p>
              AquaScan AI is an intelligent system designed to assist underwater
              surveys by analyzing side-scan sonar imagery and identifying
              potential marine debris and anomalies.
            </p>

            <p>
              The system helps reduce manual inspection effort by highlighting
              detected objects, providing confidence scores, and connecting
              detections with available geographic information.
            </p>

            <Link to="/analyze" className="secondary-btn">
              Start Analysis
              <ArrowRight size={17} />
            </Link>
          </div>

          <div className="about-features">
            <div className="about-feature">
              <div className="about-feature-icon">
                <Waves size={22} />
              </div>

              <div>
                <strong>Sonar Intelligence</strong>
                <span>Analyze complex underwater sonar imagery.</span>
              </div>
            </div>

            <div className="about-feature">
              <div className="about-feature-icon">
                <ShieldCheck size={22} />
              </div>

              <div>
                <strong>Detection Confidence</strong>
                <span>View confidence scores for detected objects.</span>
              </div>
            </div>

            <div className="about-feature">
              <div className="about-feature-icon">
                <Database size={22} />
              </div>

              <div>
                <strong>Structured Results</strong>
                <span>Organize detections for mapping and reporting.</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="dashboard-section" id="how-it-works">
        <div className="section-heading">
          <div>
            <span className="eyebrow">WORKFLOW</span>
            <h2>How AquaScan AI works</h2>
          </div>
        </div>

        <div className="workflow">
          <div className="workflow-card">
            <div className="step-number">01</div>
            <Upload size={25} />

            <h3>Upload</h3>

            <p>Upload side-scan sonar imagery in supported formats.</p>
          </div>

          <div className="workflow-card">
            <div className="step-number">02</div>
            <ScanSearch size={25} />

            <h3>Analyze</h3>

            <p>AI processes the image and detects potential anomalies.</p>
          </div>

          <div className="workflow-card">
            <div className="step-number">03</div>
            <MapPin size={25} />

            <h3>Locate</h3>

            <p>Detected objects are linked with their geographic location.</p>
          </div>

          <div className="workflow-card">
            <div className="step-number">04</div>
            <FileText size={25} />

            <h3>Report</h3>

            <p>Export detection results for further analysis.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
