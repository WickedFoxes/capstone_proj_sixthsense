import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Card, Collapse, Button } from "react-bootstrap";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function Result() {
  const { projectId, pageId } = useParams();
  const [scanResults, setScanResults] = useState([]);
  const [pageUrl, setPageUrl] = useState("");
  const [openCard, setOpenCard] = useState({});

  useEffect(() => {
    const fetchPageUrlFromList = async () => {
      try {
        const response = await axios.get(`${API.PAGELIST}${projectId}`);
        if (response.status === 200 && Array.isArray(response.data)) {
          const selectedPage = response.data.find(
            (page) => page.id.toString() === pageId
          );
          if (selectedPage) {
            setPageUrl(selectedPage.url);
          }
        }
      } catch (error) {
        console.error("Error fetching page URL from list:", error);
      }
    };

    if (projectId && pageId) {
      fetchPageUrlFromList();
    }
  }, [projectId, pageId]);

  useEffect(() => {
    const fetchScanResults = async () => {
      try {
        const response = await axios.get(`${API.SCANLIST}${pageId}`);
        if (response.status === 200) {
          setScanResults(response.data);
        }
      } catch (error) {
        console.error("Error fetching scan results:", error);
      }
    };

    if (pageId) {
      fetchScanResults();
    }
  }, [pageId]);

  const groupedErrors = scanResults.reduce((acc, result) => {
    if (!acc[result.error]) {
      acc[result.error] = [];
    }
    acc[result.error].push(result);
    return acc;
  }, {});

  const toggleCard = (index) => {
    setOpenCard((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  return (
    <Container className="d-flex flex-column align-items-center">
      <h5 className="mb-4 text-center">
        {pageUrl && scanResults.length > 0 ? (
          <>
            {pageUrl} 에서 발견된 오류는 {scanResults.length}개입니다.
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
                  {results.map((result, idx) => (
                    <div key={idx} className="mb-3 border-bottom pb-2">
                      <p>
                        <strong>오류 내용:</strong> {result.item.body}
                      </p>
                      <p>
                        <strong>오류 메시지:</strong> {result.errormessage}
                      </p>
                      {result.item.itemtype === "IMAGE" && (
                        <div className="mt-3">
                          <img
                            src={result.item.colorimg || result.item.grayimg}
                            alt="오류 이미지"
                            style={{ maxWidth: "100%" }}
                          />
                        </div>
                      )}
                    </div>
                  ))}
                </Card.Body>
              </Collapse>
            </Card>
          ))}
      </div>
    </Container>
  );
}

export default Result;
