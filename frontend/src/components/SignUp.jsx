import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./SignUp.css";

// 백엔드 API 주소
const API_BASE_URL = "http://localhost:8080";
axios.defaults.withCredentials = true;

const SignUp = () => {
  const [username, setusername] = useState("");
  const [email, setemail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // 이름, 이메일, 비밀번호, 비밀번호 확인이 모두 입력된 경우 버튼 활성화
    if (username && email && password && confirmPassword) {
      setIsButtonDisabled(false);
    } else {
      setIsButtonDisabled(true);
    }
  }, [username, email, password, confirmPassword]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // 비밀번호 확인
    if (password !== confirmPassword) {
      setErrorMessage("비밀번호가 일치하지 않습니다");
      return;
    }

    try {
      // 백엔드로 회원가입 요청 보내기
      const response = await axios.post(`${API_BASE_URL}/auth/signup`, {
        username,
        email,
        password,
      });

      if (response.status === 201) {
        // 회원가입 성공
        console.log("Sign Up successful");
        navigate("/"); // 회원가입 후 이동할 페이지
      }
    } catch (error) {
      // 회원가입 실패
      if (error.response && error.response.status === 409) {
        setErrorMessage("이미 가입된 아이디입니다");
      }
    }
  };

  return (
    <div className="wrapper">
      <div className="signup-container">
        <div className="signup-form">
          <h2>회원가입</h2>
          <form onSubmit={handleSubmit}>
            <div>
              <input
                type="text"
                value={username}
                placeholder="아이디"
                onChange={(e) => setusername(e.target.value)}
                required
              />
            </div>
            <div>
              <input
                type="text"
                value={email}
                placeholder="이메일"
                onChange={(e) => setemail(e.target.value)}
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
            <div>
              <input
                type="password"
                value={confirmPassword}
                placeholder="비밀번호 확인"
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" disabled={isButtonDisabled}>
              회원가입
            </button>
          </form>
          {errorMessage && <div className="error-message">{errorMessage}</div>}
        </div>
      </div>
    </div>
  );
};

export default SignUp;
