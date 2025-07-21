import React, { useState, useEffect } from "react";
import { Card, Row, Col, Spinner, Alert } from "react-bootstrap";
import { Line, Bar, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const API_BASE_URL = "http://localhost:8000";

function VisualizeTab() {
  const [visualizationData, setVisualizationData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchVisualizationData();
  }, []);

  const fetchVisualizationData = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/visualize`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setVisualizationData(data);
    } catch (error) {
      console.error("Error fetching visualization data:", error);
      setError("Error loading visualization data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading visualizations...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger">
        <i className="fas fa-exclamation-triangle me-2"></i>
        {error}
      </Alert>
    );
  }

  if (!visualizationData) {
    return (
      <Alert variant="info">
        <i className="fas fa-info-circle me-2"></i>
        No visualization data available. Please ensure the backend is running
        and has visualization data.
      </Alert>
    );
  }

  // Sample data for demonstration (replace with actual data from API)
  const featureImportanceData = {
    labels: ["Age", "Tumor Grade", "Tumor Stage", "Tumor Size", "Lymph Nodes"],
    datasets: [
      {
        label: "Feature Importance",
        data: [0.25, 0.3, 0.2, 0.15, 0.1],
        backgroundColor: [
          "rgba(255, 99, 132, 0.8)",
          "rgba(54, 162, 235, 0.8)",
          "rgba(255, 206, 86, 0.8)",
          "rgba(75, 192, 192, 0.8)",
          "rgba(153, 102, 255, 0.8)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const predictionDistributionData = {
    labels: ["Benign", "Malignant"],
    datasets: [
      {
        data: [65, 35],
        backgroundColor: ["rgba(75, 192, 192, 0.8)", "rgba(255, 99, 132, 0.8)"],
        borderColor: ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)"],
        borderWidth: 2,
      },
    ],
  };

  const modelPerformanceData = {
    labels: ["Accuracy", "Precision", "Recall", "F1-Score"],
    datasets: [
      {
        label: "Model Performance",
        data: [0.92, 0.89, 0.94, 0.91],
        backgroundColor: "rgba(54, 162, 235, 0.8)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Breast Cancer Prediction Model Analytics",
      },
    },
  };

  return (
    <div>
      <div className="hero-section text-center mb-4">
        <h1>
          <i className="fas fa-chart-bar me-3"></i>Model Analytics &
          Visualizations
        </h1>
        <p className="lead">
          Explore model performance, feature importance, and prediction
          distributions
        </p>
      </div>

      <Row>
        <Col md={6}>
          <Card className="visualization-card mb-4">
            <Card.Body>
              <Card.Title>
                <i className="fas fa-chart-pie me-2"></i>Feature Importance
              </Card.Title>
              <Bar data={featureImportanceData} options={chartOptions} />
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="visualization-card mb-4">
            <Card.Body>
              <Card.Title>
                <i className="fas fa-chart-doughnut me-2"></i>Prediction
                Distribution
              </Card.Title>
              <Doughnut
                data={predictionDistributionData}
                options={chartOptions}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col md={12}>
          <Card className="visualization-card">
            <Card.Body>
              <Card.Title>
                <i className="fas fa-chart-line me-2"></i>Model Performance
                Metrics
              </Card.Title>
              <Bar data={modelPerformanceData} options={chartOptions} />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={12}>
          <Card>
            <Card.Body>
              <Card.Title>
                <i className="fas fa-info-circle me-2"></i>Model Statistics
              </Card.Title>
              <Row>
                <Col md={3}>
                  <div className="text-center">
                    <h4 className="text-primary">92%</h4>
                    <p>Accuracy</p>
                  </div>
                </Col>
                <Col md={3}>
                  <div className="text-center">
                    <h4 className="text-success">89%</h4>
                    <p>Precision</p>
                  </div>
                </Col>
                <Col md={3}>
                  <div className="text-center">
                    <h4 className="text-warning">94%</h4>
                    <p>Recall</p>
                  </div>
                </Col>
                <Col md={3}>
                  <div className="text-center">
                    <h4 className="text-info">91%</h4>
                    <p>F1-Score</p>
                  </div>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default VisualizeTab;
