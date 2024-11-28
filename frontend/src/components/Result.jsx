import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Card, Collapse, Button } from "react-bootstrap";
import axios from "axios";
import { API } from "../config";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vs } from "react-syntax-highlighter/dist/esm/styles/prism";

axios.defaults.withCredentials = true;

function Result() {
  const { projectId, pageId } = useParams();
  const [scanResults, setScanResults] = useState([]);
  const [pageTitle, setPageTitle] = useState(""); // 페이지 제목 상태
  const [openCard, setOpenCard] = useState({});

  // 페이지 제목을 가져오기
  useEffect(() => {
    const fetchPageDetails = async () => {
      try {
        const response = await axios.get(`${API.PAGELIST}${projectId}`);
        if (response.status === 200 && Array.isArray(response.data)) {
          const selectedPage = response.data.find(
            (page) => page.id.toString() === pageId
          );
          if (selectedPage) {
            setPageTitle(selectedPage.title || "제목 없음"); // 페이지 제목 설정
          }
        }
      } catch (error) {
        console.error("Error fetching page details:", error);
      }
    };

    if (projectId && pageId) {
      fetchPageDetails(); // projectId와 pageId가 있을 때만 요청
    }
  }, [projectId, pageId]);

  // 스캔 결과 가져오기
  useEffect(() => {
    const fetchScanResults = async () => {
      try {
        const response = await axios.get(`${API.SCANLIST}${pageId}`);
        if (response.status === 200) {
          setScanResults(response.data); // 스캔 결과 저장
        }
      } catch (error) {
        console.error("Error fetching scan results:", error);
      }
    };

    if (pageId) {
      fetchScanResults(); // pageId가 있을 때만 요청
    }
  }, [pageId]);

  // 오류 유형별로 결과 그룹화
  const groupedErrors = scanResults.reduce((acc, result) => {
    if (!acc[result.error]) {
      acc[result.error] = [];
    }
    acc[result.error].push(result);
    return acc;
  }, {});

  // 카드 토글 함수
  const toggleCard = (index) => {
    setOpenCard((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  return (
    <Container className="d-flex flex-column align-items-center">
      <h5 className="mb-4 text-center">
        {pageTitle && scanResults.length > 0 ? (
          <>
            <strong>{pageTitle}</strong> 에서 발견된 오류는{" "}
            <span style={{ color: "red" }}>{scanResults.length}개</span>
            입니다.
            <br />각 항목을 눌러 세부 내용을 확인하세요.
          </>
        ) : (
          <>
            <strong>{pageTitle}</strong> 검사 결과, 오류가 발견되지 않았습니다.
          </>
        )}
      </h5>

      <div style={{ width: "80%", maxWidth: "800px", margin: "5px" }}>
        {Object.keys(groupedErrors).length > 0 &&
          Object.entries(groupedErrors).map(([error, results], index) => (
            <Card key={index} className="mb-3">
              <Card.Header
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span>
                  {error} ({results.length})
                </span>
                <Button
                  variant="outline-primary"
                  size="sm"
                  onClick={() => toggleCard(index)}
                  aria-controls={`collapse-text-${index}`}
                  aria-expanded={openCard[index] || false}
                  style={{ marginLeft: "10px", width: "auto" }}
                >
                  {openCard[index] ? "닫기" : "세부 내용 보기"}
                </Button>
              </Card.Header>
              <Collapse in={openCard[index]}>
                <Card.Body>
                  {results.map((result, idx) => {
                    const code =
                      typeof result.item.body === "string"
                        ? result.item.body
                        : JSON.stringify(result.item.body);
                    const colorImgSrc = result.item.colorimg
                      ? `${API.GETIMAGE}${result.item.colorimg}`
                      : null;

                    return (
                      <div key={idx} className="mb-3 border-bottom pb-2">
                        <p>
                          <strong>[{idx + 1}] 오류 메시지:</strong>{" "}
                          {result.errormessage}
                        </p>

                        {result.item.css_selector && (
                          <p>
                            <strong>오류 위치:</strong>{" "}
                            <span style={{ textDecoration: "underline" }}>
                              {result.item.css_selector}
                            </span>
                          </p>
                        )}

                        {code && code !== "null" && (
                          <>
                            <p>
                              <strong>오류 내용:</strong>
                            </p>
                            <SyntaxHighlighter language="html" style={vs}>
                              {code}
                            </SyntaxHighlighter>
                          </>
                        )}

                        {colorImgSrc && (
                          <div className="mt-3">
                            <p>
                              <strong>이미지:</strong>
                            </p>
                            <img
                              src={colorImgSrc}
                              alt="오류 컬러 이미지"
                              style={{
                                maxWidth: "100%",
                                marginBottom: "10px",
                              }}
                            />
                          </div>
                        )}
                      </div>
                    );
                  })}
                </Card.Body>
              </Collapse>
            </Card>
          ))}
      </div>
    </Container>
  );
}

export default Result;
