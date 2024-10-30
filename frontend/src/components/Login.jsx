import "./Login.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Button from "react-bootstrap/Button";
import { API } from "../config";

axios.defaults.withCredentials = true;

const Login = () => {
  const [username, setusername] = useState("");
  const [password, setPassword] = useState("");
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const goSignupPage = () => {
    navigate("/signup");
  };

  useEffect(() => {
    if (username && password) {
      setIsButtonDisabled(false);
    } else {
      setIsButtonDisabled(true);
    }
  }, [username, password]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(`${API.LOGIN}`, {
        username,
        password,
      });

      if (response.status === 201) {
        localStorage.setItem("username", username);
        navigate("/main");
      }
    } catch (error) {
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
        <div className="logo-text">Sixthsense</div> {/* 로고 텍스트 추가 */}
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
          {errorMessage && <div className="error-message">{errorMessage}</div>}
          <div className="signup-section">
            <span className="signup-prompt">아직 회원이 아니신가요?</span>
            <Button
              variant="link"
              size="sm"
              onClick={goSignupPage}
              className="signup-link"
            >
              회원가입
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
