import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  Upload,
  Image as ImageIcon,
  X,
  ScanSearch,
  ArrowRight,
  LoaderCircle,
} from "lucide-react";

function Analyze() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const inputRef = useRef(null);
  const navigate = useNavigate();

  const selectFile = (selectedFile) => {
    if (!selectedFile) return;

    const allowedTypes = ["image/png", "image/jpeg", "image/tiff"];

    if (allowedTypes.includes(selectedFile.type)) {
      setFile(selectedFile);

      if (selectedFile.type !== "image/tiff") {
        const previewUrl = URL.createObjectURL(selectedFile);
        setPreview(previewUrl);
      } else {
        setPreview(null);
      }
    } else {
      alert("Please select a PNG, JPG, JPEG or TIFF image.");
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    selectFile(e.dataTransfer.files[0]);
  };

  const removeFile = () => {
    if (preview) {
      URL.revokeObjectURL(preview);
    }

    setFile(null);
    setPreview(null);

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  const analyzeImage = () => {
    if (!file) return;

    setAnalyzing(true);

    // Temporary frontend simulation.
    // Later this will be replaced by the backend API.
    setTimeout(() => {
      sessionStorage.setItem("sonarFileName", file.name);

      if (preview) {
        sessionStorage.setItem("sonarImagePreview", preview);
      }

      navigate("/results");
    }, 2000);
  };

  return (
    <div className="analyze-page">
      <div className="page-heading">
        <span className="eyebrow">SONAR ANALYSIS</span>

        <h1>Analyze Side-Scan Sonar</h1>

        <p>
          Upload a sonar image to detect underwater marine debris and anomalies
          using AI.
        </p>
      </div>

      <section className="upload-card">
        {!file ? (
          <div
            className={`drop-zone ${dragging ? "dragging" : ""}`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".png,.jpg,.jpeg,.tif,.tiff"
              hidden
              onChange={(e) => selectFile(e.target.files[0])}
            />

            <div className="upload-icon">
              <Upload size={30} />
            </div>

            <h2>Upload Side-Scan Sonar Image</h2>

            <p>
              Drag and drop your sonar image here
              <br />
              or click to browse from your computer
            </p>

            <span className="supported">PNG • JPG • JPEG • TIFF</span>
          </div>
        ) : (
          <div className="preview-section">
            <div className="preview-header">
              <div>
                <h2>Selected Sonar Image</h2>
                <span>Ready for AI analysis</span>
              </div>

              {!analyzing && (
                <button
                  className="remove-file"
                  onClick={removeFile}
                  title="Remove image"
                >
                  <X size={18} />
                </button>
              )}
            </div>

            <div className="image-preview">
              {preview ? (
                <img src={preview} alt="Selected sonar" />
              ) : (
                <div className="tiff-preview">
                  <ImageIcon size={35} />

                  <strong>TIFF image selected</strong>

                  <span>Preview will be available after processing</span>
                </div>
              )}

              <div className="preview-overlay">
                <span>SONAR IMAGE</span>
              </div>
            </div>

            <div className="selected-file">
              <div className="file-icon">
                <ImageIcon size={25} />
              </div>

              <div className="file-info">
                <strong>{file.name}</strong>

                <span>{(file.size / 1024 / 1024).toFixed(2)} MB</span>
              </div>
            </div>
          </div>
        )}

        <div className="analyze-action">
          <div>
            {analyzing ? (
              <LoaderCircle size={20} className="loading-icon" />
            ) : (
              <ScanSearch size={20} />
            )}

            <div>
              <strong>
                {analyzing ? "Analyzing sonar image..." : "AI Detection"}
              </strong>

              <span>
                {analyzing
                  ? "Processing image for marine debris and anomalies"
                  : "Detect debris, anomalies and calculate confidence scores"}
              </span>
            </div>
          </div>

          <button
            className="primary-btn"
            disabled={!file || analyzing}
            onClick={analyzeImage}
          >
            {analyzing ? "Analyzing..." : "Analyze Image"}

            {!analyzing && <ArrowRight size={18} />}
          </button>
        </div>
      </section>

      <section className="analysis-info">
        <div className="info-card">
          <strong>01</strong>

          <h3>Upload</h3>

          <p>
            Select a side-scan sonar image captured during an underwater survey.
          </p>
        </div>

        <div className="info-card">
          <strong>02</strong>

          <h3>AI Processing</h3>

          <p>
            The detection model identifies potential man-made objects and
            anomalies.
          </p>
        </div>

        <div className="info-card">
          <strong>03</strong>

          <h3>Results</h3>

          <p>
            View detected objects, confidence scores and available location
            data.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Analyze;
