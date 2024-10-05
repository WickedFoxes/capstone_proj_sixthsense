import { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function CreateProject({ show, onHide }) {
  const [projectTitle, setProjectTitle] = useState("");
  const [projectDescription, setProjectDescription] = useState("");

  // 저장 버튼 클릭 시 프로젝트 생성 요청
  const handleSave = async () => {
    try {
      const response = await axios.post(`${API.PROJECTCREATE}`, {
        title: projectTitle,
        description: projectDescription,
      });
      if (response.status === 201) {
        console.log("프로젝트가 성공적으로 생성되었습니다.");
        onHide(); // 모달 닫기
        // 상태 초기화 (선택사항)
        setProjectTitle("");
        setProjectDescription("");
      }
    } catch (error) {
      console.error("프로젝트 생성 중 오류 발생:", error);
    }
  };

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>프로젝트 생성</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
            <Form.Label>프로젝트 이름</Form.Label>
            <Form.Control
              type="text"
              placeholder="프로젝트 이름을 입력하세요"
              value={projectTitle}
              onChange={(e) => setProjectTitle(e.target.value)}
              autoFocus
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
            <Form.Label>프로젝트 설명</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={projectDescription}
              onChange={(e) => setProjectDescription(e.target.value)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          닫기
        </Button>
        <Button variant="primary" onClick={handleSave}>
          저장
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default CreateProject;
