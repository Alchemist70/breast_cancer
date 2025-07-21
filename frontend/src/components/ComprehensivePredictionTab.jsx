import React, { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  Alert,
  Spinner,
  Badge,
  ProgressBar,
  Accordion,
  Table,
} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

const API_BASE_URL = "/api";

const ComprehensivePredictionTab = () => {
  const [formData, setFormData] = useState({});
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableModels, setAvailableModels] = useState({});
  const [sampleData, setSampleData] = useState({});
  const [currentPage, setCurrentPage] = useState(0);
  const featuresPerPage = 10;

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

  // Add a mapping for short feature labels
  const shortFeatureLabels = {
    "exposures.smoking_frequency": "Smoking Freq.",
    "samples.freezing_method": "Freezing Method",
    "diagnoses.contiguous_organ_invaded": "Contiguous Organ",
    "exposures.environmental_tobacco_smoke_exposure": "Env. Tobacco Smoke",
    "other_clinical_attributes.premature_at_birth": "Premature Birth",
    "exposures.type_of_tobacco_used": "Tobacco Type",
    "exposures.exposure_duration": "Exposure Duration",
    "demographic.age_is_obfuscated": "Age Obfuscated",
    "diagnoses.cog_neuroblastoma_risk_group": "Neuroblastoma Risk",
    "exposures.radon_exposure": "Radon Exposure",
    "samples.composition": "Sample Composition",
    "samples.preservation_method": "Preservation",
    "exposures.cigarettes_per_day": "Cigs/Day",
    "samples.days_to_collection": "Days to Collection",
    "diagnoses.year_of_diagnosis": "Year of Dx",
    "samples.specimen_type": "Specimen Type",
    "exposures.exposure_type": "Exposure Type",
    "treatments.treatment_outcome": "Tx Outcome",
    "samples.tumor_code_id": "Tumor Code",
    "diagnoses.sites_of_involvement": "Sites Involved",
    "diagnoses.ajcc_pathologic_n": "AJCC N",
    "samples.pathology_report_uuid": "Path. Report ID",
    "exposures.occupation_duration_years": "Occ. Duration (yrs)",
    "molecular_tests.specialized_molecular_test": "Spec. Mol. Test",
    "cases.disease_type": "Disease Type",
    "exposures.coal_dust_exposure": "Coal Dust",
    "diagnoses.days_to_diagnosis": "Days to Dx",
    "pathology_details.submitter_id": "Path. Submitter",
    "exposures.time_between_waking_and_first_smoke": "Time Wake-1st Smoke",
    "diagnoses.cog_rhabdomyosarcoma_risk_group": "Rhabdo. Risk",
    "treatments.treatment_id": "Tx ID",
    "exposures.submitter_id": "Exposure Submitter",
    "treatments.treatment_intent_type": "Tx Intent",
    "demographic.cause_of_death": "Cause of Death",
    "follow_ups.timepoint_category": "Timepoint Cat.",
    "cases.days_to_consent": "Days to Consent",
    "molecular_tests.test_result": "Test Result",
    "demographic.marital_status": "Marital Status",
    "exposures.exposure_duration_years": "Exposure Yrs",
    "exposures.pack_years_smoked": "Pack-Years",
    "demographic.demographic_id": "Demo. ID",
    "exposures.occupation_type": "Occ. Type",
    "demographic.premature_at_birth": "Premature Birth",
    "diagnoses.ajcc_pathologic_stage": "AJCC Stage",
    "diagnoses.method_of_diagnosis": "Dx Method",
    "diagnoses.diagnosis_id_y": "Dx ID Y",
    "exposures.respirable_crystalline_silica_exposure": "Silica Exposure",
    "pathology_details.pathology_detail_id": "Path. Detail ID",
    "exposures.tobacco_smoking_quit_year": "Quit Year",
    "cases.primary_site": "Primary Site",
    "diagnoses.laterality": "Laterality",
    "samples.initial_weight": "Init. Weight",
    "demographic.cause_of_death_source": "COD Source",
    "diagnoses.morphology": "Morphology",
    "cases.submitter_id": "Case Submitter",
    "demographic.country_of_residence_at_enrollment": "Country (Enroll)",
    "exposures.tobacco_smoking_onset_year": "Onset Year",
    "diagnoses.submitter_id_y": "Dx Submitter Y",
    "demographic.days_to_birth": "Days to Birth",
    "molecular_tests.test_value_range": "Test Value Range",
    "demographic.age_at_index": "Age at Index",
    "treatments.treatment_anatomic_sites": "Tx Anatomic Sites",
    "diagnoses.metastasis_at_diagnosis": "Metastasis at Dx",
    "cases.consent_type": "Consent Type",
    "diagnoses.primary_diagnosis": "Primary Dx",
    "exposures.exposure_id": "Exposure ID",
    "treatments.days_to_treatment_start": "Days to Tx Start",
    "exposures.exposure_source": "Exposure Source",
    "treatments.treatment_type": "Tx Type",
    "exposures.type_of_smoke_exposure": "Smoke Type",
    "pathology_details.lymph_nodes_tested": "Nodes Tested",
    "molecular_tests.submitter_id": "Mol. Submitter",
    "other_clinical_attributes.risk_factor_treatment": "Risk Factor Tx",
    "diagnoses.diagnosis_id_x": "Dx ID X",
    "diagnoses.child_pugh_classification": "Child-Pugh",
    "other_clinical_attributes.other_clinical_attribute_id":
      "Other Clin. Attr. ID",
    "pathology_details.lymph_nodes_positive": "Nodes Positive",
    "molecular_tests.variant_type": "Variant Type",
    "exposures.exposure_duration_hrs_per_day": "Exposure Hrs/Day",
    "demographic.country_of_birth": "Country of Birth",
    "samples.tissue_type": "Tissue Type",
    "other_clinical_attributes.reflux_treatment_type": "Reflux Tx Type",
    "cases.case_id_x": "Case ID X",
    "other_clinical_attributes.menopause_status": "Menopause",
    "molecular_tests.gene_symbol": "Gene Symbol",
    "cases.index_date": "Index Date",
    "follow_ups.follow_up_id": "Follow-up ID",
    "molecular_tests.chromosome": "Chromosome",
    "samples.sample_type_id": "Sample Type ID",
    "treatments.initial_disease_status": "Init. Disease Status",
    "cases.days_to_lost_to_followup": "Days to Lost Followup",
    "diagnoses.submitter_id_x": "Dx Submitter X",
    "follow_ups.days_to_follow_up": "Days to Follow-up",
    "demographic.race": "Race",
    "samples.is_ffpe": "FFPE",
    "diagnoses.days_to_last_follow_up": "Days to Last FU",
    "exposures.use_per_day": "Use/Day",
    "samples.catalog_reference": "Catalog Ref.",
    "molecular_tests.molecular_test_id": "Mol. Test ID",
    "diagnoses.age_at_diagnosis": "Age at Dx",
    "demographic.submitter_id": "Demo. Submitter",
    "treatments.therapeutic_agents": "Therapeutic Agents",
    "treatments.submitter_id": "Tx Submitter",
    "exposures.years_smoked": "Years Smoked",
    "samples.tumor_descriptor": "Tumor Desc.",
    "samples.sample_id": "Sample ID",
    "follow_ups.comorbidity_method_of_diagnosis": "Comorbidity Dx Method",
    "samples.oct_embedded": "OCT Embedded",
    "samples.sample_type": "Sample Type",
    "molecular_tests.staining_intensity_value": "Stain Intensity",
    "exposures.secondhand_smoke_as_child": "2ndhand Smoke (Child)",
    "diagnoses.ajcc_staging_system_edition": "AJCC Edition",
    "demographic.days_to_death": "Days to Death",
    "samples.submitter_id": "Sample Submitter",
    "other_clinical_attributes.submitter_id": "Other Clin. Submitter",
    "exposures.parent_with_radiation_exposure": "Parent Radiation",
    "follow_ups.submitter_id": "FU Submitter",
    "exposures.tobacco_smoking_status": "Smoking Status",
    "cases.case_id": "Case ID",
    "treatments.days_to_treatment_end": "Days to Tx End",
    "cases.case_id_y": "Case ID Y",
    "cases.lost_to_followup": "Lost to FU",
    "samples.days_to_sample_procurement": "Days to Sample Proc.",
    "other_clinical_attributes.risk_factor_method_of_diagnosis":
      "Risk Factor Dx Method",
    "diagnoses.cog_liver_stage": "COG Liver Stage",
    "molecular_tests.test_value": "Test Value",
  };

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

  useEffect(() => {
    fetchAvailableModels();
    loadSampleData();
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

  const loadSampleData = async () => {
    try {
      // Load sample data from public folder
      const response = await fetch("/sample_data.csv");
      if (response && response.ok) {
        const text = await response.text();
        const lines = text.split("\n");
        if (lines.length > 1) {
          const headers = lines[0].split(",");
          const values = lines[1].split(",");
          const sample = {};
          headers.forEach((header, index) => {
            if (values[index]) {
              sample[header.trim()] =
                parseFloat(values[index]) || values[index].trim();
            }
          });
          setSampleData(sample);
          setFormData(sample);
        }
      } else {
        // Create default sample data if file not found or response not ok
        createDefaultSampleData();
      }
    } catch (error) {
      console.error("Error loading sample data:", error);
      // Create default sample data if fetch fails
      createDefaultSampleData();
    }
  };

  const createDefaultSampleData = () => {
    const defaultSample = {};
    for (let i = 1; i <= 126; i++) {
      // Use 126 features to match the model
      defaultSample[`feature_${i}`] = Math.random();
    }
    setSampleData(defaultSample);
    setFormData(defaultSample);
  };

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPredictions(null);

    try {
      const response = await fetch(`${API_BASE_URL}/predict-all`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ features: formData }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPredictions(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.9) return "success";
    if (confidence >= 0.7) return "warning";
    return "danger";
  };

  const getPredictionColor = (target, prediction) => {
    if (prediction === "N/A" || prediction === "Inconclusive") {
      return "secondary";
    }
    const colors = {
      vital_status: { Alive: "success", Dead: "danger" },
      metastasis: { "No Metastasis": "success", "Metastasis, NOS": "danger" },
      clinical_trial: { No: "secondary", Yes: "primary" },
    };
    return colors[target]?.[prediction] || "primary";
  };

  const renderPredictionCard = (target, predictionData) => {
    if (!predictionData || predictionData.error) {
      return (
        <Card className="mb-3 border-danger">
          <Card.Body>
            <Card.Title className="text-danger">
              {targetLabels[target]}
            </Card.Title>
            <Alert variant="danger">
              {predictionData?.error || "Prediction failed"}
            </Alert>
          </Card.Body>
        </Card>
      );
    }

    let { prediction, confidence, probabilities, model_accuracy } =
      predictionData;
    const isLoaded = availableModels[target]?.loaded;

    // Map prediction to human-readable label if mapping exists
    if (
      classLabelMappings[target] &&
      prediction !== null &&
      prediction !== undefined &&
      !isNaN(Number(prediction)) &&
      Number(prediction) < classLabelMappings[target].length
    ) {
      prediction = classLabelMappings[target][Number(prediction)];
    }

    return (
      <Card
        className={`mb-3 ${isLoaded ? "border-success" : "border-warning"}`}
      >
        <Card.Body>
          <div className="d-flex justify-content-between align-items-start mb-2">
            <Card.Title className="mb-0">{targetLabels[target]}</Card.Title>
            <Badge bg={isLoaded ? "success" : "warning"}>
              {isLoaded ? "Loaded" : "Not Available"}
            </Badge>
          </div>

          {isLoaded && (
            <>
              <div className="mb-3">
                <strong>Prediction:</strong>{" "}
                <Badge bg={getPredictionColor(target, prediction)}>
                  {prediction}
                </Badge>
              </div>

              {prediction !== "N/A" && (
                <div className="mb-3">
                  <strong>Confidence:</strong>
                  <ProgressBar
                    variant={getConfidenceColor(confidence)}
                    now={confidence * 100}
                    label={`${(confidence * 100).toFixed(1)}%`}
                    className="mt-1"
                  />
                </div>
              )}

              {model_accuracy && (
                <div className="mb-2">
                  <small className="text-muted">
                    Model Accuracy: {(model_accuracy * 100).toFixed(1)}%
                  </small>
                </div>
              )}
            </>
          )}
        </Card.Body>
      </Card>
    );
  };

  return (
    <Container fluid>
      <Row>
        <Col lg={6}>
          <Card className="mb-4">
            <Card.Header>
              <h5 className="mb-0">
                <i className="fas fa-brain me-2"></i>
                Comprehensive Prediction
              </h5>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <Button
                    variant="outline-secondary"
                    size="sm"
                    onClick={() => setFormData(sampleData)}
                    className="me-2"
                  >
                    <i className="fas fa-download me-1"></i>
                    Load Sample Data
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => setFormData({})}
                  >
                    <i className="fas fa-trash me-1"></i>
                    Clear Form
                  </Button>
                </div>

                <Accordion defaultActiveKey="0">
                  <Accordion.Item eventKey="0">
                    <Accordion.Header>
                      <i className="fas fa-sliders-h me-2"></i>
                      Input Features
                    </Accordion.Header>
                    <Accordion.Body>
                      <div className="mb-3">
                        <div className="d-flex justify-content-between align-items-center mb-2">
                          <small className="text-muted">
                            Showing features {currentPage * featuresPerPage + 1}{" "}
                            -{" "}
                            {Math.min(
                              (currentPage + 1) * featuresPerPage,
                              Object.keys(sampleData).length
                            )}{" "}
                            of {Object.keys(sampleData).length}
                          </small>
                          <div>
                            <Button
                              variant="outline-secondary"
                              size="sm"
                              onClick={() =>
                                setCurrentPage(Math.max(0, currentPage - 1))
                              }
                              disabled={currentPage === 0}
                              className="me-1"
                            >
                              <i className="fas fa-chevron-left"></i>
                            </Button>
                            <Button
                              variant="outline-secondary"
                              size="sm"
                              onClick={() => setCurrentPage(currentPage + 1)}
                              disabled={
                                (currentPage + 1) * featuresPerPage >=
                                Object.keys(sampleData).length
                              }
                            >
                              <i className="fas fa-chevron-right"></i>
                            </Button>
                          </div>
                        </div>
                      </div>

                      <Row>
                        {Object.keys(sampleData)
                          .slice(
                            currentPage * featuresPerPage,
                            (currentPage + 1) * featuresPerPage
                          )
                          .map((field) => (
                            <Col md={6} key={field}>
                              <Form.Group className="mb-3">
                                <Form.Label>
                                  {shortFeatureLabels[field] || field}
                                </Form.Label>
                                <Form.Control
                                  type="number"
                                  step="any"
                                  value={formData[field] || ""}
                                  onChange={(e) =>
                                    handleInputChange(
                                      field,
                                      parseFloat(e.target.value) || 0
                                    )
                                  }
                                  placeholder="Enter value"
                                />
                              </Form.Group>
                            </Col>
                          ))}
                      </Row>

                      <Alert variant="info">
                        <i className="fas fa-info-circle me-2"></i>
                        All {Object.keys(sampleData).length} features will be
                        included in prediction. Use pagination to navigate
                        through all features.
                      </Alert>
                    </Accordion.Body>
                  </Accordion.Item>
                </Accordion>

                <div className="d-grid gap-2 mt-3">
                  <Button
                    type="submit"
                    variant="primary"
                    size="lg"
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

        <Col lg={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">
                <i className="fas fa-chart-line me-2"></i>
                Prediction Results
              </h5>
            </Card.Header>
            <Card.Body>
              {predictions ? (
                <>
                  <div className="mb-3">
                    <Badge bg="success" className="me-2">
                      {predictions.successful_predictions} Successful
                    </Badge>
                    <Badge bg="secondary">
                      {predictions.total_targets} Total Targets
                    </Badge>
                  </div>

                  <div className="prediction-results">
                    {targets.map((target) =>
                      renderPredictionCard(
                        target,
                        predictions.predictions[target]
                      )
                    )}
                  </div>
                </>
              ) : (
                <div className="text-center text-muted py-5">
                  <i className="fas fa-chart-bar fa-3x mb-3"></i>
                  <p>No predictions yet. Submit data to see results.</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ComprehensivePredictionTab;
