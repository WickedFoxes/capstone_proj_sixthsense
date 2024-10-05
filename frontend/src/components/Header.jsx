import { useEffect, useState } from "react";
import { Container, Nav, Navbar, Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { MdAccountCircle } from "react-icons/md";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function Header() {
  const [username, setUsername] = useState("");

  useEffect(() => {
    // 로컬 스토리지에서 사용자 이름 가져오기
    const storedUsername = localStorage.getItem("username");
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);

  const handleLogout = async () => {
    try {
      // 백엔드의 로그아웃 엔드포인트 호출
      const response = await axios.post(`${API.LOGOUT}`);
      if (response.status === 200) {
        // 성공적으로 로그아웃되면 로컬 스토리지에서 사용자 정보 제거
        localStorage.removeItem("username");
        // 로그인 페이지로 리디렉션
        window.location.href = "/";
      }
    } catch (error) {
      console.error("로그아웃 실패:", error);
    }
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
    </>
  );
}

export default Header;
