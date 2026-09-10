import {
  CheckCircle2,
  MapPin,
  Target,
  Clock3,
  Download,
  Image as ImageIcon,
} from "lucide-react";

const detections = [
  {
    id: 1,
    type: "Ghost Net",
    confidence: 92,
    latitude: "18.5234",
    longitude: "72.8456",
    dimensions: "145 × 82 px",
    box: "box-one",
  },
  {
    id: 2,
    type: "Pipe",
    confidence: 87,
    latitude: "18.5241",
    longitude: "72.8462",
    dimensions: "132 × 60 px",
    box: "box-two",
  },
  {
    id: 3,
    type: "Tire",
    confidence: 78,
    latitude: "18.5239",
    longitude: "72.8448",
    dimensions: "98 × 98 px",
    box: "box-three",
  },
  {
    id: 4,
    type: "Debris",
    confidence: 81,
    latitude: "18.5245",
    longitude: "72.8460",
    dimensions: "76 × 54 px",
    box: "box-four",
  },
];

function Results() {
  const fileName = sessionStorage.getItem("sonarFileName") || "Sonar Image";

  const imagePreview = sessionStorage.getItem("sonarImagePreview");

  return (
    <div className="results-page">
      <div className="page-heading results-heading">
        <div>
          <span className="eyebrow">AI DETECTION RESULTS</span>

          <h1>Analysis Results</h1>

          <p>{fileName}</p>
        </div>

        <div className="analysis-status">
          <CheckCircle2 size={18} />
          Analysis Complete
        </div>
      </div>

      <section className="result-stats">
        <div className="result-stat">
          <Target size={21} />

          <div>
            <strong>4</strong>
            <span>Objects Detected</span>
          </div>
        </div>

        <div className="result-stat">
          <Target size={21} />

          <div>
            <strong>92%</strong>
            <span>Highest Confidence</span>
          </div>
        </div>

        <div className="result-stat">
          <MapPin size={21} />

          <div>
            <strong>4</strong>
            <span>Geo-tagged Objects</span>
          </div>
        </div>

        <div className="result-stat">
          <Clock3 size={21} />

          <div>
            <strong>12.6s</strong>
            <span>Processing Time</span>
          </div>
        </div>
      </section>

      <section className="results-grid">
        <div className="result-image-card">
          <div className="result-card-header">
            <div>
              <h2>Sonar Image</h2>

              <span>Detected objects highlighted by AI</span>
            </div>

            <button className="small-btn">
              <ImageIcon size={16} />
              Annotated
            </button>
          </div>

          <div className="sonar-result">
            {imagePreview ? (
              <img
                src={imagePreview}
                alt="Uploaded sonar"
                className="result-sonar-image"
              />
            ) : (
              <div className="sonar-texture"></div>
            )}

            <div className="result-image-overlay"></div>

            {detections.map((item) => (
              <div key={item.id} className={`detection-box ${item.box}`}>
                <span>
                  {item.type} · {item.confidence}%
                </span>
              </div>
            ))}

            <div className="sonar-center-line"></div>
          </div>
        </div>

        <div className="location-card">
          <div className="result-card-header">
            <div>
              <h2>Primary Location</h2>

              <span>Detected object coordinates</span>
            </div>

            <MapPin size={20} />
          </div>

          <div className="coordinate-box">
            <span>LATITUDE</span>
            <strong>18.5234° N</strong>

            <span>LONGITUDE</span>
            <strong>72.8456° E</strong>
          </div>

          <div className="mini-map">
            <div className="map-lines"></div>

            <MapPin className="result-map-pin" size={30} />
          </div>
        </div>
      </section>

      <section className="detections-card">
        <div className="result-card-header">
          <div>
            <h2>Detected Objects</h2>

            <span>AI classification and geospatial information</span>
          </div>
        </div>

        <div className="results-table-wrap">
          <table className="results-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Object Type</th>
                <th>Confidence</th>
                <th>Latitude</th>
                <th>Longitude</th>
                <th>Dimensions</th>
              </tr>
            </thead>

            <tbody>
              {detections.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>

                  <td>
                    <span className="object-name">{item.type}</span>
                  </td>

                  <td>
                    <span className="confidence">{item.confidence}%</span>
                  </td>

                  <td>{item.latitude}</td>

                  <td>{item.longitude}</td>

                  <td>{item.dimensions}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="result-actions">
        <button className="secondary-btn">
          <Download size={17} />
          Download CSV
        </button>

        <button className="secondary-btn">
          <Download size={17} />
          Download JSON
        </button>

        <button className="primary-btn">
          <ImageIcon size={17} />
          Download Annotated Image
        </button>
      </section>
    </div>
  );
}

export default Results;
