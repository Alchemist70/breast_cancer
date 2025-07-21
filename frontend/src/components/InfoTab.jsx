import React, { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Badge,
  Table,
  Alert,
  Spinner,
  Accordion,
} from "react-bootstrap";

const API_BASE_URL = "http://localhost:8000";

const InfoTab = ({ modelInfo }) => {
  const [models, setModels] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/models`);
      const data = await response.json();
      setModels(data);
    } catch (error) {
      console.error("Error fetching models:", error);
    } finally {
      setLoading(false);
    }
  };

  const targetLabels = {
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

  const renderModelCard = (target, modelInfo) => {
    if (!modelInfo.loaded) {
  return (
        <Col md={6} lg={4} key={target} className="mb-3">
          <Card className="h-100 border-warning">
            <Card.Body>
              <Card.Title className="h6">{targetLabels[target]}</Card.Title>
              <Badge bg="warning" className="mb-2">
                Not Available
                    </Badge>
              <p className="text-muted small">{modelInfo.error}</p>
            </Card.Body>
          </Card>
        </Col>
      );
    }

    return (
      <Col md={6} lg={4} key={target} className="mb-3">
        <Card className="h-100 border-success">
            <Card.Body>
            <Card.Title className="h6">{targetLabels[target]}</Card.Title>
            <Badge bg="success" className="mb-2">
              Loaded
            </Badge>

            <div className="mb-2">
              <small className="text-muted">
                <strong>Accuracy:</strong>{" "}
                {(modelInfo.accuracy * 100).toFixed(1)}%
              </small>
            </div>

            <div className="mb-2">
              <small className="text-muted">
                <strong>Features:</strong> {modelInfo.features_count}
              </small>
            </div>

            <div className="mb-2">
              <small className="text-muted">
                <strong>Type:</strong> {modelInfo.model_type}
              </small>
            </div>

            {modelInfo.summary && (
              <Accordion>
                <Accordion.Item eventKey={target}>
                  <Accordion.Header>
                    <small>Model Details</small>
                  </Accordion.Header>
                  <Accordion.Body>
                    <div className="small">
                      <div>
                        <strong>Training Samples:</strong>{" "}
                        {modelInfo.summary.train_samples || "N/A"}
                  </div>
                      <div>
                        <strong>Test Samples:</strong>{" "}
                        {modelInfo.summary.test_samples || "N/A"}
                  </div>
                      <div>
                        <strong>Best Parameters:</strong>
                  </div>
                      <ul className="small">
                        {modelInfo.summary.best_params &&
                          Object.entries(modelInfo.summary.best_params).map(
                            ([key, value]) => (
                              <li key={key}>
                                {key}: {value}
                              </li>
                            )
                          )}
                      </ul>
                  </div>
                  </Accordion.Body>
                </Accordion.Item>
              </Accordion>
            )}
            </Card.Body>
          </Card>
        </Col>
    );
  };

  return (
    <Container fluid>
      <Row>
        <Col>
          <Card className="mb-4">
            <Card.Header>
              <h5 className="mb-0">
                <i className="fas fa-info-circle me-2"></i>
                Model Information
              </h5>
            </Card.Header>
            <Card.Body>
              {loading ? (
                <div className="text-center py-4">
                  <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                  <p className="mt-2">Loading model information...</p>
                </div>
              ) : models ? (
                <>
                  <div className="mb-4">
                    <h6>System Overview</h6>
              <Row>
                      <Col md={3}>
                        <div className="text-center">
                          <h4 className="text-primary">
                            {models.loaded_models}
                          </h4>
                          <small className="text-muted">Models Loaded</small>
                        </div>
                  </Col>
                      <Col md={3}>
                        <div className="text-center">
                          <h4 className="text-success">
                            {models.total_models}
                          </h4>
                          <small className="text-muted">Total Models</small>
                        </div>
        </Col>
                      <Col md={3}>
                        <div className="text-center">
                          <h4 className="text-info">11</h4>
                          <small className="text-muted">
                            Prediction Targets
                          </small>
                        </div>
                </Col>
                      <Col md={3}>
                        <div className="text-center">
                          <h4 className="text-warning">Enhanced</h4>
                          <small className="text-muted">Model Type</small>
                        </div>
        </Col>
      </Row>
                </div>

                  <div className="mb-4">
                    <h6>Available Models</h6>
                    <Row>
                      {Object.entries(models.available_models).map(
                        ([target, info]) => renderModelCard(target, info)
                      )}
                    </Row>
                </div>

                  <Alert variant="info">
                    <h6>
                      <i className="fas fa-lightbulb me-2"></i>System Features
                    </h6>
                    <ul className="mb-0">
                      <li>
                        <strong>Comprehensive Predictions:</strong> Predict all
                        11 targets simultaneously
                      </li>
                      <li>
                        <strong>Batch Processing:</strong> Upload CSV files for
                        bulk predictions
                      </li>
                      <li>
                        <strong>Real-time Results:</strong> Get instant
                        predictions with confidence scores
                      </li>
                      <li>
                        <strong>Enhanced Models:</strong> Optimized Random
                        Forest models with feature selection
                      </li>
                      <li>
                        <strong>High Accuracy:</strong> Models achieve 99%+
                        accuracy on test data
                    </li>
                  </ul>
                  </Alert>
                </>
              ) : (
                <Alert variant="danger">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  Failed to load model information. Please check the API
                  connection.
                </Alert>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default InfoTab;
