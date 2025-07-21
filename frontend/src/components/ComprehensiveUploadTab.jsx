import React, { useState, useRef } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  Alert,
  Spinner,
  Table,
  Badge,
  ProgressBar,
  Accordion,
} from "react-bootstrap";
import Papa from "papaparse";
import "./ComprehensiveUploadTab.css"; // Import the new CSS file

const API_BASE_URL = "http://localhost:8000";

// ADDED: Centralized mapping for all prediction labels
const classLabelMappings = {
  wdbc_malignancy: ["Benign", "Malignant"],
  vital_status: ["Alive", "Dead"],
  cancer_type: [
    "Breast Invasive Ductal Carcinoma",
    "Breast Invasive Lobular Carcinoma",
    "Breast Mixed Ductal and Lobular Carcinoma",
    "Metaplastic Breast Cancer",
    "Breast Invasive Mixed Mucinous Carcinoma",
    "Solid Papillary Carcinoma with Invasion",
    "Mucinous Breast Cancer",
    "Invasive Micropapillary Carcinoma of the Breast",
    "Paget's Disease of the Nipple",
    "Infiltrating Ductal Carcinoma",
    "Intraductal Carcinoma, Noninfiltrating",
    "Adenocarcinoma with mixed subtypes",
    "Other",
    "Unspecified Ductal Carcinoma",
    "Unspecified Lobular Carcinoma",
    "Inflammatory Breast Cancer",
    "Triple-Negative Breast Cancer",
    "HER2-Positive Breast Cancer",
    "Hormone Receptor-Positive Breast Cancer",
    "Phyllodes Tumor",
    "Angiosarcoma",
    "Ductal Carcinoma in Situ (DCIS)",
    "Lobular Carcinoma in Situ (LCIS)",
    "Tubular Carcinoma",
    "Cribriform Carcinoma",
    "Medullary Carcinoma",
    "Secretory Carcinoma",
    "Adenoid Cystic Carcinoma",
    "Apocrine Carcinoma",
    "Neuroendocrine Tumor",
    "Primary Lymphoma",
    "Sarcoma",
    "Unspecified Malignant Neoplasm",
    "Unspecified Benign Neoplasm",
    "Unspecified Neoplasm",
    "Unknown",
    "Not Applicable",
  ],
  stage: [
    "Stage I",
    "Stage IA",
    "Stage IB",
    "Stage II",
    "Stage IIA",
    "Stage IIB",
    "Stage III",
    "Stage IIIA",
    "Stage IIIB",
    "Stage IIIC",
    "Stage IV",
    "Stage X",
    "Stage 0",
    "Stage 0is",
  ],
  metastasis: ["No Metastasis", "Metastasis, NOS"],
  age_at_index: ["<=50", ">50"],
  clinical_trial: ["No", "Yes"],
  treatment_type: [
    "Ancillary Treatment",
    "Bisphosphonate Therapy",
    "Brachytherapy, High Dose",
    "Brachytherapy, NOS",
    "Chemotherapy",
    "Hormone Therapy",
    "Immunotherapy",
    "Pharmaceutical Therapy, NOS",
    "Radiation Therapy, NOS",
    "Radiation, External Beam",
    "Radiation, Implants",
    "Radiation, Radioisotope",
    "Surgery, NOS",
    "Targeted Molecular Therapy",
  ],
  disease_response: ["TF-Tumor Free", "Unknown", "WT-With Tumor"],
  treatment_outcome: [
    "Complete Response",
    "Partial Response",
    "Progressive Disease",
    "Stable Disease",
    "Treatment Ongoing",
    "Unknown",
  ],
  classification_of_tumor: [
    "Adenocarcinoma, NOS",
    "Adenoid cystic carcinoma",
    "Apocrine adenocarcinoma",
    "Basal cell carcinoma, NOS",
    "Carcinoma in situ, NOS",
    "Carcinoma, NOS",
    "Clear cell carcinoma",
    "Combined small cell carcinoma",
    "Cribriform carcinoma, NOS",
    "Gastrointestinal stromal tumor, NOS",
    "Hodgkin lymphoma, NOS",
    "Infiltrating duct and lobular carcinoma",
    "Infiltrating duct carcinoma, NOS",
    "Infiltrating duct mixed with other types of carcinoma",
    "Infiltrating lobular carcinoma, NOS",
    "Infiltrating lobular mixed with other types of carcinoma",
    "Intraductal carcinoma, noninfiltrating, NOS",
    "Intraductal papillary adenocarcinoma with invasion",
    "Invasive micropapillary carcinoma",
    "Large cell neuroendocrine carcinoma",
    "Lobular carcinoma in situ, NOS",
    "Lobular carcinoma, NOS",
    "Malignant lymphoma, non-Hodgkin, NOS",
    "Malignant melanoma, NOS",
    "Medullary carcinoma, NOS",
    "Melanoma in situ",
    "Metaplastic carcinoma, NOS",
    "Mucinous adenocarcinoma",
    "Myelodysplastic syndrome, NOS",
    "Paget disease and infiltrating duct carcinoma of breast",
    "Papillary carcinoma, NOS",
    "Pheochromocytoma, NOS",
    "Phyllodes tumor, malignant",
    "Pleomorphic carcinoma",
    "Secretory carcinoma of breast",
    "Squamous cell carcinoma in situ, NOS",
    "Tubular adenocarcinoma",
  ],
  tissue_or_organ_of_origin: [
    "Abdomen, NOS",
    "Adrenal gland, NOS",
    "Bladder, NOS",
    "Bone marrow",
    "Bone, NOS",
    "Brain, NOS",
    "Breast, NOS",
    "Cervix uteri",
    "Colon, NOS",
    "Connective, subcutaneous and other soft tissues of thorax",
    "Endometrium",
    "Head, face or neck, NOS",
    "Intrathoracic lymph nodes",
    "Kidney, NOS",
    "Lip, NOS",
    "Liver",
    "Lower limb, NOS",
    "Lower-inner quadrant of breast",
    "Lower-outer quadrant of breast",
    "Lung, NOS",
    "Lymph node, NOS",
    "Lymph nodes of head, face and neck",
    "Other ill-defined sites",
    "Ovary",
    "Overlapping lesion of breast",
    "Rectum, NOS",
    "Skin of lower limb and hip",
    "Skin of scalp and neck",
    "Skin of trunk",
    "Skin, NOS",
    "Specified parts of peritoneum",
    "Stomach, NOS",
    "Thorax, NOS",
    "Thyroid gland",
    "Unknown",
    "Upper limb, NOS",
    "Upper-inner quadrant of breast",
    "Upper-outer quadrant of breast",
    "Uterus, NOS",
  ],
};

