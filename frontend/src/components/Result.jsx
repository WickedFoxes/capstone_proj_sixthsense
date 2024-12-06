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
          if (selectedPage) setPageTitle(selectedPage.title || "제목 없음");
        }
      } catch (error) {
        console.error("Error fetching page details:", error);
      }
    };

    if (projectId && pageId) fetchPageDetails();
  }, [projectId, pageId]);

  useEffect(() => {
    const fetchScanResults = async () => {
      try {
        const response = await axios.get(`${API.SCANLIST}${pageId}`);
        if (response.status === 200) {
          const results = response.data;
          setScanResults(results);
          setErrors(results.filter((result) => result.erroroption === "ERROR"));
          setWarnings(
            results.filter((result) => result.erroroption === "WARNING")
          );
        }
      } catch (error) {
        console.error("Error fetching scan results:", error);
      }
    };

    if (pageId) fetchScanResults();
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
      const labelStyle = {
        display: "inline-block",
        backgroundColor: isError ? "#FFCCCC" : "#FFFF99",
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
              [{idx + 1}] {isError ? "ERROR" : "WARNING"}
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

  const renderSummary = () => (
    <>
      {errors.length > 0 && warnings.length > 0 ? (
        <>
          <span style={{ color: "red", fontWeight: "bold" }}>
            오류 {errors.length}개
          </span>
          와 경고 {warnings.length}개가 발견되었습니다.
        </>
      ) : errors.length > 0 ? (
        <>
          <span style={{ color: "red", fontWeight: "bold" }}>
            오류 {errors.length}개
          </span>
          가 발견되었습니다.
        </>
      ) : warnings.length > 0 ? (
        <>
          <span style={{ color: "red", fontWeight: "bold" }}>
            경고 {warnings.length}개
          </span>
          가 발견되었습니다.
        </>
      ) : (
        "발견된 오류나 경고가 없습니다."
      )}
      <br />각 항목을 눌러 세부 내용을 확인하세요.
    </>
  );

  return (
    <Container className="d-flex flex-column align-items-center">
      <h5 className="mb-4 text-center">
        {pageTitle && scanResults.length > 0 ? (
          <>
            <strong>{pageTitle}</strong>
            <br />
            {renderSummary()}
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
        {Object.entries(
          scanResults
            .sort((a, b) => {
              const numA = parseInt(a.error.match(/^\d+/)) || 0;
              const numB = parseInt(b.error.match(/^\d+/)) || 0;
              return numA - numB;
            })
            .reduce((grouped, result) => {
              if (!grouped[result.error]) grouped[result.error] = [];
              grouped[result.error].push(result);
              return grouped;
            }, {})
        ).map(([errorTitle, errorDetails], index) => (
          <Card key={index} className="mb-3 shadow-sm">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <span>
                <strong>{errorTitle}</strong>{" "}
                <span>
                  ({errorDetails[0].erroroption === "ERROR" ? "오류" : "경고"}{" "}
                  {errorDetails.length}개)
                </span>
              </span>
              <Button
                variant="outline-primary"
                size="sm"
                onClick={() => toggleCard(index)}
                aria-controls={`collapse-${index}`}
                aria-expanded={openCard[index] || false}
                className="card-button"
              >
                {openCard[index] ? "닫기" : "세부 내용 보기"}
              </Button>
            </Card.Header>
            <Collapse in={openCard[index]}>
              <Card.Body>{renderResults(errorDetails)}</Card.Body>
            </Collapse>
          </Card>
        ))}
      </div>
    </Container>
  );
}

export default Result;
