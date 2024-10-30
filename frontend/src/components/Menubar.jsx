import { useEffect, useState } from "react";
import { Container, Navbar } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { CgAddR } from "react-icons/cg";
import axios from "axios";
import CreateProject from "./CreateProject";
import { API } from "../config";

axios.defaults.withCredentials = true;

function Menubar() {
  const [projectCount, setProjectCount] = useState(0);
  const [showCreateProjectModal, setShowCreateProjectModal] = useState(false);

  // 프로젝트 목록을 가져와 카운트를 업데이트하는 함수
  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API.PROJECTLIST}`);
      if (response.status === 200 && Array.isArray(response.data)) {
        setProjectCount(response.data.length);
      }
    } catch (error) {
      console.error("프로젝트 리스트를 가져오는 중 오류 발생:", error);
    }
  };

  useEffect(() => {
    fetchProjects(); // 초기 로드 시 프로젝트 목록 가져오기

    // 주기적으로 프로젝트 수 갱신
    const intervalId = setInterval(fetchProjects, 5000); // 5초마다 호출

    return () => clearInterval(intervalId); // 컴포넌트 언마운트 시 인터벌 해제
  }, []);

  // 팝업창 열기
  const openCreateProjectModal = () => {
    setShowCreateProjectModal(true);
  };

  // 팝업창 닫기
  const closeCreateProjectModal = () => {
    setShowCreateProjectModal(false);
  };

  // 프로젝트가 생성되었을 때 프로젝트 수 갱신
  const handleRefresh = () => {
    fetchProjects(); // 프로젝트 수 업데이트
    closeCreateProjectModal(); // 모달 닫기
  };

  return (
    <>
      <Navbar bg="white" data-bs-theme="light">
        <Container>
          <Navbar.Brand>검사항목({projectCount})</Navbar.Brand>
          <CgAddR size="35" onClick={openCreateProjectModal} cursor="pointer" />
        </Container>
      </Navbar>
      {projectCount === 0 && (
        <Container className="text-center mt-3">
          <span>
            검사 항목이 없습니다.{" "}
            <CgAddR size="20" style={{ verticalAlign: "middle" }} /> 버튼을 눌러
            웹 접근성 검사를 해보세요.
          </span>
        </Container>
      )}
      <CreateProject
        show={showCreateProjectModal}
        onHide={closeCreateProjectModal}
        onSave={handleRefresh} // onSave prop으로 handleRefresh 전달
      />
    </>
  );
}

export default Menubar;
