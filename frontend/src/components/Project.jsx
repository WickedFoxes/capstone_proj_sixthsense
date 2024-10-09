import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, Row, Col, Dropdown, Modal, Form } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function Project() {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null); // 수정할 프로젝트 선택
  const [showEditModal, setShowEditModal] = useState(false); // 수정 모달 표시 여부
  const navigate = useNavigate();

  // 프로젝트 페이지로 이동
  const goProjectPage = (projectId) => {
    navigate(`/project/${projectId}`);
  };

  useEffect(() => {
    // 백엔드에서 프로젝트 정보 가져오기
    const fetchProjects = async () => {
      try {
        const response = await axios.get(`${API.PROJECTLIST}`);
        if (response.status === 200 && Array.isArray(response.data)) {
          setProjects(response.data);
        }
      } catch (error) {
        console.error("Error fetching project list:", error);
      }
    };

    fetchProjects();
  }, []);

  // 프로젝트 수정 요청
  const handleProjectUpdate = async () => {
    if (!selectedProject) return;
    try {
      const response = await axios.put(`${API.PROJECTUPDATE}`, {
        id: selectedProject.id, // 수정할 프로젝트 ID
        title: selectedProject.title,
        description: selectedProject.description,
      });

      if (response.status === 201) {
        // 성공적으로 업데이트되면 목록을 업데이트
        setProjects((prevProjects) =>
          prevProjects.map((project) =>
            project.id === selectedProject.id ? selectedProject : project
          )
        );
        setShowEditModal(false); // 모달 닫기
      }
    } catch (error) {
      console.error("프로젝트 수정 중 오류 발생:", error);
    }
  };

  // 프로젝트 삭제 요청
  const handleProjectDelete = async (projectId) => {
    const confirmDelete = window.confirm(
      "정말로 이 프로젝트를 삭제하시겠습니까?"
    );
    if (!confirmDelete) return;

    try {
      const response = await axios.delete(`${API.PROJECTDELETE}`, {
        data: { id: projectId }, // 프로젝트 ID를 데이터로 넘겨줌
      });

      if (response.status === 202) {
        // 성공적으로 삭제되면 목록에서 제거
        setProjects((prevProjects) =>
          prevProjects.filter((p) => p.id !== projectId)
        );
      }
    } catch (error) {
      console.error("프로젝트 삭제 중 오류 발생:", error);
    }
  };

  return (
    <Row className="justify-content-start" style={{ margin: "20px" }}>
      {projects.map((project, index) => (
        <Col key={index} xs={12} sm={6} md={4} className="mb-3">
          <Card style={{ width: "auto", height: "auto", margin: "5px" }}>
            <Card.Body style={{ position: "relative" }}>
              <Card.Title>{project.title}</Card.Title>
              <Card.Text>{project.description}</Card.Text>

              {/* 프로젝트로 이동 버튼 */}
              <Button
                variant="outline-primary"
                onClick={() => goProjectPage(project.id)}
              >
                보러가기
              </Button>

              {/* 우측 상단 편집 메뉴 */}
              <Dropdown
                style={{ position: "absolute", top: "10px", right: "10px" }}
              >
                <Dropdown.Toggle
                  variant="outline-secondary"
                  id="dropdown-basic"
                >
                  편집
                </Dropdown.Toggle>

                <Dropdown.Menu>
                  <Dropdown.Item
                    onClick={() => {
                      setSelectedProject(project);
                      setShowEditModal(true);
                    }}
                  >
                    수정
                  </Dropdown.Item>
                  <Dropdown.Item
                    onClick={() => handleProjectDelete(project.id)}
                  >
                    삭제
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Card.Body>
          </Card>
        </Col>
      ))}

      {/* 수정 모달 창 */}
      <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>프로젝트 수정</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedProject && (
            <Form>
              <Form.Group className="mb-3" controlId="formProjectTitle">
                <Form.Label>프로젝트 이름</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="프로젝트 이름을 입력하세요"
                  value={selectedProject.title}
                  onChange={(e) =>
                    setSelectedProject({
                      ...selectedProject,
                      title: e.target.value,
                    })
                  }
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formProjectDescription">
                <Form.Label>프로젝트 설명</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  placeholder="프로젝트 설명을 입력하세요"
                  value={selectedProject.description}
                  onChange={(e) =>
                    setSelectedProject({
                      ...selectedProject,
                      description: e.target.value,
                    })
                  }
                />
              </Form.Group>
            </Form>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowEditModal(false)}>
            닫기
          </Button>
          <Button variant="primary" onClick={handleProjectUpdate}>
            저장
          </Button>
        </Modal.Footer>
      </Modal>
    </Row>
  );
}

export default Project;
