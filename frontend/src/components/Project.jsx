import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";

const API_BASE_URL = "http://localhost:8080";
axios.defaults.withCredentials = true;

function Project() {
  const [projects, setProjects] = useState([]);
  const navigate = useNavigate();

  // 프로젝트 페이지로 이동
  const goProjectPage = (projectId) => {
    navigate(`/project/${projectId}`);
  };

  useEffect(() => {
    // 백엔드에서 프로젝트 정보 가져오기
    const fetchProjects = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/project/list`);
        if (response.status === 200 && Array.isArray(response.data)) {
          setProjects(response.data);
        }
      } catch (error) {
        console.error("Error fetching project list:", error);
      }
    };

    fetchProjects();
  }, []);

  return (
    <Row className="justify-content-start" style={{ margin: "20px" }}>
      {projects.map((project, index) => (
        <Col key={index} xs={12} sm={6} md={4} className="mb-3">
          <Card style={{ width: "auto", height: "auto", margin: "5px" }}>
            <Card.Img variant="top" src="holder.js/100px180" />
            <Card.Body>
              <Card.Title>{project.title}</Card.Title>
              <Card.Text>{project.description}</Card.Text>
              <Button
                variant="outline-primary"
                onClick={() => goProjectPage(project.id)}
              >
                보러가기
              </Button>
            </Card.Body>
          </Card>
        </Col>
      ))}
    </Row>
  );
}

export default Project;
