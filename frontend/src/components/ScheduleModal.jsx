import { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import PropTypes from "prop-types";
import axios from "axios";
import { API } from "../config";

axios.defaults.withCredentials = true;

function ScheduleModal({ projectId, show, onHide }) {
  const [scheduleTitle, setScheduleTitle] = useState(""); // 검사 예약 제목
  const [scheduleDescription, setScheduleDescription] = useState(""); // 검사 예약 내용
  const [scheduleDate, setScheduleDate] = useState(""); // 검사 예약 날짜/시간

  // 검사 예약 요청
  const handleSchedule = async () => {
    if (!scheduleTitle || !scheduleDate) {
      alert("제목과 날짜를 입력해주세요.");
      return;
    }

    const requestData = {
      title: scheduleTitle,
      description: scheduleDescription || scheduleTitle,
      date: scheduleDate,
    };

    try {
      const response = await axios.post(
        `${API.MAKESCHEDULE}${projectId}`,
        requestData
      );
      if (response.status === 201) {
        alert("검사가 성공적으로 예약되었습니다!");
        onHide(); // 모달 닫기
        resetScheduleFields(); // 입력 필드 초기화
      }
    } catch (error) {
      console.error("Error scheduling test:", error);
      alert("검사 예약 중 오류가 발생했습니다.");
    }
  };

  const resetScheduleFields = () => {
    setScheduleTitle("");
    setScheduleDescription("");
    setScheduleDate("");
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>검사 예약</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="formScheduleTitle" className="mb-3">
            <Form.Label>예약 제목</Form.Label>
            <Form.Control
              type="text"
              placeholder="검사 예약 제목을 입력하세요. ex) 2024 하반기 검사"
              value={scheduleTitle}
              onChange={(e) => setScheduleTitle(e.target.value)}
            />
          </Form.Group>

          <Form.Group controlId="formScheduleDescription" className="mb-3">
            <Form.Label>예약 내용</Form.Label>
            <Form.Control
              type="text"
              placeholder="검사 예약 설명을 입력하세요. (선택 사항)"
              value={scheduleDescription}
              onChange={(e) => setScheduleDescription(e.target.value)}
            />
          </Form.Group>

          <Form.Group controlId="formScheduleDate" className="mb-3">
            <Form.Label>예약 날짜 및 시간</Form.Label>
            <input
              type="datetime-local"
              className="custom-datetime-input"
              value={scheduleDate}
              onChange={(e) => setScheduleDate(e.target.value)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          취소
        </Button>
        <Button
          variant="primary"
          onClick={handleSchedule}
          disabled={!scheduleTitle || !scheduleDate}
        >
          저장
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

ScheduleModal.propTypes = {
  projectId: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
};

export default ScheduleModal;
