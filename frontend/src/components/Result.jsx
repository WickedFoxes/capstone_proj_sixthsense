import { useEffect, useState } from "react";
import Accordion from "react-bootstrap/Accordion";
import { useParams } from "react-router-dom";
import { Container } from "react-bootstrap";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function Result() {
  const { projectId, pageId } = useParams(); // URL에서 projectId, pageId 추출
  const [scanResults, setScanResults] = useState([]);
  const [pageUrl, setPageUrl] = useState(""); // 페이지 URL 상태 추가

  // 페이지 리스트 가져오기 및 해당 페이지 URL 설정
  useEffect(() => {
    const fetchPageUrlFromList = async () => {
      try {
        const response = await axios.get(`${API.PAGELIST}${projectId}`);
        if (response.status === 200 && Array.isArray(response.data)) {
          const selectedPage = response.data.find(
            (page) => page.id.toString() === pageId
          );
          if (selectedPage) {
            setPageUrl(selectedPage.url); // 해당 pageId에 맞는 URL 설정
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

  // 검사 결과 가져오기
  useEffect(() => {
    const fetchScanResults = async () => {
      try {
        const response = await axios.get(`${API.SCANLIST}${pageId}`);
        if (response.status === 200) {
          setScanResults(response.data); // 가져온 검사 결과 저장
        }
      } catch (error) {
        console.error("Error fetching scan results:", error);
      }
    };

    if (pageId) {
      fetchScanResults();
    }
  }, [pageId]);

  return (
    <Container className="d-flex flex-column align-items-center">
      {/* 오류 개수 및 페이지 URL 표시 */}
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
        {scanResults.length > 0 ? (
          <Accordion>
            {scanResults.map((result, index) => (
              <Accordion.Item eventKey={index.toString()} key={result.id}>
                <Accordion.Header>{result.error}</Accordion.Header>
                <Accordion.Body>
                  <p>
                    <strong>오류 메시지:</strong> {result.errormessage}
                  </p>
                  <p>
                    <strong>오류 내용:</strong> {result.item.body}
                  </p>

                  {/* 이미지 오류일 경우 이미지 출력 */}
                  {result.item.itemtype === "IMAGE" && (
                    <div className="mt-3">
                      <img
                        src={result.item.colorimg || result.item.grayimg}
                        alt="오류 이미지"
                        style={{ maxWidth: "100%" }}
                      />
                    </div>
                  )}
                </Accordion.Body>
              </Accordion.Item>
            ))}
          </Accordion>
        ) : null}
      </div>
    </Container>
  );
}

export default Result;
