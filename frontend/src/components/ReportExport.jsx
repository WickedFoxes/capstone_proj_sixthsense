import { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import axios from "axios";
import PizZip from "pizzip";
import Docxtemplater from "docxtemplater";
import { saveAs } from "file-saver";
import { useParams } from "react-router-dom"; // useParams 추가
import { API } from "../config";

function ReportExport() {
  const { projectId } = useParams(); // URL에서 projectId 가져오기
  const [projectTitle, setProjectTitle] = useState("");
  const [pages, setPages] = useState([]);
  const [loading, setLoading] = useState(false);

  // 프로젝트 제목 가져오기
  useEffect(() => {
    const fetchProjectTitle = async () => {
      try {
        const response = await axios.get(API.PROJECTLIST);
        if (response.status === 200) {
          const project = response.data.find(
            (p) => p.id === parseInt(projectId)
          );
          setProjectTitle(project?.title || "제목 없음");
        }
      } catch (error) {
        console.error("Error fetching project title:", error);
      }
    };

    if (projectId) {
      fetchProjectTitle();
    }
  }, [projectId]);

  useEffect(() => {
    const fetchPagesAndScanResults = async () => {
      try {
        if (!projectId) return; // projectId가 없는 경우 실행하지 않음
        const pagesResponse = await axios.get(`${API.PAGELIST}${projectId}`);
        if (pagesResponse.status === 200 && Array.isArray(pagesResponse.data)) {
          const pagesWithResults = await Promise.all(
            pagesResponse.data.map(async (page) => {
              try {
                const scanResponse = await axios.get(
                  `${API.SCANLIST}${page.id}`
                );
                console.log(
                  "Scan results for page",
                  page.id,
                  scanResponse.data
                );

                // 에러 메시지별로 그룹화
                const groupedErrors = scanResponse.data.reduce(
                  (acc, result) => {
                    if (!acc[result.error]) {
                      acc[result.error] = [];
                    }
                    acc[result.error].push(result);
                    return acc;
                  },
                  {}
                );

                // 고유한 에러 메시지의 수
                const uniqueErrorCount = Object.keys(groupedErrors).length;

                return {
                  title: page.title || "제목 없음",
                  url: page.url || "url 없음",
                  results: scanResponse.data || [],
                  errorcount: uniqueErrorCount, // 고유 에러 개수
                };
              } catch (error) {
                console.error(
                  "Error fetching scan results for page:",
                  page.id,
                  error
                );
                return {
                  title: page.title || "제목 없음",
                  url: page.url || "url 없음",
                  results: [],
                  errorcount: 0, // 에러가 없으면 0
                };
              }
            })
          );
          console.log("Pages with results:", pagesWithResults);
          setPages(pagesWithResults);
        }
      } catch (error) {
        console.error("Error fetching pages or scan results:", error);
      }
    };

    fetchPagesAndScanResults();
  }, [projectId]);

  const generateReport = async () => {
    setLoading(true);

    try {
      const templateResponse = await fetch("/template.docx");
      const arrayBuffer = await templateResponse.arrayBuffer();
      const zip = new PizZip(arrayBuffer);
      const doc = new Docxtemplater(zip, {
        paragraphLoop: true,
        linebreaks: true,
      });

      doc.setData({
        project_title: projectTitle,
        pages: pages.map((page, index) => ({
          index: index + 1,
          title: page.title,
          url: page.url,
          errorcount: page.errorcount, // 에러 개수 추가
          pageBreak: '<w:p><w:r><w:br w:type="page"/></w:r></w:p>', // 페이지 넘기기
          results: page.results.map((result, idx) => ({
            idx: idx + 1,
            error: result.error || "오류 없음",
            errormessage: result.errormessage || "오류 메시지 없음",
            css_selector: result.item?.css_selector || "없음",
            body: result.item?.body || "없음",
          })),
        })),
      });

      doc.render();

      const output = doc.getZip().generate({
        type: "blob",
        mimeType:
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      });

      saveAs(output, "web-accessibility-report.docx");
    } catch (error) {
      console.error("Error generating report:", error);
      alert("보고서 생성 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button variant="primary" onClick={generateReport} disabled={loading}>
      {loading ? "보고서 생성 중..." : "검사 결과 보고서 출력"}
    </Button>
  );
}

export default ReportExport;
