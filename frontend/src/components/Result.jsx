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
  const [pageUrl, setPageUrl] = useState("");
  const [openCard, setOpenCard] = useState({});

  // 페이지 URL을 가져오기
  useEffect(() => {
    const fetchPageUrlFromList = async () => {
      try {
        const response = await axios.get(`${API.PAGELIST}${projectId}`);
        if (response.status === 200 && Array.isArray(response.data)) {
          const selectedPage = response.data.find(
            (page) => page.id.toString() === pageId
          );
          if (selectedPage) {
            setPageUrl(selectedPage.url); // 페이지 URL 설정
          }
        }
      } catch (error) {
        console.error("Error fetching page URL from list:", error);
      }
    };

    if (projectId && pageId) {
      fetchPageUrlFromList(); // projectId와 pageId가 있을 때만 URL 요청
    }
  }, [projectId, pageId]);

  // 스캔리스트를 가져오기
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
        {pageUrl && scanResults.length > 0 ? (
          <>
            {pageUrl} 에서 발견된 오류는{" "}
            <span style={{ color: "red" }}>{scanResults.length}개</span>입니다.
            <br />각 항목을 눌러 세부 내용을 확인하세요.
          </>
        ) : (
          `${pageUrl} 검사 결과, 오류가 발견되지 않았습니다.`
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
                    // code는 result.item.body 값을 기본적으로 사용, 문자열이 아닐 경우 JSON 문자열로 변환
                    const code =
                      typeof result.item.body === "string"
                        ? result.item.body
                        : JSON.stringify(result.item.body);
                    // 이미지 경로 설정, colorimg 또는 grayimg가 null이 아닌 경우에만 설정됨
                    const colorImgSrc = result.item.colorimg
                      ? `${API.GETIMAGE}${result.item.colorimg}`
                      : null;
                    /* const grayImgSrc = result.item.grayimg
                      ? `${API.GETIMAGE}${result.item.grayimg}`
                      : null; */

                    return (
                      <div key={idx} className="mb-3 border-bottom pb-2">
                        {/* 번호와 오류 메시지 출력 */}
                        <p>
                          <strong>[{idx + 1}] 오류 메시지:</strong>{" "}
                          {result.errormessage}
                        </p>
                        {/* 오류 위치 출력 */}
                        <p>
                          <strong>오류 위치:</strong>{" "}
                          <span style={{ textDecoration: "underline" }}>
                            {result.item.css_selector}
                          </span>
                        </p>
                        {/* 오류 내용 코드 출력 */}
                        <p>
                          <strong>오류 내용:</strong>
                        </p>
                        <SyntaxHighlighter language="html" style={vs}>
                          {code}
                        </SyntaxHighlighter>
                        {/* 컬러 이미지 출력 */}
                        {colorImgSrc && (
                          <div className="mt-3">
                            <p>
                              <strong>이미지:</strong>
                            </p>
                            <img
                              src={colorImgSrc}
                              alt="오류 컬러 이미지"
                              style={{ maxWidth: "100%", marginBottom: "10px" }}
                            />
                          </div>
                        )}
                        {/* 흑백 이미지 출력 : 우선 주석 처리
                        {grayImgSrc && (
                          <div className="mt-3">
                            <p>
                              <strong>흑백 이미지:</strong>
                            </p>
                            <img
                              src={grayImgSrc}
                              alt="오류 흑백 이미지"
                              style={{ maxWidth: "100%" }}
                            />
                          </div>
                        )}*/}
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
