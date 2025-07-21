import React, { useState } from "react";
import {
  Card,
  Button,
  Form,
  Spinner,
  Alert,
  Row,
  Col,
  Table,
} from "react-bootstrap";
import "./UploadTab.css";

const API_BASE_URL = "/api";

const PREDICTION_TARGETS = [
  {
    key: "wdbc_malignancy",
    name: "Malignancy (WDBC)",
    description: "Predict malignancy using the WDBC dataset.",
    batchEndpoint: "/batch-predict-wdbc-malignancy",
    sampleFile: "sample_wdbc_malignancy.csv",
    color: "purple",
    icon: "fas fa-star",
  },
  {
    key: "vital_status",
    name: "Vital Status",
    description: "Predict if a patient is alive or deceased.",
    batchEndpoint: "/batch-predict-vital-status",
    sampleFile: "sample_vital_status.csv",
    color: "primary",
    icon: "fas fa-heartbeat",
  },
  {
    key: "cancer_type",
    name: "Cancer Type",
    description: "Identify the primary type of cancer.",
    batchEndpoint: "/batch-predict-cancer-type",
    sampleFile: "sample_cancer_type.csv",
    color: "info",
    icon: "fas fa-microscope",
  },
  {
    key: "cancer_stage",
    name: "Cancer Stage",
    description: "Determine the extent of the disease.",
    batchEndpoint: "/batch-predict-stage",
    sampleFile: "sample_stage.csv",
    color: "success",
    icon: "fas fa-chart-line",
  },
  {
    key: "metastasis",
    name: "Metastasis",
    description: "Check if the cancer has spread to other parts of the body.",
    batchEndpoint: "/batch-predict-metastasis",
    sampleFile: "sample_metastasis.csv",
    color: "warning",
    icon: "fas fa-arrows-alt",
  },
  {
    key: "treatment_outcome",
    name: "Treatment Outcome",
    description: "Record the success or failure of a treatment.",
    batchEndpoint: "/batch-predict-treatment-outcome",
    sampleFile: "sample_treatment_outcome.csv",
    color: "danger",
    icon: "fas fa-clipboard-check",
  },
  {
    key: "treatment_type",
    name: "Treatment Type",
    description: "Specify the type of treatment received.",
    batchEndpoint: "/batch-predict-treatment-type",
    sampleFile: "sample_treatment_type.csv",
    color: "secondary",
    icon: "fas fa-pills",
  },
  {
    key: "clinical_trial",
    name: "Clinical Trial",
    description: "Indicate if the patient was part of a clinical trial.",
    batchEndpoint: "/batch-predict-clinical-trial",
    sampleFile: "sample_clinical_trial.csv",
    color: "primary",
    icon: "fas fa-flask",
  },
  {
    key: "age_at_index",
    name: "Age at Index",
    description: "Record the age of the patient at the time of the diagnosis.",
    batchEndpoint: "/batch-predict-age-at-index",
    sampleFile: "sample_age_at_index.csv",
    color: "info",
    icon: "fas fa-user-clock",
  },
  {
    key: "classification_of_tumor",
    name: "Tumor Classification",
    description: "Categorize the type of tumor.",
    batchEndpoint: "/batch-predict-classification-of-tumor",
    sampleFile: "sample_classification_of_tumor.csv",
    color: "success",
    icon: "fas fa-tag",
  },
  {
    key: "disease_response",
    name: "Disease Response",
    description: "Record the patient's response to treatment.",
    batchEndpoint: "/batch-predict-disease-response",
    sampleFile: "sample_disease_response.csv",
    color: "danger",
    icon: "fas fa-chart-bar",
  },
  {
    key: "tissue_or_organ_of_origin",
    name: "Tissue/Organ of Origin",
    description: "Specify the location of the primary tumor.",
    batchEndpoint: "/batch-predict-tissue-or-organ-of-origin",
    sampleFile: "sample_tissue_or_organ_of_origin.csv",
    color: "secondary",
    icon: "fas fa-map-marker-alt",
  },
];

function UploadTab() {
  const [file, setFile] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedTarget, setSelectedTarget] = useState("all_targets"); // Default to all

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setPredictions(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    const endpoint =
      selectedTarget === "all_targets"
        ? "/batch-predict"
        : PREDICTION_TARGETS.find((t) => t.key === selectedTarget)
            ?.batchEndpoint;

    if (!endpoint) {
      setError("Invalid target selected.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();
      setPredictions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadTemplate = (sampleFile) => {
    const link = document.createElement("a");
    link.href = `/${sampleFile}`;
    link.download = sampleFile;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container-fluid mt-4">
      <Row>
        <Col md={7}>
          <Card>
            <Card.Header as="h4" className="text-center">
              <i className="fas fa-cloud-upload-alt me-2"></i>
              Batch Upload & Predict
            </Card.Header>
            <Card.Body>
              <p className="text-center text-muted">
                Download a template, fill it out, and upload it for batch
                predictions.
              </p>

              <div className="mb-4">
                <h5 className="text-center">Download Batch Upload Templates</h5>
                <Row>
                  {PREDICTION_TARGETS.map((target) => (
                    <Col md={4} key={target.key} className="mb-3">
                      <Card className="text-center h-100">
                        <Card.Body>
                          <i
                            className={`${target.icon} fa-2x text-${target.color} mb-2`}
                          ></i>
                          <Card.Title>{target.name}</Card.Title>
                          <Card.Text style={{ fontSize: "0.9rem" }}>
                            {target.description}
                          </Card.Text>
                          <Button
                            variant={`outline-${target.color}`}
                            size="sm"
                            onClick={() =>
                              handleDownloadTemplate(target.sampleFile)
                            }
                          >
                            Download Template
                          </Button>
                        </Card.Body>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </div>

              <div className="upload-section">
                <h5 className="text-center">Upload CSV File</h5>
                <Form.Group controlId="formFile" className="mb-3">
                  <Form.Control
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                  />
                  <Form.Text className="text-muted">
                    Upload a CSV file with feature columns. The first row should
                    contain headers.
                  </Form.Text>
                </Form.Group>
                <div className="d-grid">
                  <Button
                    variant="primary"
                    onClick={handleUpload}
                    disabled={loading || !file}
                  >
                    {loading ? (
                      <Spinner
                        as="span"
                        animation="border"
                        size="sm"
                        role="status"
                        aria-hidden="true"
                      />
                    ) : (
                      "Predict All Targets"
                    )}
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={5}>
          <Card>
            <Card.Header as="h4" className="text-center">
              <i className="fas fa-poll me-2"></i>
              Batch Results
            </Card.Header>
            <Card.Body style={{ minHeight: "400px" }}>
              {loading && (
                <div className="text-center">
                  <Spinner animation="border" />
                </div>
              )}
              {error && <Alert variant="danger">{error}</Alert>}
              {predictions && (
                <div className="table-responsive">
                  <Table striped bordered hover responsive>
                    <thead>
                      <tr>
                        {Object.keys(predictions[0]).map((key) => (
                          <th key={key}>
                            {key.replace(/_/g, " ").toUpperCase()}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {predictions.map((row, index) => (
                        <tr key={index}>
                          {Object.values(row).map((val, i) => (
                            <td key={i}>
                              {typeof val === "number"
                                ? val.toFixed(4)
                                : String(val)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </div>
              )}
              {!predictions && !loading && !error && (
                <div className="text-center text-muted mt-5">
                  <i className="fas fa-file-excel fa-3x mb-3"></i>
                  <p>No batch predictions yet. Upload a file to see results.</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default UploadTab;
