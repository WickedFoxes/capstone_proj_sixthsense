import { useEffect, useState } from "react";
import {
  ListGroup,
  Button,
  Dropdown,
  Container,
  Spinner,
} from "react-bootstrap";
import { useParams } from "react-router-dom";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function Url() {
  const { projectId } = useParams(); // URL에서 projectId 추출
  const [urls, setUrls] = useState([]); // URL 리스트 상태

  useEffect(() => {
    // 특정 프로젝트에 연결된 URL 정보 가져오기
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

    if (projectId) {
      fetchUrls(); // projectId가 존재할 때만 URL 데이터 가져오기
    }
  }, [projectId]);

  // 검사 버튼 클릭 시 페이지 검사 요청 보내기
  const handleRequestCreate = async (id) => {
    try {
      const response = await axios.post(`${API.REQUESTCREATE}${id}`);
      if (response.status === 201) {
        alert("페이지 검사가 성공적으로 요청되었습니다!");
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
    if (!confirmDelete) return; // 사용자가 삭제를 취소하면 함수 종료

    try {
      const response = await axios.request({
        method: "DELETE",
        url: `${API.PAGEDELETE}`, // URL은 /page/delete 엔드포인트
        data: { id: pageId }, // 요청 본문에 id를 포함하여 전송
      });

      if (response.status === 202) {
        // 삭제 성공 시 해당 항목을 상태에서 제거
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
              {/* 페이지 상태 및 정보 표시 */}
              <div className="ms-2 text-start d-flex align-items-center">
                <div className="fw-bold">{index + 1}.</div>
                <div className="ms-2">{page.url}</div>
                {/* 상태가 READY 또는 RUNNING일 때 스피너 표시 */}
                {(page.status === "READY" || page.status === "RUNNING") && (
                  <Spinner
                    animation="border"
                    variant="primary"
                    size="sm"
                    className="ms-3"
                    role="status"
                  >
                    <span className="visually-hidden">검사 중...</span>
                  </Spinner>
                )}
              </div>

              {/* 버튼 및 드롭다운 메뉴 */}
              <div className="d-flex align-items-center">
                {/* 검사 버튼: COMPLETE 상태일 때만 활성화 */}
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

                {/* 보기 버튼: COMPLETE 상태일 때만 활성화 */}
                <Button
                  variant={
                    page.status === "COMPLETE" ? "outline-danger" : "secondary"
                  }
                  className="me-2"
                  onClick={() => window.open(page.url, "_blank")}
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
