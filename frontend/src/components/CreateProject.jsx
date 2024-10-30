import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { Button, Form, Modal, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function CreateProject({ show, onHide, onSave }) {
  const [projectTitle, setProjectTitle] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [pageList, setPageList] = useState([{ url: "", isSaved: false }]);
  const [isUrlEmpty, setIsUrlEmpty] = useState(true);

  const handleAddUrl = () => {
    const updatedPageList = pageList.map((page) => ({
      ...page,
      isSaved: true,
    }));
    setPageList([...updatedPageList, { url: "", isSaved: false }]);
  };

  const handleRemoveUrl = (index) => {
    const updatedPageList = pageList.filter((_, idx) => idx !== index);
    setPageList(updatedPageList);
  };

  const handleUrlChange = (index, value) => {
    const updatedPageList = [...pageList];
    updatedPageList[index].url = value;
    setPageList(updatedPageList);
  };

  useEffect(() => {
    const lastPage = pageList[pageList.length - 1];
    setIsUrlEmpty(lastPage.url.trim() === "");
  }, [pageList]);

  const handleSave = async () => {
    try {
      const requestData = {
        project: {
          title: projectTitle,
          description: projectDescription,
        },
        pageList: pageList.map((page) => ({ title: "", url: page.url })),
      };

      const response = await axios.post(
        `${API.PROJECT_PAGE_CREATE}`,
        requestData
      );
      if (response.status === 201) {
        console.log("프로젝트가 성공적으로 생성되었습니다.");
        setProjectTitle("");
        setProjectDescription("");
        setPageList([{ url: "", isSaved: false }]);

        onSave(); // Menubar 컴포넌트에서 목록 새로고침 및 모달 닫기
      }
    } catch (error) {
      console.error("프로젝트 생성 중 오류 발생:", error);
    }
  };

  return (
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

          {pageList.map((page, index) => (
            <div key={index} className="mb-3">
              <Row>
                <Col sm="10">
                  <Form.Control
                    type="text"
                    placeholder={`검사 페이지 URL (${index + 1})`}
                    value={page.url}
                    onChange={(e) => handleUrlChange(index, e.target.value)}
                    className="mb-2"
                  />
                </Col>
                <Col sm="2">
                  {page.isSaved && (
                    <Button
                      variant="danger"
                      onClick={() => handleRemoveUrl(index)}
                      className="mb-2"
                    >
                      삭제
                    </Button>
                  )}
                </Col>
              </Row>
            </div>
          ))}

          <Button
            variant="outline-primary"
            onClick={handleAddUrl}
            className="mb-3"
            disabled={isUrlEmpty}
          >
            + URL 추가
          </Button>
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

CreateProject.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
};

export default CreateProject;
