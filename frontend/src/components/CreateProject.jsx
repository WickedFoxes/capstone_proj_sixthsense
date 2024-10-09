import { useState, useEffect } from "react";
import { Button, Form, Modal, Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function CreateProject({ show, onHide }) {
  const [projectTitle, setProjectTitle] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [pageList, setPageList] = useState([{ url: "", isSaved: false }]); // 초기 URL 상태
  const [isUrlEmpty, setIsUrlEmpty] = useState(true); // URL 입력 필드가 비어있는지 확인

  // URL 추가 핸들러
  const handleAddUrl = () => {
    const updatedPageList = pageList.map((page) => ({
      ...page,
      isSaved: true, // 기존 URL 항목의 삭제 버튼 보이도록 설정
    }));
    setPageList([...updatedPageList, { url: "", isSaved: false }]); // 새로운 URL 객체 추가
  };

  // URL 삭제 핸들러
  const handleRemoveUrl = (index) => {
    const updatedPageList = pageList.filter((_, idx) => idx !== index);
    setPageList(updatedPageList);
  };

  // 개별 URL 입력 핸들러
  const handleUrlChange = (index, value) => {
    const updatedPageList = [...pageList];
    updatedPageList[index].url = value;
    setPageList(updatedPageList);
  };

  // 마지막 URL 입력 필드가 비어있는지 확인하여 추가 버튼 상태 업데이트
  useEffect(() => {
    const lastPage = pageList[pageList.length - 1];
    setIsUrlEmpty(lastPage.url.trim() === ""); // 마지막 URL이 비어있으면 true, 아니면 false
  }, [pageList]);

  // 저장 버튼 클릭 시 프로젝트 생성 요청
  const handleSave = async () => {
    try {
      const requestData = {
        project: {
          title: projectTitle,
          description: projectDescription,
        },
        pageList: pageList.map((page) => ({ title: "", url: page.url })), // title은 ""
      };

      const response = await axios.post(
        `${API.PROJECT_PAGE_CREATE}`,
        requestData
      );
      if (response.status === 201) {
        console.log("프로젝트가 성공적으로 생성되었습니다.");
        onHide(); // 모달 닫기
        setProjectTitle("");
        setProjectDescription("");
        setPageList([{ url: "", isSaved: false }]); // 상태 초기화
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

          {/* URL 입력 필드 반복 렌더링 */}
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
                  {/* 삭제 버튼: 기존 URL 항목이 추가된 후 표시되도록 설정 */}
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

          {/* URL 추가 버튼 */}
          <Button
            variant="outline-primary"
            onClick={handleAddUrl}
            className="mb-3"
            disabled={isUrlEmpty} // 마지막 URL 입력 필드가 비어있을 경우 비활성화
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

export default CreateProject;
