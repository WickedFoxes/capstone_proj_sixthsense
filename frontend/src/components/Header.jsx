import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Container, Nav, Navbar, Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { MdAccountCircle } from "react-icons/md";
import { CgAddR } from "react-icons/cg";
import axios from "axios";

const API_BASE_URL = "http://localhost:8080";
axios.defaults.withCredentials = true;

function Header() {
  const [username, setUsername] = useState("");
  const [projectCount, setProjectCount] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    // 로컬 스토리지에서 사용자 이름 가져오기
    const storedUsername = localStorage.getItem("username");
    if (storedUsername) {
      setUsername(storedUsername);
    }

    // 프로젝트 리스트 가져오기
    const fetchProjects = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/project/list`);
        if (response.status === 200 && Array.isArray(response.data)) {
          setProjectCount(response.data.length);
        }
      } catch (error) {
        console.error("프로젝트 리스트를 가져오는 중 오류 발생:", error);
      }
    };

    fetchProjects();
  }, []);

  const goProjectCreate = () => {
    navigate("/project-create");
  };

  const handleLogout = () => {
    // 로컬 스토리지에서 사용자 정보 제거
    localStorage.removeItem("username");
    // 로그아웃 후 리디렉션 (로그인 페이지 이동)
    window.location.href = "/";
  };

  return (
    <>
      <Navbar
        bg="primary"
        data-bs-theme="dark"
        expand="lg"
        style={{ width: "100%" }}
      >
        <Container fluid>
          <Navbar.Brand href="/main">SixthSense</Navbar.Brand>
          <Nav className="me-auto d-flex align-items-center">
            <MdAccountCircle size="24" color="white" />
            {username && <span className="navbar-text ms-2">{username}님</span>}
          </Nav>
          <div className="d-flex justify-content-end">
            <Button variant="outline-light" size="sm" onClick={handleLogout}>
              로그아웃
            </Button>
          </div>
        </Container>
      </Navbar>
      <br />
      <Navbar bg="white" data-bs-theme="light">
        <Container>
          <Navbar.Brand>검사항목({projectCount})</Navbar.Brand>
          <CgAddR size="35" onClick={goProjectCreate} cursor="pointer" />
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
    </>
  );
}

export default Header;
