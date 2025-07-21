import React from "react";
import {
  Card,
  Container,
  Row,
  Col,
  Accordion,
  Table,
  Badge,
} from "react-bootstrap";

const GLOSSARY = [
  {
    term: "Carcinoma",
    definition:
      "A cancer that begins in the skin or in tissues that line or cover internal organs.",
  },
  {
    term: "Metastasis",
    definition:
      "The spread of cancer cells from the place where they first formed to another part of the body.",
  },
  {
    term: "Mammogram",
    definition:
      "An X-ray picture of the breast used to detect tumors or other abnormalities.",
  },
  {
    term: "BRCA1/2",
    definition:
      "Genes that, when mutated, increase the risk of breast and ovarian cancer.",
  },
  {
    term: "Lumpectomy",
    definition:
      "Surgical removal of a lump from the breast, typically when cancer is present but localized.",
  },
  {
    term: "Chemotherapy",
    definition:
      "Treatment of cancer with drugs that kill or slow the growth of cancer cells.",
  },
  {
    term: "Immunotherapy",
    definition:
      "Treatment that uses certain parts of a person’s immune system to fight diseases such as cancer.",
  },
  {
    term: "Hormone Therapy",
    definition:
      "Treatment that adds, blocks, or removes hormones to slow or stop the growth of cancer cells.",
  },
  {
    term: "Invasive",
    definition:
      "Cancer that has spread beyond the layer of tissue in which it developed and is growing into surrounding, healthy tissues.",
  },
  {
    term: "Benign",
    definition:
      "A tumor that is not cancerous and does not spread to other parts of the body.",
  },
];

const sectionStyle = {
  background: "#f8f9fa",
  borderRadius: "12px",
  padding: "24px 18px",
  marginBottom: "32px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.04)",
};

const dividerStyle = {
  border: 0,
  height: "2px",
  background: "linear-gradient(90deg, #6c63ff 0%, #e66465 100%)",
  margin: "32px 0 24px 0",
};

