import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Button, Form, Row, Col, Container } from "react-bootstrap";
import axios from "axios";
import { API } from "../config";
import ReportExport from "./ReportExport"; // ReportExport 컴포넌트 가져오기
import ScheduleModal from "./ScheduleModal"; // ScheduleModal 컴포넌트 가져오기

axios.defaults.withCredentials = true;

function UrlInput() {
  const { projectId } = useParams(); // URL에서 projectId 추출
  const [projects, setProjects] = useState([]); // 모든 프로젝트 목록을 저장
  const [projectTitle, setProjectTitle] = useState(""); // 현재 선택된 프로젝트의 타이틀 상태
  const [title, setTitle] = useState(""); // Title 상태
  const [url, setUrl] = useState(""); // URL 상태
  const [htmlBody, setHtmlBody] = useState(""); // HTML 상태
  const [pageType, setPageType] = useState("URL"); // 드롭다운 선택 값 (URL/TEXT)
  const [isButtonDisabled, setIsButtonDisabled] = useState(true); // 등록 버튼 비활성화 상태

  const [showScheduleModal, setShowScheduleModal] = useState(false); // 검사 예약 모달 상태

  // 전체 프로젝트 목록 가져오기
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await axios.get(API.PROJECTLIST);
        if (response.status === 200 && Array.isArray(response.data)) {
          setProjects(response.data); // 전체 프로젝트 목록을 상태에 저장
        }
      } catch (error) {
        console.error("Error fetching project list:", error);
      }
    };

    fetchProjects();
  }, []);

  // projectId가 변경될 때마다 해당 프로젝트 타이틀 설정
  useEffect(() => {
    if (projects.length > 0 && projectId) {
      const selectedProject = projects.find(
        (project) => project.id.toString() === projectId
      );
      if (selectedProject) {
        setProjectTitle(selectedProject.title);
      }
    }
  }, [projects, projectId]);

  // 등록 버튼 활성화 상태 업데이트
  useEffect(() => {
    if (
      title.trim() === "" || // 제목이 비어 있으면 비활성화
      (pageType === "URL" && url.trim() === "") || // URL 타입에서 URL이 비어 있으면 비활성화
      (pageType === "TEXT" && (url.trim() === "" || htmlBody.trim() === "")) // HTML 타입에서 URL 또는 HTML이 비어 있으면 비활성화
    ) {
      setIsButtonDisabled(true);
    } else {
      setIsButtonDisabled(false);
    }
  }, [title, url, htmlBody, pageType]);

  // 등록 버튼 클릭 시 페이지 생성 요청
  const handleSubmit = async (event) => {
    event.preventDefault();

    const requestData = {
      title,
      pagetype: pageType,
    };

    if (pageType === "URL") {
      requestData.url = url;
    } else if (pageType === "TEXT") {
      requestData.htmlbody = htmlBody;
      if (url.trim() !== "") {
        requestData.url = url;
      }
    }

    try {
      const response = await axios.post(
        `${API.PAGECREATE}${projectId}`,
        requestData
      );

      if (response.status === 201) {
        alert("페이지가 성공적으로 생성되었습니다!");
        resetFields(); // 입력 필드 초기화
      }
    } catch (error) {
      console.error("Error creating page:", error);
      alert("페이지 생성 중 오류가 발생했습니다.");
    }
  };

  const resetFields = () => {
    setTitle("");
    setUrl("");
    setHtmlBody("");
    setPageType("URL");
  };

  // 페이지 전체 검사
  const handleAllPageRun = async () => {
    try {
      const response = await axios.post(`${API.ALLPAGERUN}${projectId}`);
      if (response.status === 200) {
        alert("모든 페이지 검사를 시작합니다.");
      }
    } catch (error) {
      console.error("Error running all page tests:", error);
      alert("모든 페이지 검사 중 오류가 발생했습니다.");
    }
  };

  return (
    <Container className="d-flex flex-column align-items-center">
      <Form style={{ width: "70%" }} onSubmit={handleSubmit}>
        {projectTitle ? (
          <h4 className="mb-4 text-center">
            {projectTitle} 에서 추가로 검사할 페이지를 등록하세요.
          </h4>
        ) : (
          <h4 className="mb-4 text-center">프로젝트 정보를 불러오는 중...</h4>
        )}

        {/* Title 입력 */}
        <Form.Group as={Row} className="mb-4" controlId="formBasicTitle">
          <Form.Label
            column
            sm="2"
            style={{ textAlign: "left", fontWeight: "bold" }}
          >
            제목
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="text"
              placeholder="페이지 제목을 입력하세요."
              style={{ height: "45px" }}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </Col>
        </Form.Group>

        {/* Page Type 선택 */}
        <Form.Group as={Row} className="mb-4" controlId="formPageType">
          <Form.Label
            column
            sm="2"
            style={{ textAlign: "left", fontWeight: "bold" }}
          >
            유형
          </Form.Label>
          <Col sm="10">
            <Form.Select
              value={pageType}
              onChange={(e) => setPageType(e.target.value)}
            >
              <option value="URL">URL</option>
              <option value="TEXT">HTML</option>
            </Form.Select>
          </Col>
        </Form.Group>

        {/* URL 입력 */}
        <Form.Group as={Row} className="mb-4" controlId="formBasicUrl">
          <Form.Label
            column
            sm="2"
            style={{ textAlign: "left", fontWeight: "bold" }}
          >
            URL
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="url"
              placeholder="Ex) https://www.cau.ac.kr/index.do"
              style={{ height: "45px" }}
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required={pageType === "URL"}
            />
          </Col>
        </Form.Group>

        {/* HTML 입력 */}
        {pageType === "TEXT" && (
          <Form.Group as={Row} className="mb-4" controlId="formHtmlBody">
            <Form.Label
              column
              sm="2"
              style={{ textAlign: "left", fontWeight: "bold" }}
            >
              HTML
            </Form.Label>
            <Col sm="10">
              <Form.Control
                as="textarea"
                rows={5}
                placeholder="HTML 코드를 입력하세요."
                value={htmlBody}
                onChange={(e) => setHtmlBody(e.target.value)}
              />
            </Col>
          </Form.Group>
        )}

        <Row className="text-center">
          <Col>
            <Button variant="primary" type="submit" disabled={isButtonDisabled}>
              등록
            </Button>
          </Col>
        </Row>
      </Form>

      <div
        className="mt-4 d-flex justify-content-between"
        style={{ width: "70%" }}
      >
        <div style={{ display: "flex", justifyContent: "flex-start" }}>
          <ReportExport />
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <Button
            variant="success"
            onClick={handleAllPageRun}
            style={{
              whiteSpace: "nowrap",
              padding: "0.5rem 1rem",
            }}
          >
            페이지 전체 검사
          </Button>
          <Button
            variant="outline-success"
            onClick={() => setShowScheduleModal(true)}
            className="ms-2"
          >
            검사 예약
          </Button>
        </div>
      </div>

      {/* 검사 예약 모달 창 */}
      <ScheduleModal
        projectId={projectId}
        show={showScheduleModal}
        onHide={() => setShowScheduleModal(false)}
      />
    </Container>
  );
}

export default UrlInput;
