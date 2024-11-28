import { useEffect, useState } from "react";
import {
  ListGroup,
  Button,
  Dropdown,
  Container,
  Spinner,
} from "react-bootstrap";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function Url() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [urls, setUrls] = useState([]);

  // 특정 프로젝트에 연결된 URL 정보 가져오기 함수 정의
  const fetchUrls = async () => {
    try {
      const response = await axios.get(`${API.PAGELIST}${projectId}`);
      if (response.status === 200 && Array.isArray(response.data)) {
        setUrls(response.data); // URL 리스트를 상태에 저장
      }
    } catch (error) {
      console.error("Error fetching project URLs:", error);
    }
  };

  useEffect(() => {
    if (projectId) {
      fetchUrls(); // projectId가 존재할 때만 URL 데이터 가져오기
      // 2초마다 fetchUrls 호출 : 새고고침 없이 상태 업데이트
      const intervalId = setInterval(fetchUrls, 2000);

      // 컴포넌트 언마운트 시 인터벌 해제
      return () => clearInterval(intervalId);
    }
  }, [projectId]);

  // 검사 버튼 클릭 시 페이지 검사 요청 보내기 (검사 후 즉시 갱신)
  const handleRequestCreate = async (pageId) => {
    try {
      const response = await axios.post(`${API.PAGERUN}${pageId}`);
      if (response.status === 200) {
        alert("페이지 검사가 성공적으로 요청되었습니다!");
        fetchUrls(); // 검사 후 즉시 상태 갱신
      }
    } catch (error) {
      console.error("Error creating request:", error);
      alert("페이지 검사 요청 중 오류가 발생했습니다.");
    }
  };

  // 페이지 삭제 요청 보내기
  const handleDelete = async (pageId) => {
    const confirmDelete = window.confirm(
      "정말로 이 페이지를 삭제하시겠습니까?"
    );
    if (!confirmDelete) return;

    try {
      const response = await axios.request({
        method: "DELETE",
        url: `${API.PAGEDELETE}`,
        data: { id: pageId },
      });

      if (response.status === 202) {
        setUrls((prevUrls) => prevUrls.filter((url) => url.id !== pageId));
        alert("페이지가 성공적으로 삭제되었습니다.");
      }
    } catch (error) {
      console.error("Error deleting page:", error);
      alert("페이지 삭제 중 오류가 발생했습니다.");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center">
      <ListGroup style={{ width: "70%" }}>
        {urls.length > 0 ? (
          urls.map((page, index) => (
            <ListGroup.Item
              key={index}
              as="li"
              className="d-flex justify-content-between align-items-center mb-2"
              style={{ padding: "20px" }}
            >
              <div className="ms-2 text-start d-flex align-items-center">
                {/* 번호 표시 */}
                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    width: "30px",
                    height: "30px",
                    borderRadius: "5%",
                    backgroundColor: "#007bff",
                    color: "white",
                    fontWeight: "bold",
                    marginRight: "10px",
                  }}
                >
                  {index + 1}
                </div>

                {/* 제목과 URL 표시 */}
                <div className="ms-2 d-flex flex-column">
                  <div className="fw-bold">{page.title || "제목 없음"}</div>
                  <a
                    href={page.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      textDecoration: "underline",
                      color: "blue",
                      fontSize: "0.9rem",
                      marginTop: "5px",
                    }}
                  >
                    {page.url}
                  </a>
                </div>

                {/* 상태 표시 */}
                {(page.status === "READY" || page.status === "RUNNING") && (
                  <Spinner
                    animation="border"
                    variant="primary"
                    size="sm"
                    className="ms-3"
                    role="status"
                  ></Spinner>
                )}
              </div>

              <div className="d-flex align-items-center">
                {/* 검사 버튼 */}
                <Button
                  variant={
                    page.status === "COMPLETE" ? "outline-success" : "secondary"
                  }
                  className="me-2"
                  onClick={() => handleRequestCreate(page.id)}
                  disabled={page.status !== "COMPLETE"}
                  style={
                    page.status !== "COMPLETE" ? { cursor: "not-allowed" } : {}
                  }
                >
                  검사
                </Button>

                {/* 보기 버튼 */}
                <Button
                  variant={
                    page.status === "COMPLETE" ? "outline-danger" : "secondary"
                  }
                  className="me-2"
                  onClick={() =>
                    navigate(`/project/${projectId}/page/${page.id}`)
                  }
                  disabled={page.status !== "COMPLETE"}
                  style={
                    page.status !== "COMPLETE" ? { cursor: "not-allowed" } : {}
                  }
                >
                  보기
                </Button>

                {/* 편집 드롭다운 */}
                <Dropdown>
                  <Dropdown.Toggle
                    variant="outline-secondary"
                    id="dropdown-basic"
                    disabled={page.status !== "COMPLETE"}
                    style={
                      page.status !== "COMPLETE"
                        ? { cursor: "not-allowed" }
                        : {}
                    }
                  >
                    편집
                  </Dropdown.Toggle>

                  <Dropdown.Menu>
                    <Dropdown.Item href="#/action-1">수정</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleDelete(page.id)}>
                      삭제
                    </Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
              </div>
            </ListGroup.Item>
          ))
        ) : (
          <h5 className="text-center mt-4">등록된 URL이 없습니다.</h5>
        )}
      </ListGroup>
    </Container>
  );
}

export default Url;
