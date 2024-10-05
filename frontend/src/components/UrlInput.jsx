import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Button, Form, Row, Col, Container } from "react-bootstrap";
import axios from "axios";
import { API } from "../config"; // API 설정 파일에서 불러오기

axios.defaults.withCredentials = true;

function UrlInput() {
  const { projectId } = useParams(); // URL에서 projectId 추출
  const [projects, setProjects] = useState([]); // 모든 프로젝트 목록을 저장
  const [projectTitle, setProjectTitle] = useState(""); // 현재 선택된 프로젝트의 타이틀 상태
  const [name, setName] = useState(""); // 이름 상태
  const [url, setUrl] = useState(""); // URL 상태

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
      // projectId와 일치하는 프로젝트를 찾음
      const selectedProject = projects.find(
        (project) => project.id.toString() === projectId
      );
      if (selectedProject) {
        setProjectTitle(selectedProject.title);
      }
    }
  }, [projects, projectId]);

  // 등록 버튼 클릭 시 페이지 생성 요청
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(
        `${API.PAGECREATE}${projectId}`, // 프로젝트 ID를 동적으로 추가하여 URL 생성
        {
          name: name, // 입력한 페이지 이름
          url: url, // 입력한 URL
        }
      );

      if (response.status === 201) {
        alert("페이지가 성공적으로 생성되었습니다!");
      }
    } catch (error) {
      console.error("Error creating page:", error);
      alert("페이지 생성 중 오류가 발생했습니다.");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center">
      <Form style={{ width: "70%" }} onSubmit={handleSubmit}>
        {projectTitle ? (
          <h4 className="mb-4 text-center">
            {projectTitle} 에서 검사할 URL을 등록하세요.
          </h4>
        ) : (
          <h4 className="mb-4 text-center">프로젝트 정보를 불러오는 중...</h4>
        )}

        <Form.Group as={Row} className="mb-4" controlId="formBasicName">
          <Form.Label
            column
            sm="2"
            style={{ textAlign: "left", fontWeight: "bold" }}
          >
            이름
          </Form.Label>
          <Col sm="10">
            <Form.Control
              type="text"
              placeholder="Ex) 수강신청, 로그인, 메인 화면 ..."
              style={{ height: "45px" }}
              value={name}
              onChange={(e) => setName(e.target.value)} // 입력 값 상태 업데이트
              required
            />
          </Col>
        </Form.Group>
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
              onChange={(e) => setUrl(e.target.value)} // 입력 값 상태 업데이트
              required
            />
          </Col>
        </Form.Group>
        <Row className="text-center">
          <Col>
            <Button variant="primary" type="submit">
              등록
            </Button>
          </Col>
        </Row>
      </Form>
    </Container>
  );
}

export default UrlInput;
