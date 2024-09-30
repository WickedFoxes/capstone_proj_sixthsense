import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./SignUp.css";

// 유저 데이터(예시)
const existUsers = [{ email: "user1@gmail.com" }, { email: "user2@naver.com" }];

const SignUp = () => {
  const [name, setName] = useState("");
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // 이름, 이메일, 비밀번호, 비밀번호 확인이 모두 입력된 경우 버튼 활성화
    if (name && id && password && confirmPassword) {
      setIsButtonDisabled(false);
    } else {
      setIsButtonDisabled(true);
    }
  }, [name, id, password, confirmPassword]);

  const handleSubmit = (e) => {
    e.preventDefault();

    // 아이디 중복 검사
    const emailExists = existUsers.some((user) => user.email === id);
    if (emailExists) {
      setErrorMessage("이미 가입된 아이디입니다");
      return;
    }

    // 비밀번호 확인
    if (password !== confirmPassword) {
      setErrorMessage("비밀번호가 일치하지 않습니다");
      return;
    }

    // 실제 회원가입 로직 추가 (서버에 데이터 전송)
    console.log("Sign Up successful");
    navigate("/"); // 회원가입 후 이동할 페이지 (나중에 메인 화면 구현)
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
                value={name}
                placeholder="이름"
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div>
              <input
                type="text"
                value={id}
                placeholder="아이디"
                onChange={(e) => setId(e.target.value)}
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