const AboutCancerTab = () => (
  <Container className="mt-4 mb-5">
    <Row>
      <Col md={12}>
        <div className="about-cancer-section fade-in">
          <h4 className="mb-3">
            <i className="fas fa-dna me-2 text-primary"></i>About Cancer
          </h4>
          <h5 className="mt-4">
            <i className="fas fa-disease me-2 text-danger"></i>What is Cancer?
          </h5>
          <p>
            <strong>Cancer</strong> is a group of diseases characterized by the
            uncontrolled growth and spread of abnormal cells. If the spread is
            not controlled, it can result in death. Cancer can develop in almost
            any organ or tissue, such as the lung, colon, breast, skin, bones,
            or nerve tissue.
          </p>
          <h5 className="mt-4">
            <i className="fas fa-dna me-2 text-info"></i>How Does Cancer
            Develop?
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-arrow-right text-primary me-2"></i>Cancer
              begins when genetic mutations disrupt normal cell growth and
              division.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-arrow-right text-primary me-2"></i>These
              mutations may be inherited or caused by environmental exposures
              (e.g., tobacco, radiation, chemicals, infections).
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-arrow-right text-primary me-2"></i>Cancer
              cells can invade nearby tissues and spread (metastasize) to other
              parts of the body.
            </div>
          </div>
          <div className="text-center mb-3">
            <img
              src="https://www.cancer.gov/sites/g/files/xnrzdm211/files/styles/cgov_article/public/cgov_image/media_image/2021-07/cancer-spread-diagram.png"
              alt="Diagram showing how cancer spreads"
              style={{
                maxWidth: "400px",
                width: "100%",
                border: "1px solid #eee",
              }}
              onError={(e) => {
                e.target.onerror = null;
                e.target.src =
                  "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Cancer_cell_diagram_en.svg/400px-Cancer_cell_diagram_en.svg.png";
              }}
            />
            <div className="text-muted small mt-1">
              Source: National Cancer Institute
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-exclamation-triangle me-2 text-warning"></i>
            Common Risk Factors
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Age (risk
              increases with age)
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Family history
              of cancer
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Smoking and
              tobacco use
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Excessive
              alcohol consumption
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Poor diet and
              lack of physical activity
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Certain
              infections (e.g., HPV, hepatitis B/C, H. pylori)
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-shield-alt me-2 text-success"></i>Prevention
            and Early Detection
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-check-circle text-success me-2"></i>Avoid
              tobacco and limit alcohol use
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-check-circle text-success me-2"></i>Maintain
              a healthy weight and diet
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-check-circle text-success me-2"></i>Exercise
              regularly
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-check-circle text-success me-2"></i>Protect
              skin from excessive sun exposure
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-check-circle text-success me-2"></i>Get
              vaccinated against cancer-related infections (e.g., HPV, hepatitis
              B)
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-check-circle text-success me-2"></i>
              Participate in recommended cancer screening programs (e.g.,
              mammograms, colonoscopies)
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-globe-americas me-2 text-secondary"></i>Global
            Cancer Statistics
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-globe text-secondary me-2"></i>There are over
              19 million new cancer cases and nearly 10 million cancer deaths
              worldwide each year (GLOBOCAN 2020).
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-globe text-secondary me-2"></i>The most
              common cancers globally are breast, lung, colorectal, prostate,
              and stomach cancer.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-globe text-secondary me-2"></i>Survival rates
              vary widely depending on cancer type, stage at diagnosis, and
              access to care.
            </div>
          </div>
        </div>
        <hr className="about-cancer-divider" />
        <div className="about-cancer-section fade-in">
          <h4 className="mb-3">
            <i className="fas fa-ribbon me-2 text-pink"></i>About Breast Cancer
          </h4>
          <h5 className="mt-4">
            <i className="fas fa-female me-2 text-danger"></i>What is Breast
            Cancer?
          </h5>
          <p>
            <strong>Breast cancer</strong> is the most common cancer in women
            worldwide and can also affect men (though rarely). It begins when
            cells in the breast grow out of control, forming a tumor that can
            often be seen on an x-ray or felt as a lump.
          </p>
          <h5 className="mt-4">
            <i className="fas fa-video me-2 text-info"></i>Educational Video:
            Breast Cancer Explained
          </h5>
          <div className="text-center mb-3">
            <iframe
              width="400"
              height="225"
              src="https://www.youtube.com/embed/6EdI5bQn4v8"
              title="Breast Cancer Explained"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              referrerPolicy="no-referrer"
              style={{ maxWidth: "100%" }}
              onError={(e) => {
                const fallback = document.createElement("div");
                fallback.innerHTML =
                  "<div style=\"color:#b00; font-weight:bold; margin-top:1em;\">Video could not be loaded. <a href='https://www.youtube.com/watch?v=6EdI5bQn4v8' target='_blank' rel='noopener noreferrer'>Watch on YouTube</a></div>";
                e.target.replaceWith(fallback);
              }}
            ></iframe>
            <div className="text-muted small mt-1">
              Source: Cancer Research UK (YouTube)
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-vials me-2 text-primary"></i>Breast Cancer
            Subtypes
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-flask text-primary me-2"></i>
              <strong>Invasive ductal carcinoma (IDC):</strong> The most common
              type, starting in the milk ducts and invading surrounding tissue.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-flask text-primary me-2"></i>
              <strong>Invasive lobular carcinoma (ILC):</strong> Begins in the
              milk-producing lobules.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-flask text-primary me-2"></i>
              <strong>Triple-negative breast cancer:</strong> Lacks estrogen,
              progesterone, and HER2 receptors; often more aggressive.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-flask text-primary me-2"></i>
              <strong>HER2-positive breast cancer:</strong> Has high levels of
              HER2 protein, which promotes cancer growth.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-flask text-primary me-2"></i>
              <strong>Hormone receptor-positive:</strong> Grows in response to
              estrogen and/or progesterone.
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-exclamation-circle me-2 text-warning"></i>Risk
            Factors for Breast Cancer
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Female gender
              (but can occur in men)
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Increasing age
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Family history
              of breast or ovarian cancer
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Inherited gene
              mutations (e.g., BRCA1/2)
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Early
              menstruation or late menopause
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Never having
              children or having first child after age 30
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Hormone
              replacement therapy
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Obesity and
              lack of physical activity
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Alcohol
              consumption
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-circle text-warning me-2"></i>Previous chest
              radiation
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-eye me-2 text-success"></i>Symptoms of Breast
            Cancer
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-eye text-success me-2"></i>Lump or thickening
              in the breast or underarm
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-eye text-success me-2"></i>Change in size,
              shape, or appearance of the breast
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-eye text-success me-2"></i>Unexplained pain
              in the breast or nipple
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-eye text-success me-2"></i>Nipple discharge
              (other than breast milk)
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-eye text-success me-2"></i>Redness or scaling
              of the nipple or breast skin
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-search me-2 text-info"></i>Screening and Early
            Detection
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-search text-info me-2"></i>Regular mammograms
              (x-ray of the breast) are the best way to detect breast cancer
              early.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-search text-info me-2"></i>Clinical breast
              exams and breast self-exams can help detect changes.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-search text-info me-2"></i>Early detection
              greatly improves the chances of successful treatment and survival.
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-stethoscope me-2 text-primary"></i>Treatment
            Options
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-stethoscope text-primary me-2"></i>Surgery
              (lumpectomy, mastectomy)
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-stethoscope text-primary me-2"></i>Radiation
              therapy
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-stethoscope text-primary me-2"></i>
              Chemotherapy
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-stethoscope text-primary me-2"></i>Hormone
              therapy
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-stethoscope text-primary me-2"></i>Targeted
              therapy (e.g., HER2 inhibitors)
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-stethoscope text-primary me-2"></i>
              Immunotherapy (for some subtypes)
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-stethoscope text-primary me-2"></i>Treatment
              is personalized based on cancer subtype, stage, and patient
              preferences.
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-heart me-2 text-danger"></i>Survivorship and
            Support
          </h5>
          <div className="about-cancer-list">
            <div className="about-cancer-list-item">
              <i className="fas fa-heart text-danger me-2"></i>Many women live
              long, healthy lives after breast cancer treatment.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-heart text-danger me-2"></i>Follow-up care,
              healthy lifestyle, and emotional support are important for
              survivors.
            </div>
            <div className="about-cancer-list-item">
              <i className="fas fa-heart text-danger me-2"></i>Support groups
              and counseling can help patients and families cope with diagnosis
              and treatment.
            </div>
          </div>
          <h5 className="mt-4">
            <i className="fas fa-link me-2 text-secondary"></i>Trusted Resources
          </h5>
          <ul>
            <li>
              <a
                href="https://www.cancer.org/cancer/breast-cancer.html"
                target="_blank"
                rel="noopener noreferrer"
              >
                American Cancer Society: Breast Cancer
              </a>
            </li>
            <li>
              <a
                href="https://www.cancer.gov/types/breast"
                target="_blank"
                rel="noopener noreferrer"
              >
                National Cancer Institute: Breast Cancer
              </a>
            </li>
            <li>
              <a
                href="https://www.breastcancer.org/"
                target="_blank"
                rel="noopener noreferrer"
              >
                Breastcancer.org
              </a>
            </li>
            <li>
              <a
                href="https://www.who.int/news-room/fact-sheets/detail/breast-cancer"
                target="_blank"
                rel="noopener noreferrer"
              >
                World Health Organization: Breast Cancer
              </a>
            </li>
          </ul>
          <p className="mt-3 text-muted">
            <strong>Note:</strong> This AI system is designed to assist with
            breast cancer prediction and should not replace professional medical
            advice. Always consult a healthcare provider for diagnosis and
            treatment decisions.
          </p>
        </div>
        <hr className="about-cancer-divider" />
        <div className="about-cancer-section fade-in">
          <h4 className="mb-3">
            <i className="fas fa-book me-2 text-info"></i>Glossary of Cancer
            Terms
          </h4>
          <Table striped bordered hover size="sm" className="bg-white">
            <thead>
              <tr>
                <th>Term</th>
                <th>Definition</th>
              </tr>
            </thead>
            <tbody>
              {GLOSSARY.map((item) => (
                <tr key={item.term}>
                  <td>
                    <Badge bg="primary" className="me-2">
                      {item.term}
                    </Badge>
                  </td>
                  <td>{item.definition}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </Col>
    </Row>
  </Container>
);

export default AboutCancerTab;
