import {
  FileText,
  Download,
  CheckCircle2,
  Database,
  MapPin,
  Target,
} from "lucide-react";

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

function Reports() {
  const fileName = sessionStorage.getItem("sonarFileName") || "Sonar Image";

  const reportData = {
    project: "AquaScan AI",
    file: fileName,
    status: "Analysis Complete",
    total_detections: detections.length,
    detections: detections,
  };

  const downloadJSON = () => {
    const data = JSON.stringify(reportData, null, 2);
    const blob = new Blob([data], {
      type: "application/json",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "aquascan-report.json";
    link.click();

    URL.revokeObjectURL(url);
  };

  const downloadCSV = () => {
    const headers = ["Object Type", "Confidence", "Latitude", "Longitude"];

    const rows = detections.map((item) => [
      item.type,
      `${item.confidence}%`,
      item.latitude,
      item.longitude,
    ]);

    const csv = [headers.join(","), ...rows.map((row) => row.join(","))].join(
      "\n",
    );

    const blob = new Blob([csv], {
      type: "text/csv",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "aquascan-report.csv";
    link.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="reports-page">
      <div className="page-heading">
        <span className="eyebrow">DETECTION REPORTS</span>

        <h1>Analysis Report</h1>

        <p>Review and export the results generated from the sonar analysis.</p>
      </div>

      <section className="report-header-card">
        <div className="report-title">
          <div className="report-icon">
            <FileText size={25} />
          </div>

          <div>
            <h2>AquaScan AI Detection Report</h2>
            <span>{fileName}</span>
          </div>
        </div>

        <div className="report-complete">
          <CheckCircle2 size={17} />
          Analysis Complete
        </div>
      </section>

      <section className="report-summary">
        <div className="report-summary-card">
          <Target size={20} />

          <div>
            <strong>{detections.length}</strong>
            <span>Objects Detected</span>
          </div>
        </div>

        <div className="report-summary-card">
          <Target size={20} />

          <div>
            <strong>92%</strong>
            <span>Highest Confidence</span>
          </div>
        </div>

        <div className="report-summary-card">
          <MapPin size={20} />

          <div>
            <strong>4</strong>
            <span>Geo-tagged</span>
          </div>
        </div>

        <div className="report-summary-card">
          <Database size={20} />

          <div>
            <strong>JSON / CSV</strong>
            <span>Export Formats</span>
          </div>
        </div>
      </section>

      <section className="report-table-card">
        <div className="report-section-header">
          <div>
            <h2>Detection Details</h2>
            <span>Complete object classification and location data</span>
          </div>
        </div>

        <div className="report-table-wrap">
          <table className="report-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Object Type</th>
                <th>Confidence</th>
                <th>Latitude</th>
                <th>Longitude</th>
              </tr>
            </thead>

            <tbody>
              {detections.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>

                  <td>
                    <strong>{item.type}</strong>
                  </td>

                  <td>
                    <span className="report-confidence">
                      {item.confidence}%
                    </span>
                  </td>

                  <td>{item.latitude}° N</td>

                  <td>{item.longitude}° E</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="report-downloads">
        <div>
          <h2>Export Report</h2>

          <p>
            Download the detection results for further analysis, storage or
            sharing.
          </p>
        </div>

        <div className="download-buttons">
          <button className="secondary-btn" onClick={downloadCSV}>
            <Download size={17} />
            Download CSV
          </button>

          <button className="primary-btn" onClick={downloadJSON}>
            <Download size={17} />
            Download JSON
          </button>
        </div>
      </section>
    </div>
  );
}

export default Reports;
