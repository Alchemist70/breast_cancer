import React, { useState, useEffect } from "react";
import { Card, Form, Button, Row, Col, Alert, Spinner } from "react-bootstrap";

const API_BASE_URL = "/api";

// Define all available prediction targets with their specific sample files
const PREDICTION_TARGETS = [
  {
    key: "wdbc_malignancy",
    name: "Malignancy (WDBC)",
    endpoint: "/predict-wdbc-malignancy",
    features: "wdbc_malignancy_features.joblib",
    sampleFile: "sample_wdbc_malignancy.csv",
    description: "Predict malignancy using the WDBC dataset",
    icon: "fas fa-star",
  },
  {
    key: "vital_status",
    name: "Vital Status",
    endpoint: "/predict-vital-status",
    sampleFile: "sample_vital_status.csv",
    description: "Predict patient survival status",
    icon: "fas fa-heartbeat",
  },
  {
    key: "cancer_type",
    name: "Cancer Type",
    endpoint: "/predict-cancer-type",
    sampleFile: "sample_cancer_type.csv",
    description: "Predict specific type of breast cancer",
    icon: "fas fa-microscope",
  },
  {
    key: "stage",
    name: "Cancer Stage",
    endpoint: "/predict-stage",
    sampleFile: "sample_stage.csv",
    description: "Predict cancer stage (0-IV)",
    icon: "fas fa-chart-line",
  },
  {
    key: "metastasis",
    name: "Metastasis",
    endpoint: "/predict-metastasis",
    sampleFile: "sample_metastasis.csv",
    description: "Predict if cancer has spread",
    icon: "fas fa-arrows-alt",
  },
  {
    key: "treatment_outcome",
    name: "Treatment Outcome",
    endpoint: "/predict-treatment-outcome",
    sampleFile: "sample_treatment_outcome.csv",
    description: "Predict treatment response",
    icon: "fas fa-clipboard-check",
  },
  {
    key: "treatment_type",
    name: "Treatment Type",
    endpoint: "/predict-treatment-type",
    sampleFile: "sample_treatment_type.csv",
    description: "Predict recommended treatment",
    icon: "fas fa-pills",
  },
  {
    key: "clinical_trial",
    name: "Clinical Trial",
    endpoint: "/predict-clinical-trial",
    sampleFile: "sample_clinical_trial.csv",
    description: "Predict clinical trial eligibility",
    icon: "fas fa-flask",
  },
  {
    key: "age_at_index",
    name: "Age at Diagnosis",
    endpoint: "/predict-age-at-index",
    sampleFile: "sample_age_at_index.csv",
    description: "Predict age category at diagnosis",
    icon: "fas fa-user-clock",
  },
  {
    key: "classification_of_tumor",
    name: "Tumor Classification",
    endpoint: "/predict-classification-of-tumor",
    sampleFile: "sample_classification_of_tumor.csv",
    description: "Predict tumor classification type",
    icon: "fas fa-tag",
  },
  {
    key: "disease_response",
    name: "Disease Response",
    endpoint: "/predict-disease-response",
    sampleFile: "sample_disease_response.csv",
    description: "Predict disease response to treatment",
    icon: "fas fa-chart-bar",
  },
  {
    key: "tissue_or_organ_of_origin",
    name: "Tissue/Organ Origin",
    endpoint: "/predict-tissue-or-organ-of-origin",
    sampleFile: "sample_tissue_or_organ_of_origin.csv",
    description: "Predict tissue or organ of origin",
    icon: "fas fa-map-marker-alt",
  },
];

