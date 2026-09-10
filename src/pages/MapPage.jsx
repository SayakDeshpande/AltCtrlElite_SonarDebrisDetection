import { MapPin, Navigation, Target, AlertTriangle } from "lucide-react";

const detections = [
  {
    id: 1,
    type: "Ghost Net",
    confidence: 92,
    latitude: "18.5234",
    longitude: "72.8456",
  },
  {
    id: 2,
    type: "Pipe",
    confidence: 87,
    latitude: "18.5241",
    longitude: "72.8462",
  },
  {
    id: 3,
    type: "Tire",
    confidence: 78,
    latitude: "18.5239",
    longitude: "72.8448",
  },
  {
    id: 4,
    type: "Debris",
    confidence: 81,
    latitude: "18.5245",
    longitude: "72.8460",
  },
];

function MapPage() {
  return (
    <div className="map-page">
      <div className="page-heading">
        <span className="eyebrow">GEOSPATIAL INTELLIGENCE</span>

        <h1>Detection Map</h1>

        <p>
          View detected marine debris and anomalies based on their geographic
          coordinates.
        </p>
      </div>

      <section className="map-layout">
        <div className="map-card">
          <div className="map-header">
            <div>
              <h2>Detected Locations</h2>
              <span>Side-scan sonar detection coordinates</span>
            </div>

            <div className="map-status">
              <span></span>4 detections
            </div>
          </div>

          <div className="large-map">
            <div className="map-grid"></div>

            <div className="map-water-lines"></div>

            {detections.map((item, index) => (
              <div
                key={item.id}
                className={`map-marker marker-${index + 1}`}
                title={`${item.type} - ${item.confidence}%`}
              >
                <MapPin size={30} />
              </div>
            ))}

            <div className="map-center-label">
              <Navigation size={15} />
              SONAR SURVEY AREA
            </div>
          </div>
        </div>

        <div className="map-side">
          <div className="map-summary">
            <div className="summary-icon">
              <Target size={21} />
            </div>

            <div>
              <strong>4</strong>
              <span>Total Detections</span>
            </div>
          </div>

          <div className="map-summary">
            <div className="summary-icon">
              <AlertTriangle size={21} />
            </div>

            <div>
              <strong>92%</strong>
              <span>Highest Confidence</span>
            </div>
          </div>

          <div className="location-list">
            <div className="list-header">
              <h2>Detection Locations</h2>
              <span>Coordinates</span>
            </div>

            {detections.map((item) => (
              <div className="location-item" key={item.id}>
                <div className="location-icon">
                  <MapPin size={17} />
                </div>

                <div className="location-info">
                  <strong>{item.type}</strong>

                  <span>
                    {item.latitude}° N, {item.longitude}° E
                  </span>
                </div>

                <b>{item.confidence}%</b>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default MapPage;
