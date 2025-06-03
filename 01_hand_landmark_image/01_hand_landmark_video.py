# 환경 변수 설정 (protobuf 충돌 우회용)
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# 필요한 모듈 불러오기
import cv2  # OpenCV: 영상 처리 라이브러리
import mediapipe as mp  # MediaPipe: 손 인식 등 경량 딥러닝 모듈

# MediaPipe 모듈 초기화
mp_hands = mp.solutions.hands  # 손 인식 관련 기능
mp_drawing = mp.solutions.drawing_utils  # 손 관절 시각화 도구

# 웹캠 열기 (0번: 기본 내장 웹캠, 외장이라면 1, 2로 변경)
cap = cv2.VideoCapture(0)

# 💡 해상도 설정 (가능한 경우 HD 이상으로 설정됨)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)   # 가로 해상도
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)   # 세로 해상도

# MediaPipe 손 인식 모델 구성 (최대 4개 손 인식 시도)
with mp_hands.Hands(
    max_num_hands=2,                # 동시에 최대 인식할 손 개수(2이면 인식율이 가장 적합, 3 이상이면 누락 높아짐, 성능 떨어짐짐)
    min_detection_confidence=0.7,   # 인식 신뢰도 임계값 (0~1)
    min_tracking_confidence=0.5     # 추적 신뢰도 임계값 (0~1)
) as hands:

    while cap.isOpened():  # 카메라가 정상적으로 켜져 있는 동안 반복
        ret, frame = cap.read()  # 프레임 읽기
        if not ret:
            print("카메라에서 프레임을 불러오지 못했습니다.")
            break

        # 좌우 반전 (셀카처럼 보이도록)
        frame = cv2.flip(frame, 1)

        # OpenCV는 BGR 색상, MediaPipe는 RGB 사용 → 변환
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 손 인식 처리
        result = hands.process(rgb)

        # 손이 인식된 경우 결과 시각화
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                # 손 마디 21개 + 뼈대 연결선을 프레임 위에 그림
                mp_drawing.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

        # 화면에 출력
        cv2.imshow('📸 Hand Tracking (Press Q to quit)', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 웹캠 해제 및 모든 창 닫기
cap.release()
cv2.destroyAllWindows()
