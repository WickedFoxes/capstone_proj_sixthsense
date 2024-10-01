import "./Login.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

// 백엔드 API 주소
const API_BASE_URL = "http://localhost:8080";
axios.defaults.withCredentials = true;

const Login = () => {
  const [username, setusername] = useState("");
  const [password, setPassword] = useState("");
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  // 회원가입 페이지 이동
  const goSignupPage = () => {
    navigate("/signup");
  };

  useEffect(() => {
    //아이디와 비밀번호가 모두 입력된 경우 버튼을 활성화
    if (username && password) {
      setIsButtonDisabled(false);
    } else {
      setIsButtonDisabled(true);
    }
  }, [username, password]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // 백엔드로 로그인 요청 보내기
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        username,
        password,
      });

      if (response.status === 201) {
        // 로그인 성공
        console.log("Login successful");
        navigate("/main"); // 로그인 후 이동할 페이지
      }
    } catch (error) {
      // 로그인 실패
      if (error.response && error.response.status === 401) {
        setErrorMessage("아이디 또는 비밀번호가 일치하지 않습니다.");
      } else {
        setErrorMessage(
          "서버 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
        );
      }
    }
  };

  return (
    <div className="wrapper">
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <input
              type="text"
              value={username}
              placeholder="아이디(Username)"
              onChange={(e) => setusername(e.target.value)}
              required
            />
          </div>

          <div>
            <input
              type="password"
              value={password}
              placeholder="비밀번호"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" disabled={isButtonDisabled}>
            로그인
          </button>
          <h5 className="signup-link" onClick={goSignupPage}>
            회원가입
          </h5>
        </form>
        {errorMessage && <div className="error-message">{errorMessage}</div>}
      </div>
    </div>
  );
};

export default Login;