function PredictionTab() {
  const [features, setFeatures] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [validationError, setValidationError] = useState(null);
  const [featureNames, setFeatureNames] = useState([]);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [selectedTarget, setSelectedTarget] = useState("wdbc_malignancy");

  // Add class label mappings for all targets
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
    metastasis: ["Metastasis, NOS", "No Metastasis"],
    age_at_index: ["No", "Yes"],
    clinical_trial: ["No", "Yes"],
    treatment_type: [
      "Ancillary Treatment",
      "Bisphosphonate Therapy",
      "Brachytherapy, High Dose",
      "Brachytherapy, NOS",
      "Chemotherapy",
      "Hormone Therapy",
      "Immunotherapy (Including Vaccines)",
      "Pharmaceutical Therapy, NOS",
      "Radiation Therapy, NOS",
      "Radiation, External Beam",
      "Radiation, Implants",
      "Radiation, Radioisotope",
      "Radiation, Stereotactic/Gamma Knife/SRS",
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
      "Bladder, NOS",
      "Blood vessel",
      "Bone marrow",
      "Breast, NOS",
      "Bronchus and lung",
      "Cervix uteri",
      "Colon, NOS",
      "Corpus uteri",
      "Esophagus, NOS",
      "Head, face or neck, NOS",
      "Kidney, NOS",
      "Liver",
      "Lymph nodes",
      "Melanocytes, NOS",
      "Ovary",
      "Pancreas, NOS",
      "Peripheral nerves and autonomic nervous system",
      "Pleura, NOS",
      "Prostate gland",
      "Skin, NOS",
      "Small intestine, NOS",
      "Soft tissues",
      "Stomach, NOS",
      "Testis, NOS",
      "Thyroid gland",
      "Unknown primary site",
    ],
  };

  // Fetch feature names from backend
  useEffect(() => {
    const fetchFeatures = async () => {
      const target = PREDICTION_TARGETS.find((t) => t.key === selectedTarget);
      if (target && target.features) {
        try {
          // This assumes the joblib file is converted to JSON and placed in public
          const response = await fetch(
            `/${target.features.replace(".joblib", ".json")}`
          );
          const data = await response.json();
          setFeatureNames(data);
        } catch (e) {
          console.error("Could not load features for WDBC model", e);
        }
      } else if (selectedTarget === "malignancy") {
        // Legacy handling for original malignancy model
        fetch(`${API_BASE_URL}/model-info`)
          .then((res) => res.json())
          .then((data) => {
            if (
              data &&
              data.model_summary &&
              data.model_summary.feature_names
            ) {
              setFeatureNames(data.model_summary.feature_names);
            }
          });
      }
    };
    fetchFeatures();
  }, [selectedTarget]);

  // Only show a few important fields in the main form
  const mainFields = [
    "demographic.age_at_index",
    "diagnoses.tumor_grade",
    "diagnoses.ajcc_pathologic_stage",
    "diagnoses.tumor_size",
    "diagnoses.lymph_nodes_examined",
  ];

  const handleFeatureChange = (key, value) => {
    setFeatures((prev) => ({
      ...prev,
      [key]: value === "" ? "" : parseFloat(value) || 0,
    }));
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    setValidationError(null);

    // Validation: Tumor size must be positive
    if (
      features["diagnoses.tumor_size"] === undefined ||
      isNaN(features["diagnoses.tumor_size"]) ||
      features["diagnoses.tumor_size"] <= 0
    ) {
      setLoading(false);
      setValidationError("Tumor size must be a positive number.");
      return;
    }

    // Build full feature vector
    const fullFeatures = {};
    featureNames.forEach((fname) => {
      fullFeatures[fname] =
        features[fname] !== undefined && features[fname] !== ""
          ? features[fname]
          : 0;
    });

    try {
      const target = PREDICTION_TARGETS.find((t) => t.key === selectedTarget);
      const response = await fetch(`${API_BASE_URL}${target.endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ features: fullFeatures }),
      });

      if (!response.ok) {
        let backendMsg = "";
        try {
          const errData = await response.json();
          backendMsg = errData.detail || JSON.stringify(errData);
        } catch {}
        throw new Error(
          `HTTP error! status: ${response.status}${
            backendMsg ? ": " + backendMsg : ""
          }`
        );
      }

      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error("Prediction error:", error);
      setError(error.message || "Error making prediction. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Enhanced: Load realistic sample values and then override with potent benign values
  const loadBenignExample = async () => {
    const target = PREDICTION_TARGETS.find((t) => t.key === selectedTarget);
    if (!target || !target.sampleFile) {
      console.error("No sample file specified for the selected target.");
      return;
    }

    let sample = {};
    try {
      const response = await fetch(`/${target.sampleFile}`);
      if (response.ok) {
        const text = await response.text();
        const lines = text.split("\n");
        if (lines.length > 1) {
          const headers = lines[0].split(",").map((h) => h.trim());
          const values = lines[1].split(",").map((v) => v.trim());
          headers.forEach((header, index) => {
            if (values[index] && header) {
              const numValue = parseFloat(values[index]);
              sample[header] = isNaN(numValue) ? values[index] : numValue;
            }
          });
        }
      }
    } catch (e) {
      console.error(`Failed to load or parse ${target.sampleFile}`, e);
    }

    // Forcefully override with values guaranteed to trigger a benign prediction
    const benignOverrides = {
      radius_mean: 10,
      texture_mean: 15,
      perimeter_mean: 60,
      area_mean: 300,
      smoothness_mean: 0.08,
      compactness_mean: 0.05,
      concavity_mean: 0.01,
      concave_points_mean: 0.01,
      symmetry_mean: 0.18,
      fractal_dimension_mean: 0.06,
      radius_se: 0.2,
      texture_se: 0.5,
      perimeter_se: 1.5,
      area_se: 15,
      "diagnoses.tumor_grade": 1,
      "diagnoses.ajcc_pathologic_stage": 1,
      "diagnoses.tumor_size": 1, // cm
      "diagnoses.lymph_nodes_examined": 0,
      "demographic.age_at_index": 40,
    };

    const newFeatures = { ...sample, ...benignOverrides };
    setFeatures(newFeatures);
  };

  // Enhanced: Load realistic sample values and then override with potent malignant values
  const loadMalignantExample = async () => {
    const target = PREDICTION_TARGETS.find((t) => t.key === selectedTarget);
    if (!target || !target.sampleFile) {
      console.error("No sample file specified for the selected target.");
      return;
    }

    let sample = {};
    try {
      const response = await fetch(`/${target.sampleFile}`);
      if (response.ok) {
        const text = await response.text();
        const lines = text.split("\n");
        if (lines.length > 1) {
          const headers = lines[0].split(",").map((h) => h.trim());
          const values = lines[1].split(",").map((v) => v.trim());
          headers.forEach((header, index) => {
            if (values[index] && header) {
              const numValue = parseFloat(values[index]);
              sample[header] = isNaN(numValue) ? values[index] : numValue;
            }
          });
        }
      }
    } catch (e) {
      console.error(`Failed to load or parse ${target.sampleFile}`, e);
    }

    // Forcefully override with values guaranteed to trigger a malignant prediction
    const malignantOverrides = {
      // Key features for WDBC model
      radius_mean: 25,
      texture_mean: 25,
      perimeter_mean: 180,
      area_mean: 2000,
      smoothness_mean: 0.15,
      compactness_mean: 0.3,
      concavity_mean: 0.4,
      concave_points_mean: 0.2,
      symmetry_mean: 0.3,
      fractal_dimension_mean: 0.08,
      radius_se: 1,
      texture_se: 2,
      perimeter_se: 10,
      area_se: 150,
      // Key features for other models
      "diagnoses.tumor_grade": 4,
      "diagnoses.ajcc_pathologic_stage": 4,
      "diagnoses.tumor_size": 10, // cm
      "diagnoses.lymph_nodes_examined": 20,
      "demographic.age_at_index": 70,
    };

    const newFeatures = { ...sample, ...malignantOverrides };
    setFeatures(newFeatures);
  };

  const getPredictionDisplay = () => {
    if (!prediction) return null;

    const target = PREDICTION_TARGETS.find((t) => t.key === selectedTarget);

    // Handle different prediction formats
    let predictionValue = prediction.prediction;
    let predictionClass = "bg-primary";

    // Special handling for malignancy (legacy format)
    if (selectedTarget === "malignancy") {
      predictionValue = prediction.prediction === 1 ? "Malignant" : "Benign";
      predictionClass =
        prediction.prediction === 1 ? "bg-danger" : "bg-success";
    } else {
      // For other targets, use the prediction string directly
      predictionClass = "bg-info";
    }

    return (
      <Card className="prediction-result">
        <Card.Body>
          <Card.Title>
            <i className={`${target.icon} me-2`}></i>
            {target.name} Prediction Results
          </Card.Title>

          <div className="mb-3">
            <strong>Predicted {target.name}:</strong>
            <div className="mt-2">
              <span className={`badge ${predictionClass} fs-6`}>
                {predictionValue}
              </span>
            </div>
          </div>

          {prediction.probabilities && (
            <div className="mb-3">
              <strong>Confidence:</strong>
              <div className="mt-2">
                <div className="progress">
                  <div
                    className={`progress-bar ${predictionClass}`}
                    style={{
                      width: `${
                        Math.max(...Object.values(prediction.probabilities)) *
                        100
                      }%`,
                    }}
                  >
                    {(
                      Math.max(...Object.values(prediction.probabilities)) * 100
                    ).toFixed(1)}
                    %
                  </div>
                </div>
              </div>
            </div>
          )}

          {prediction.probabilities &&
            Object.keys(prediction.probabilities).length > 1 && (
              <div className="mb-3">
                <strong>All Probabilities:</strong>
                <div className="mt-2">
                  {Object.entries(prediction.probabilities).map(
                    ([key, value]) => {
                      let label = key;
                      const idx = parseInt(key);
                      if (
                        !isNaN(idx) &&
                        classLabelMappings[selectedTarget] &&
                        idx < classLabelMappings[selectedTarget].length
                      ) {
                        label = classLabelMappings[selectedTarget][idx];
                      }
                      return (
                        <div
                          key={key}
                          className="d-flex justify-content-between mb-1"
                        >
                          <span>{label}:</span>
                          <span>{(value * 100).toFixed(1)}%</span>
                        </div>
                      );
                    }
                  )}
                </div>
              </div>
            )}

          {prediction.feature_importance && (
            <div>
              <strong>Key Features:</strong>
              <ul className="mt-2">
                {Object.entries(prediction.feature_importance)
                  .slice(0, 5)
                  .map(([feature, importance]) => (
                    <li key={feature}>
                      {feature}: {(importance * 100).toFixed(1)}%
                    </li>
                  ))}
              </ul>
            </div>
          )}
        </Card.Body>
      </Card>
    );
  };

  return (
    <div>
      <div className="hero-section text-center mb-4">
        <h1>
          <i className="fas fa-brain me-3"></i>AI-Powered Breast Cancer
          Prediction
        </h1>
        <p className="lead">
          Input clinical data to get instant predictions for multiple targets
        </p>
      </div>

      <Row>
        <Col md={6}>
          <Card className="feature-card">
            <Card.Body>
              <Card.Title>
                <i className="fas fa-edit me-2"></i>Input Features
              </Card.Title>

              <Form>
                {/* Prediction Target Selection */}
                <Form.Group className="mb-3">
                  <Form.Label>
                    <i className="fas fa-target me-2"></i>Prediction Target
                  </Form.Label>
                  <Form.Select
                    value={selectedTarget}
                    onChange={(e) => setSelectedTarget(e.target.value)}
                  >
                    {PREDICTION_TARGETS.map((target) => (
                      <option key={target.key} value={target.key}>
                        <i className={target.icon}></i> {target.name}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Text className="text-muted">
                    {
                      PREDICTION_TARGETS.find((t) => t.key === selectedTarget)
                        ?.description
                    }
                  </Form.Text>
                </Form.Group>

                <div className="mb-3">
                  <Button
                    variant="outline-danger"
                    size="sm"
                    className="me-2"
                    onClick={loadMalignantExample}
                  >
                    <i className="fas fa-bolt me-1"></i> Load Malignant Example
                  </Button>
                  <Button
                    variant="outline-success"
                    size="sm"
                    onClick={loadBenignExample}
                  >
                    <i className="fas fa-leaf me-1"></i> Load Benign Example
                  </Button>
                </div>

                {mainFields.map((field) => (
                  <Form.Group className="mb-3" key={field}>
                    <Form.Label>
                      {field
                        .replace(/\./g, " ")
                        .replace(/_/g, " ")
                        .replace(/\b\w/g, (l) => l.toUpperCase())}
                    </Form.Label>
                    <Form.Control
                      type="number"
                      placeholder={`Enter ${field}`}
                      value={features[field] || ""}
                      onChange={(e) =>
                        handleFeatureChange(field, e.target.value)
                      }
                    />
                  </Form.Group>
                ))}
                <Button
                  variant="link"
                  onClick={() => setShowAdvanced((v) => !v)}
                  style={{ marginBottom: "1rem" }}
                >
                  {showAdvanced ? "Hide" : "Show"} Advanced Features
                </Button>
                {showAdvanced &&
                  featureNames
                    .filter((f) => !mainFields.includes(f))
                    .map((field) => (
                      <Form.Group className="mb-2" key={field}>
                        <Form.Label>
                          {field
                            .replace(/\./g, " ")
                            .replace(/_/g, " ")
                            .replace(/\b\w/g, (l) => l.toUpperCase())}
                        </Form.Label>
                        <Form.Control
                          type="number"
                          placeholder={`Enter ${field}`}
                          value={features[field] || ""}
                          onChange={(e) =>
                            handleFeatureChange(field, e.target.value)
                          }
                        />
                      </Form.Group>
                    ))}
                {validationError && (
                  <Alert variant="warning">
                    <i className="fas fa-exclamation-circle me-2"></i>
                    {validationError}
                  </Alert>
                )}
                <Button
                  variant="primary"
                  size="lg"
                  className="w-100"
                  onClick={handlePredict}
                  disabled={loading}
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
                      Predicting...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-magic me-2"></i>Get Prediction
                    </>
                  )}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          {error && (
            <Alert variant="danger">
              <i className="fas fa-exclamation-triangle me-2"></i>
              {error}
            </Alert>
          )}

          {getPredictionDisplay()}
        </Col>
      </Row>
    </div>
  );
}

export default PredictionTab;