const ComprehensiveUploadTab = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [preview, setPreview] = useState(null);
  const [availableModels, setAvailableModels] = useState({});
  const fileInputRef = useRef(null);
  const [summary, setSummary] = useState(null); // Keep for structure
  const [detailedResults, setDetailedResults] = useState([]);

  const targets = [
    "wdbc_malignancy",
    "vital_status",
    "cancer_type",
    "stage",
    "metastasis",
    "treatment_outcome",
    "treatment_type",
    "clinical_trial",
    "age_at_index",
    "classification_of_tumor",
    "disease_response",
    "tissue_or_organ_of_origin",
  ];

  const targetLabels = {
    wdbc_malignancy: "Malignancy (WDBC)",
    vital_status: "Vital Status",
    cancer_type: "Cancer Type",
    stage: "Cancer Stage",
    metastasis: "Metastasis",
    treatment_outcome: "Treatment Outcome",
    treatment_type: "Treatment Type",
    clinical_trial: "Clinical Trial",
    age_at_index: "Age at Index",
    classification_of_tumor: "Tumor Classification",
    disease_response: "Disease Response",
    tissue_or_organ_of_origin: "Tissue/Organ of Origin",
  };

  React.useEffect(() => {
    fetchAvailableModels();
  }, []);

  const fetchAvailableModels = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/models`);
      const data = await response.json();
      setAvailableModels(data.available_models);
    } catch (error) {
      console.error("Error fetching models:", error);
    }
  };

  // DEFINITIVE FIX: Re-enabled and bulletproofed summary calculation
  const processBatchResults = (data) => {
    console.log("[DEBUG] 1. Raw data received from backend:", data); // DEBUG LOG
    if (!data || !Array.isArray(data.batch_predictions)) {
      console.error(
        "[DEBUG] CRITICAL: `data.batch_predictions` is not an array or data is null."
      );
      setError("Received invalid data structure from server.");
      setSummary(null);
      setDetailedResults([]);
      return;
    }

    const summaryData = {};
    targets.forEach((target) => {
      summaryData[target] = {
        success_rate: 0,
        avg_confidence: 0,
        top_predictions: {},
      };
    });

    data.batch_predictions.forEach((item) => {
      if (item && item.predictions) {
        targets.forEach((target) => {
          const pred = item.predictions[target];
          if (pred && !pred.error) {
            summaryData[target].success_rate++;
            summaryData[target].avg_confidence += pred.confidence || 0;
            const predValue = getDisplayLabel(target, pred.prediction); // Use the label for counting
            summaryData[target].top_predictions[predValue] =
              (summaryData[target].top_predictions[predValue] || 0) + 1;
          }
        });
      }
    });

    const totalCases = data.total_cases || data.batch_predictions.length;
    if (totalCases > 0) {
      targets.forEach((target) => {
        const successCount = summaryData[target].success_rate;
        if (successCount > 0) {
          summaryData[target].avg_confidence /= successCount;
        }
        summaryData[target].success_rate /= totalCases;
      });
    }

    setSummary(summaryData);
    setDetailedResults(data.batch_predictions);
    console.log(
      "[DEBUG] 2. State updated. Summary and detailedResults populated."
    );
  };

  // DEFINITIVE FIX: Bulletproof label mapping
  const getDisplayLabel = (target, value) => {
    try {
      if (value === null || value === undefined) return "N/A";
      const strValue = String(value); // Safely convert to string

      if (strValue === "N/A" || strValue === "Inconclusive") {
        return strValue;
      }
      const mapping = classLabelMappings[target];
      if (!mapping) return strValue;

      // Handle if the value is already the correct text label
      if (mapping.includes(strValue)) {
        return strValue;
      }
      // Handle if the value is an index needing mapping
      const numValue = parseInt(strValue, 10);
      if (!isNaN(numValue) && mapping[numValue]) {
        return mapping[numValue];
      }
      return strValue; // Fallback
    } catch (e) {
      console.error("[DEBUG] Error in getDisplayLabel:", e);
      return "Label Error"; // Return a specific error string
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setFile(file);
    setSummary(null); // CORRECTLY reset state
    setDetailedResults([]); // CORRECTLY reset state
    setError(null);

    // File preview logic
    Papa.parse(file, {
      header: true,
      preview: 5,
      complete: (results) => {
        setPreview(results);
      },
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const reader = new FileReader();
      reader.onload = (e) => {
        let text = e.target.result;
        if (text.charCodeAt(0) === 0xfeff) {
          text = text.slice(1);
        }
        Papa.parse(text, {
          header: true,
          delimiter: ",",
          skipEmptyLines: true,
          newline: "",
          worker: true,
          complete: async (results) => {
            console.log("PapaParse submit results:", results);
            console.log("First row keys:", Object.keys(results.data[0] || {}));
            console.log("First row raw:", results.data[0]);
            if (results.errors.length > 0) {
              setError(
                `CSV parsing errors: ${results.errors
                  .map((e) => e.message)
                  .join(", ")}`
              );
              setLoading(false);
              return;
            }

            // Convert data for API
            const data = results.data.map((row) => {
              const convertedRow = {};
              Object.keys(row).forEach((key) => {
                const value = row[key];
                convertedRow[key] = isNaN(value) ? value : parseFloat(value);
              });
              return convertedRow;
            });

            // Send to API
            const response = await fetch(`${API_BASE_URL}/batch-predict-all`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ data }),
            });

            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }

            const predictionData = await response.json();
            processBatchResults(predictionData); // Use the new processing function
          },
          error: (error) => {
            setError(`Error parsing CSV: ${error.message}`);
          },
        });
      };
      reader.readAsText(file, "utf-8");
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // DEFINITIVE FIX: Re-implement the download functionality
  const handleDownloadCsv = () => {
    if (!detailedResults || detailedResults.length === 0) return;

    // Create header row
    let headers = ["case_id"];
    targets.forEach((target) => {
      headers.push(`${targetLabels[target]}_prediction`);
      headers.push(`${targetLabels[target]}_confidence`);
    });
    let csvContent = headers.join(",") + "\n";

    // Create data rows
    detailedResults.forEach((result) => {
      if (!result || !result.predictions) return;

      let row = [result.case_id];
      targets.forEach((target) => {
        const pred = result.predictions[target];
        if (pred && !pred.error) {
          row.push(`"${getDisplayLabel(target, pred.prediction)}"`);
          row.push(
            pred.confidence !== undefined ? pred.confidence.toFixed(4) : "N/A"
          );
        } else {
          row.push("Error", "N/A");
        }
      });
      csvContent += row.join(",") + "\n";
    });

    // Create and trigger download
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    if (link.href) {
      URL.revokeObjectURL(link.href);
    }
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", "batch_prediction_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return "success";
    if (confidence >= 0.7) return "warning";
    return "danger";
  };

  const renderPredictionSummary = () => {
    if (!predictions) return null;

    const summary = {};
    targets.forEach((target) => {
      summary[target] = {
        total: 0,
        successful: 0,
        avgConfidence: 0,
        predictions: {},
      };
    });

    predictions.batch_predictions.forEach((caseData) => {
      targets.forEach((target) => {
        const prediction = caseData.predictions[target];
        summary[target].total++;

        if (prediction && !prediction.error) {
          summary[target].successful++;
          summary[target].avgConfidence += prediction.confidence;

          const pred = prediction.prediction;
          summary[target].predictions[pred] =
            (summary[target].predictions[pred] || 0) + 1;
        }
      });
    });

    targets.forEach((target) => {
      if (summary[target].successful > 0) {
        summary[target].avgConfidence /= summary[target].successful;
      }
    });

    return (
      <Card className="mb-4">
        <Card.Header>
          <h6 className="mb-0">Prediction Summary</h6>
        </Card.Header>
        <Card.Body>
          <Row>
            {targets.map((target) => (
              <Col md={6} lg={4} key={target} className="mb-3">
                <Card className="h-100">
                  <Card.Body>
                    <Card.Title className="h6">
                      {targetLabels[target]}
                    </Card.Title>
                    <div className="mb-2">
                      <small className="text-muted">
                        Success Rate: {summary[target].successful}/
                        {summary[target].total}
                      </small>
                    </div>
                    {summary[target].successful > 0 && (
                      <div className="mb-2">
                        <small className="text-muted">
                          Avg Confidence:{" "}
                          {(summary[target].avgConfidence * 100).toFixed(1)}%
                        </small>
                      </div>
                    )}
                    {Object.keys(summary[target].predictions).length > 0 && (
                      <div>
                        <small className="text-muted">Top Predictions:</small>
                        {Object.entries(summary[target].predictions)
                          .sort(([, a], [, b]) => b - a)
                          .slice(0, 3)
                          .map(([pred, count]) => (
                            <Badge key={pred} bg="secondary" className="me-1">
                              {pred}: {count}
                            </Badge>
                          ))}
                      </div>
                    )}
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Card.Body>
      </Card>
    );
  };

  return (
    <Container fluid className="mt-4">
      <Row>
        <Col xl={6}>
          <Card className="shadow-sm mb-4">
            <Card.Header>
              <h5 className="mb-0">
                <i className="fas fa-upload me-2"></i>
                Batch Upload & Predict All Targets
              </h5>
            </Card.Header>
            <Card.Body>
              {/* Downloadable batch template links */}
              <div className="mb-3">
                <h6>Download Batch Upload Templates:</h6>
                <Row className="g-3">
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-user-md fa-3x text-primary mb-2"></i>
                        <h6>Vital Status</h6>
                        <p className="text-muted small">
                          Predict if a patient is alive or deceased.
                        </p>
                        <Button
                          variant="outline-primary"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_vital_status.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-flask fa-3x text-info mb-2"></i>
                        <h6>Cancer Type</h6>
                        <p className="text-muted small">
                          Identify the primary type of cancer.
                        </p>
                        <Button
                          variant="outline-info"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_cancer_type.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-chart-bar fa-3x text-success mb-2"></i>
                        <h6>Cancer Stage</h6>
                        <p className="text-muted small">
                          Determine the extent of the disease.
                        </p>
                        <Button
                          variant="outline-success"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open("/batch_template_stage.csv", "_blank")
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-radiation fa-3x text-warning mb-2"></i>
                        <h6>Metastasis</h6>
                        <p className="text-muted small">
                          Check if the cancer has spread to other parts of the
                          body.
                        </p>
                        <Button
                          variant="outline-warning"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_metastasis.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-heartbeat fa-3x text-danger mb-2"></i>
                        <h6>Treatment Outcome</h6>
                        <p className="text-muted small">
                          Record the success or failure of a treatment.
                        </p>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_treatment_outcome.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-briefcase fa-3x text-secondary mb-2"></i>
                        <h6>Treatment Type</h6>
                        <p className="text-muted small">
                          Specify the type of treatment received.
                        </p>
                        <Button
                          variant="outline-secondary"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_treatment_type.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-hand-sparkles fa-3x text-primary mb-2"></i>
                        <h6>Clinical Trial</h6>
                        <p className="text-muted small">
                          Indicate if the patient was part of a clinical trial.
                        </p>
                        <Button
                          variant="outline-primary"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_clinical_trial.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-child fa-3x text-info mb-2"></i>
                        <h6>Age at Index</h6>
                        <p className="text-muted small">
                          Record the age of the patient at the time of the
                          diagnosis.
                        </p>
                        <Button
                          variant="outline-info"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_age_at_index.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-tags fa-3x text-success mb-2"></i>
                        <h6>Tumor Classification</h6>
                        <p className="text-muted small">
                          Categorize the type of tumor.
                        </p>
                        <Button
                          variant="outline-success"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_classification_of_tumor.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-heart fa-3x text-danger mb-2"></i>
                        <h6>Disease Response</h6>
                        <p className="text-muted small">
                          Record the patient's response to treatment.
                        </p>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_disease_response.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={4}>
                    <Card className="h-100">
                      <Card.Body className="text-center">
                        <i className="fas fa-map-marker-alt fa-3x text-secondary mb-2"></i>
                        <h6>Tissue/Organ of Origin</h6>
                        <p className="text-muted small">
                          Specify the location of the primary tumor.
                        </p>
                        <Button
                          variant="outline-secondary"
                          size="sm"
                          className="w-100"
                          onClick={() =>
                            window.open(
                              "/batch_template_tissue_or_organ_of_origin.csv",
                              "_blank"
                            )
                          }
                        >
                          Download Template
                        </Button>
                      </Card.Body>
                    </Card>
                  </Col>
                </Row>
              </div>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Upload CSV File</Form.Label>
                  <Form.Control
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    ref={fileInputRef}
                  />
                  <Form.Text className="text-muted">
                    Upload a CSV file with feature columns. The first row should
                    contain headers.
                  </Form.Text>
                </Form.Group>

                {/* DEFINITIVE FIX: Bulletproof file preview rendering */}
                {preview &&
                  preview.data &&
                  Array.isArray(preview.data) &&
                  preview.meta &&
                  Array.isArray(preview.meta.fields) && (
                    <div className="file-preview mb-3">
                      <h6 className="text-muted">
                        File Preview (First {preview.data.length} rows):
                      </h6>
                      <div
                        className="table-responsive"
                        style={{ maxHeight: "200px", overflowY: "auto" }}
                      >
                        <Table striped bordered hover size="sm">
                          <thead>
                            <tr>
                              {preview.meta.fields.map((field) => (
                                <th key={field}>{field}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {preview.data.map((row, i) => (
                              <tr key={i}>
                                {preview.meta.fields.map((field) => (
                                  <td key={field}>{row[field]}</td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </Table>
                      </div>
                    </div>
                  )}

                <div className="d-grid gap-2">
                  <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    disabled={loading || !file}
                  >
                    {loading ? (
                      <>
                        <Spinner
                          as="span"
                          animation="border"
                          size="sm"
                          role="status"
                          aria-hidden="true"
                          className="me-2"
                        />
                        Processing...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-magic me-2"></i>
                        Predict All Targets
                      </>
                    )}
                  </Button>
                </div>
              </Form>

              {error && (
                <Alert variant="danger" className="mt-3">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  {error}
                </Alert>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col xl={6}>
          <Card className="shadow-sm">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <h5 className="mb-0">
                <i className="fas fa-poll me-2"></i>Batch Results
              </h5>
              {summary && (
                <Button
                  variant="outline-success"
                  size="sm"
                  onClick={handleDownloadCsv}
                >
                  <i className="fas fa-download me-2"></i>Download CSV
                </Button>
              )}
            </Card.Header>
            <Card.Body style={{ minHeight: "400px" }}>
              {loading && (
                <div className="d-flex justify-content-center align-items-center h-100">
                  <Spinner animation="border" />
                </div>
              )}
              {error && <Alert variant="danger">{error}</Alert>}

              {!loading && !error && summary && (
                <Accordion defaultActiveKey={["0", "1"]} alwaysOpen>
                  {/* DEFINITIVE FIX: Summary view re-enabled with bulletproof rendering */}
                  <Accordion.Item eventKey="0">
                    <Accordion.Header>
                      <i className="fas fa-chart-pie me-2"></i>
                      Prediction Summary
                    </Accordion.Header>
                    <Accordion.Body>
                      <Row>
                        {targets.map((target) => {
                          const data = summary[target];
                          if (!data) return null; // Defensive guard
                          return (
                            <Col md={6} key={target} className="mb-3">
                              <Card>
                                <Card.Body>
                                  <Card.Title>
                                    {targetLabels[target]}
                                  </Card.Title>
                                  <Card.Text
                                    as="div"
                                    style={{ fontSize: "0.9rem" }}
                                  >
                                    <div className="d-flex justify-content-between">
                                      <span>Success Rate:</span>
                                      <strong>
                                        {(data.success_rate * 100).toFixed(0)}%
                                      </strong>
                                    </div>
                                    <div className="d-flex justify-content-between">
                                      <span>Avg Confidence:</span>
                                      <strong>
                                        {(data.avg_confidence * 100).toFixed(0)}
                                        %
                                      </strong>
                                    </div>
                                    <div className="d-flex justify-content-between align-items-center">
                                      <span className="me-2">
                                        Top Predictions:
                                      </span>
                                      <span className="text-end">
                                        {Object.entries(data.top_predictions)
                                          .length > 0 ? (
                                          Object.entries(
                                            data.top_predictions
                                          ).map(([value, count]) => (
                                            <Badge
                                              key={value}
                                              pill
                                              bg="dark"
                                              className="ms-1 fw-normal prediction-badge"
                                            >
                                              {getDisplayLabel(target, value)}:{" "}
                                              {count}
                                            </Badge>
                                          ))
                                        ) : (
                                          <Badge
                                            pill
                                            bg="light"
                                            text="dark"
                                            className="fw-normal"
                                          >
                                            None
                                          </Badge>
                                        )}
                                      </span>
                                    </div>
                                  </Card.Text>
                                </Card.Body>
                              </Card>
                            </Col>
                          );
                        })}
                      </Row>
                    </Accordion.Body>
                  </Accordion.Item>
                  <Accordion.Item eventKey="1">
                    <Accordion.Header>
                      <i className="fas fa-list-alt me-2"></i>
                      Detailed Results ({detailedResults.length} Cases)
                    </Accordion.Header>
                    <Accordion.Body>
                      {console.log(
                        "[DEBUG] 3. Rendering component with `detailedResults`:",
                        detailedResults
                      )}
                      {detailedResults && detailedResults.length > 0 ? (
                        <div className="table-responsive">
                          <Table striped bordered hover size="sm">
                            <thead>
                              <tr>
                                <th>Case</th>
                                {targets.map((target) => (
                                  <th key={target}>{targetLabels[target]}</th>
                                ))}
                              </tr>
                            </thead>
                            <tbody>
                              {detailedResults.map((result, index) => {
                                // Bulletproof guard against malformed result items
                                if (
                                  !result ||
                                  typeof result.predictions !== "object" ||
                                  result.predictions === null
                                ) {
                                  return (
                                    <tr key={index}>
                                      <td colSpan={targets.length + 1}>
                                        Malformed data for case {index + 1}
                                      </td>
                                    </tr>
                                  );
                                }
                                return (
                                  <tr key={index}>
                                    <td>
                                      {result.case_id !== undefined
                                        ? result.case_id + 1
                                        : index + 1}
                                    </td>
                                    {targets.map((target) => {
                                      const predictionData =
                                        result.predictions[target];
                                      // Bulletproof guard for each cell
                                      if (
                                        !predictionData ||
                                        predictionData.error
                                      ) {
                                        return (
                                          <td
                                            key={target}
                                            className="text-center align-middle"
                                          >
                                            <Badge
                                              bg="danger"
                                              className="fw-normal"
                                            >
                                              Error
                                            </Badge>
                                          </td>
                                        );
                                      }
                                      return (
                                        <td
                                          key={target}
                                          className="text-center align-middle"
                                        >
                                          <Badge
                                            bg={
                                              ["N/A", "Inconclusive"].includes(
                                                getDisplayLabel(
                                                  target,
                                                  predictionData.prediction
                                                )
                                              )
                                                ? "secondary"
                                                : "primary"
                                            }
                                            className="fw-normal prediction-badge"
                                          >
                                            {getDisplayLabel(
                                              target,
                                              predictionData.prediction
                                            )}
                                          </Badge>
                                        </td>
                                      );
                                    })}
                                  </tr>
                                );
                              })}
                            </tbody>
                          </Table>
                        </div>
                      ) : (
                        <Alert variant="info">
                          No detailed results to display.
                        </Alert>
                      )}
                    </Accordion.Body>
                  </Accordion.Item>
                </Accordion>
              )}

              {/* Guard for the initial state before any upload */}
              {!loading && !error && !summary && (
                <div className="text-center text-muted d-flex flex-column justify-content-center align-items-center h-100">
                  <i className="fas fa-chart-bar fa-3x mb-3"></i>
                  <p>No batch predictions yet. Upload a file to see results.</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ComprehensiveUploadTab;
