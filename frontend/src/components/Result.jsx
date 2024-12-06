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
  const [pageTitle, setPageTitle] = useState("");
  const [openCard, setOpenCard] = useState({});
  const [errors, setErrors] = useState([]);
  const [warnings, setWarnings] = useState([]);

  useEffect(() => {
    const fetchPageDetails = async () => {
      try {
        const response = await axios.get(`${API.PAGELIST}${projectId}`);
        if (response.status === 200 && Array.isArray(response.data)) {
          const selectedPage = response.data.find(
            (page) => page.id.toString() === pageId
          );
          if (selectedPage) {
            setPageTitle(selectedPage.title || "제목 없음");
          }
        }
      } catch (error) {
        console.error("Error fetching page details:", error);
      }
    };

    if (projectId && pageId) {
      fetchPageDetails();
    }
  }, [projectId, pageId]);

  useEffect(() => {
    const fetchScanResults = async () => {
      try {
        const response = await axios.get(`${API.SCANLIST}${pageId}`);
        if (response.status === 200) {
          setScanResults(response.data);
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
      fetchScanResults();
    }
  }, [pageId]);

  const toggleCard = (index) => {
    setOpenCard((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  const renderResults = (results) => {
    const sortedResults = [...results].sort((a, b) => {
      const numA = parseFloat(a.error.match(/^\d+/) || 0);
      const numB = parseFloat(b.error.match(/^\d+/) || 0);
      return numA - numB;
    });

    return sortedResults.map((result, idx) => {
      const isError = result.erroroption === "ERROR";
      const labelText = isError ? "ERROR" : "WARNING";
      const labelStyle = {
        display: "inline-block",
        backgroundColor: isError ? "#FFCCCC" : "#FFFF99", // 배경색 : 에러면 빨강, 경고면 노랑
        color: "Black",
        border: `1px solid ${isError ? "#990000" : "#CCCC33"}`,
        padding: "5px 10px",
        borderRadius: "5px",
        fontWeight: "bold",
        fontSize: "14px",
        marginRight: "10px",
      };

      return (
        <div key={idx} className="mb-3 border-bottom pb-2">
          <p>
            <strong style={labelStyle}>
              [{idx + 1}] {labelText}
            </strong>
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
      );
    });
  };

  return (
    <Container className="d-flex flex-column align-items-center">
      <h5 className="mb-4 text-center">
        {pageTitle && scanResults.length > 0 ? (
          <>
            <strong>{pageTitle}</strong>
            <br />
            <span style={{ color: "red", fontWeight: "bold" }}>
              오류 {errors.length}
            </span>
            개와 경고 {warnings.length}개가 발견되었습니다.
            <br />각 항목을 눌러 세부 내용을 확인하세요.
          </>
        ) : (
          <>
            <strong>{pageTitle}</strong>
            <br />
            검사 결과, 오류가 발견되지 않았습니다.
          </>
        )}
      </h5>

      <div style={{ width: "80%", maxWidth: "800px", margin: "5px" }}>
        {errors.length > 0 && (
          <Card className="mb-3 shadow-sm">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <span>
                <strong>{errors[0]?.error || "오류"}</strong>{" "}
                <span>(오류 {errors.length}개)</span>
              </span>
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
              <Card.Body>{renderResults(errors)}</Card.Body>
            </Collapse>
          </Card>
        )}

        {warnings.length > 0 && (
          <Card className="mb-3 shadow-sm">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <span>
                <strong>{warnings[0]?.error || "경고"}</strong>{" "}
                <span>(경고 {warnings.length}개)</span>
              </span>
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
              <Card.Body>{renderResults(warnings)}</Card.Body>
            </Collapse>
          </Card>
        )}
      </div>
    </Container>
  );
}

export default Result;
