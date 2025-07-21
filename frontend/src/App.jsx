import React, { useState, useEffect } from "react";
import { Container, Nav, Navbar, Tab, Tabs } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import PredictionTab from "./components/PredictionTab";
import UploadTab from "./components/UploadTab";
import VisualizeTab from "./components/VisualizeTab";
import InfoTab from "./components/InfoTab";
import ComprehensivePredictionTab from "./components/ComprehensivePredictionTab";
import ComprehensiveUploadTab from "./components/ComprehensiveUploadTab";
import AboutCancerTab from "./components/AboutCancerTab";

// API Configuration
const API_BASE_URL = "http://localhost:8000";

function App() {
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchModelInfo();
  }, []);

  const fetchModelInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/model-info`);
      const data = await response.json();
      setModelInfo(data);
    } catch (error) {
      console.error("Error fetching model info:", error);
    }
  };

  return (
    <div className="App">
      {/* Navigation */}
      <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
        <Container>
          <Navbar.Brand href="#">
            <i className="fas fa-dna me-2"></i>
            Breast Cancer AI Prediction System
          </Navbar.Brand>
        </Container>
      </Navbar>

      {/* Main Content */}
      <Container>
        <Tabs defaultActiveKey="comprehensive" id="main-tabs" className="mb-4">
          <Tab
            eventKey="comprehensive"
            title={
              <span>
                <i className="fas fa-brain me-1"></i> All Predictions
              </span>
            }
          >
            <ComprehensivePredictionTab />
          </Tab>
          <Tab
            eventKey="prediction"
            title={
              <span>
                <i className="fas fa-chart-line me-1"></i> Single Prediction
              </span>
            }
          >
            <PredictionTab />
          </Tab>
          <Tab
            eventKey="upload"
            title={
              <span>
                <i className="fas fa-upload me-1"></i> Batch Upload
              </span>
            }
          >
            <ComprehensiveUploadTab />
          </Tab>
          <Tab
            eventKey="visualize"
            title={
              <span>
                <i className="fas fa-chart-bar me-1"></i> Visualizations
              </span>
            }
          >
            <VisualizeTab />
          </Tab>
          <Tab
            eventKey="info"
            title={
              <span>
                <i className="fas fa-info-circle me-1"></i> Model Info
              </span>
            }
          >
            <InfoTab modelInfo={modelInfo} />
          </Tab>
          <Tab
            eventKey="about"
            title={
              <span>
                <i className="fas fa-info-circle me-1"></i> About Cancer
              </span>
            }
          >
            <AboutCancerTab />
          </Tab>
        </Tabs>
      </Container>
    </div>
  );
}

export default App;
