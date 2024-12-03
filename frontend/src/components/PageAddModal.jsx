import { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import PropTypes from "prop-types";

PageAddModal.propTypes = {
  show: PropTypes.bool.isRequired, // 모달 표시 여부
  onHide: PropTypes.func.isRequired, // 모달 닫기 함수
  onSave: PropTypes.func.isRequired, // 저장 버튼 동작 함수
};

function PageAddModal({ show, onHide, onSave }) {
  const [pageType, setPageType] = useState("URL"); // 드롭다운 선택 값
  const [title, setTitle] = useState(""); // Title 입력 값
  const [url, setUrl] = useState(""); // URL 입력 값
  const [htmlBody, setHtmlBody] = useState(""); // HTML 입력 값

  const handleSave = () => {
    const pageData = {
      title,
      pagetype: pageType,
    };

    if (pageType === "URL") {
      pageData.url = url;
    } else if (pageType === "TEXT") {
      pageData.htmlbody = htmlBody;
      pageData.url = url; // HTML 선택 시 URL도 필수
    }

    onSave(pageData);
    resetFields(); // 입력 필드 초기화
    onHide();
  };

  const resetFields = () => {
    setPageType("URL");
    setTitle("");
    setUrl("");
    setHtmlBody("");
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>페이지 추가</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          {/* Title 입력 */}
          <Form.Group controlId="formTitle" className="mb-3">
            <Form.Label>페이지 제목</Form.Label>
            <Form.Control
              type="text"
              placeholder="페이지 제목을 입력하세요."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </Form.Group>

          {/* 드롭다운으로 PageType 선택 */}
          <Form.Group controlId="formPageType" className="mb-3">
            <Form.Label>페이지 유형</Form.Label>
            <Form.Select
              value={pageType}
              onChange={(e) => setPageType(e.target.value)}
            >
              <option value="URL">URL</option>
              <option value="TEXT">HTML</option>
            </Form.Select>
          </Form.Group>

          {/* URL 입력 (항상 표시) */}
          <Form.Group controlId="formUrl" className="mb-3">
            <Form.Label>URL</Form.Label>
            <Form.Control
              type="text"
              placeholder="URL을 입력하세요."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </Form.Group>

          {/* HTML 입력 */}
          {pageType === "TEXT" && (
            <Form.Group controlId="formHtmlBody" className="mb-3">
              <Form.Label>HTML 내용</Form.Label>
              <Form.Control
                as="textarea"
                rows={5}
                placeholder="HTML 코드를 입력하세요."
                value={htmlBody}
                onChange={(e) => setHtmlBody(e.target.value)}
              />
            </Form.Group>
          )}
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button
          variant="primary"
          onClick={handleSave}
          disabled={
            title.trim() === "" || // 제목 필수
            url.trim() === "" || // URL 필수
            (pageType === "TEXT" && htmlBody.trim() === "") // HTML일 때 HTML 내용 필수
          }
        >
          저장
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default PageAddModal;
