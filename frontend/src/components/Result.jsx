import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Card, Collapse, Button } from "react-bootstrap";
import axios from "axios";
import { API } from "../config";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vs } from "react-syntax-highlighter/dist/esm/styles/prism";
import "./Result.css";

axios.defaults.withCredentials = true;

function Result() {
  const { projectId, pageId } = useParams();
  const [scanResults, setScanResults] = useState([]);
  const [pageTitle, setPageTitle] = useState(""); // 페이지 제목 상태
  const [openCard, setOpenCard] = useState({});
  const [errors, setErrors] = useState([]); // "ERROR" 타입
  const [warnings, setWarnings] = useState([]); // "WARNING" 타입

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

          // 오류와 경고로 분류
          setErrors(
            response.data.filter((result) => result.erroroption === "ERROR")
          );
          setWarnings(
            response.data.filter((result) => result.erroroption === "WARNING")
          );
        }
      } catch (error) {
        console.error("Error fetching scan results:", error);
      }
    };

    if (pageId) {
      fetchScanResults(); // pageId가 있을 때만 요청
    }
  }, [pageId]);

  // 카드 토글 함수
  const toggleCard = (index) => {
    setOpenCard((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  const renderResults = (results) => {
    // 오름차순 정렬
    const sortedResults = [...results].sort((a, b) => {
      const numA = parseFloat(a.error.match(/^\d+/) || 0);
      const numB = parseFloat(b.error.match(/^\d+/) || 0);
      return numA - numB;
    });

    return sortedResults.map((result, idx) => (
      <div key={idx} className="mb-3 border-bottom pb-2">
        <p>
          <strong>
            [{idx + 1}] {result.error}
          </strong>
        </p>

        <p>
          <strong>오류 메시지:</strong> {result.errormessage}
        </p>
        {result.item.css_selector && (
          <p>
            <strong>오류 위치:</strong>{" "}
            <span style={{ textDecoration: "underline" }}>
              {result.item.css_selector}
            </span>
          </p>
        )}
        {result.item.body && result.item.body !== "null" && (
          <>
            <p>
              <strong>오류 내용:</strong>
            </p>
            <SyntaxHighlighter language="html" style={vs}>
              {result.item.body}
            </SyntaxHighlighter>
          </>
        )}
        {result.item.colorimg && (
          <div className="mt-3">
            <p>
              <strong>이미지:</strong>
            </p>
            <img
              src={`${API.GETIMAGE}${result.item.colorimg}`}
              alt="오류 컬러 이미지"
              style={{ maxWidth: "100%", marginBottom: "10px" }}
            />
          </div>
        )}
      </div>
    ));
  };

  return (
    <Container className="d-flex flex-column align-items-center">
      <h5 className="mb-4 text-center">
        {pageTitle && scanResults.length > 0 ? (
          <>
            <strong>{pageTitle}</strong> 에서 발견된 결과는{" "}
            {errors.length > 0 && warnings.length > 0 ? (
              <>
                <span className="result-count">{errors.length}</span>개의{" "}
                <span className="result-type result-error">오류</span>와{" "}
                <span className="result-count">{warnings.length}</span>개의{" "}
                <span className="result-type result-warning">경고</span>입니다.
              </>
            ) : errors.length > 0 ? (
              <>
                <span className="result-count">{errors.length}</span>개의{" "}
                <span className="result-type result-error">오류</span>입니다.
              </>
            ) : warnings.length > 0 ? (
              <>
                <span className="result-count">{warnings.length}</span>개의{" "}
                <span className="result-type result-warning">경고</span>입니다.
              </>
            ) : null}
            <br />각 항목을 눌러 세부 내용을 확인하세요.
          </>
        ) : (
          <>
            <strong>{pageTitle}</strong> 검사 결과, 오류가 발견되지 않았습니다.
          </>
        )}
      </h5>

      <div style={{ width: "80%", maxWidth: "800px", margin: "5px" }}>
        {/* 오류 카드 */}
        {errors.length > 0 && (
          <Card className="mb-3 shadow-sm">
            <Card.Header className="card-header">
              <span className="card-title">오류 ({errors.length})</span>
              <Button
                variant="outline-primary"
                size="sm"
                onClick={() => toggleCard("errors")}
                aria-controls="collapse-errors"
                aria-expanded={openCard["errors"] || false}
                className="card-button"
              >
                {openCard["errors"] ? "닫기" : "세부 내용 보기"}
              </Button>
            </Card.Header>
            <Collapse in={openCard["errors"]}>
              <Card.Body>{renderResults(errors, "오류")}</Card.Body>
            </Collapse>
          </Card>
        )}

        {/* 경고 카드 */}
        {warnings.length > 0 && (
          <Card className="mb-3 shadow-sm">
            <Card.Header className="card-header">
              <span className="card-title">경고 ({warnings.length})</span>
              <Button
                variant="outline-primary"
                size="sm"
                onClick={() => toggleCard("warnings")}
                aria-controls="collapse-warnings"
                aria-expanded={openCard["warnings"] || false}
                className="card-button"
              >
                {openCard["warnings"] ? "닫기" : "세부 내용 보기"}
              </Button>
            </Card.Header>
            <Collapse in={openCard["warnings"]}>
              <Card.Body>{renderResults(warnings, "경고")}</Card.Body>
            </Collapse>
          </Card>
        )}
      </div>
    </Container>
  );
}

export default Result;
