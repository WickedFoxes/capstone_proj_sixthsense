import { useState } from "react";
import PropTypes from "prop-types";
import { Button, Form, Modal, ListGroup } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import PageAddModal from "./PageAddModal";
import { API } from "../config";

axios.defaults.withCredentials = true;

function CreateProject({ show, onHide, onSave }) {
  const [projectTitle, setProjectTitle] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [pageList, setPageList] = useState([]);
  const [showPageAddModal, setShowPageAddModal] = useState(false); // 페이지 추가 모달 상태

  const handleAddPage = (newPage) => {
    setPageList([...pageList, newPage]); // 새 페이지 추가
  };

  const handleRemovePage = (index) => {
    const updatedPageList = pageList.filter((_, idx) => idx !== index);
    setPageList(updatedPageList);
  };

  const handleSave = async () => {
    try {
      const requestData = {
        project: {
          title: projectTitle,
          description: projectDescription,
        },
        pageList: pageList.map((page) => ({
          title: page.title,
          pagetype: page.pagetype,
          url: page.pagetype === "URL" ? page.url : undefined,
          htmlbody: page.pagetype === "TEXT" ? page.htmlbody : undefined,
        })),
      };

      const response = await axios.post(
        `${API.PROJECT_PAGE_CREATE}`,
        requestData
      );
      if (response.status === 201) {
        console.log("프로젝트가 성공적으로 생성되었습니다.");
        setProjectTitle("");
        setProjectDescription("");
        setPageList([]);
        onSave(); // Menubar 컴포넌트에서 목록 새로고침 및 모달 닫기
      }
    } catch (error) {
      console.error("프로젝트 생성 중 오류 발생:", error);
    }
  };

  return (
    <>
      <Modal show={show} onHide={onHide}>
        <Modal.Header closeButton>
          <Modal.Title>검사 페이지 생성</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="formProjectTitle">
              <Form.Label>사이트 이름</Form.Label>
              <Form.Control
                type="text"
                placeholder="사이트 이름을 입력하세요."
                value={projectTitle}
                onChange={(e) => setProjectTitle(e.target.value)}
                autoFocus
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formProjectDescription">
              <Form.Label>사이트 설명</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                placeholder="사이트 설명을 입력하세요."
                value={projectDescription}
                onChange={(e) => setProjectDescription(e.target.value)}
              />
            </Form.Group>

            <ListGroup>
              {pageList.map((page, index) => (
                <ListGroup.Item
                  key={index}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <strong>{page.title || "제목 없음"}</strong> -{" "}
                    {page.pagetype === "URL" ? page.url : "HTML"}
                  </div>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleRemovePage(index)}
                    style={{
                      flexShrink: 0,
                      width: "60px",
                      textAlign: "center",
                    }}
                  >
                    삭제
                  </Button>
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="success"
            onClick={() => setShowPageAddModal(true)} // 페이지 추가 모달 열기
          >
            + 검사 페이지 추가
          </Button>
          <Button variant="primary" onClick={handleSave}>
            저장
          </Button>
        </Modal.Footer>
      </Modal>

      <PageAddModal
        show={showPageAddModal}
        onHide={() => setShowPageAddModal(false)}
        onSave={handleAddPage}
      />
    </>
  );
}

CreateProject.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
};

export default CreateProject;
