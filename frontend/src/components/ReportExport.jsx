import { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import axios from "axios";
import PizZip from "pizzip";
import Docxtemplater from "docxtemplater";
import { saveAs } from "file-saver";
import { useParams } from "react-router-dom";
import { API } from "../config";

function ReportExport() {
  const { projectId } = useParams();
  const [projectTitle, setProjectTitle] = useState("");
  const [pages, setPages] = useState([]);
  const [loading, setLoading] = useState(false);

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
        if (!projectId) return;
        const pagesResponse = await axios.get(`${API.PAGELIST}${projectId}`);
        if (pagesResponse.status === 200 && Array.isArray(pagesResponse.data)) {
          const pagesWithResults = await Promise.all(
            pagesResponse.data.map(async (page) => {
              try {
                const scanResponse = await axios.get(
                  `${API.SCANLIST}${page.id}`
                );

                const totalErrors = scanResponse.data.length;

                return {
                  title: page.title || "제목 없음",
                  url: page.url || "url 없음",
                  results: scanResponse.data || [],
                  errorcount: totalErrors, // 전체 오류 개수
                };
              } catch (error) {
                console.error("Error fetching scan results for page:", error);
                return {
                  title: page.title || "제목 없음",
                  url: page.url || "url 없음",
                  results: [],
                  errorcount: 0,
                };
              }
            })
          );
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
          errorcount: page.errorcount,
          pageBreak: '<w:p><w:r><w:br w:type="page"/></w:r></w:p>',
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

      saveAs(output, "웹 접근성 자동 검사 보고서.docx");
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
