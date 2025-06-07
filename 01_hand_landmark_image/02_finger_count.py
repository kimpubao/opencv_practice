# ✅ 환경 변수 설정 (protobuf 충돌 우회용)
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# ✅ 필요한 모듈 불러오기
import cv2
import mediapipe as mp

# ✅ MediaPipe 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# ✅ 손가락 마디 인덱스 정의 (tip과 pip)
finger_tips = [4, 8, 12, 16, 20]  # 엄지, 검지, 중지, 약지, 새끼
finger_pips = [2, 6, 10, 14, 18]  # 각 손가락의 PIP 관절

# ✅ 웹캠 열기 (FHD 해상도)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("카메라에서 프레임을 불러오지 못했습니다.")
            break

        # ✅ 좌우 반전 (셀카 스타일)
        frame = cv2.flip(frame, 1)

        # ✅ BGR → RGB 변환
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, hand_label in zip(result.multi_hand_landmarks, result.multi_handedness):
                # ✅ 좌표 리스트 가져오기
                lm = hand_landmarks.landmark
                label = hand_label.classification[0].label  # 'Left' or 'Right'

                # ✅ 손가락 개수 카운트 시작
                count = 0

                # ✅ 엄지: 손 방향에 따라 좌우 비교 기준이 달라짐
                if label == 'Right':
                    if lm[finger_tips[0]].x < lm[finger_pips[0]].x:
                        count += 1
                else:  # Left hand
                    if lm[finger_tips[0]].x > lm[finger_pips[0]].x:
                        count += 1

                # ✅ 나머지 4개 손가락은 y 좌표로 비교 (tip이 pip보다 위에 있으면 펼침)
                for tip, pip in zip(finger_tips[1:], finger_pips[1:]):
                    if lm[tip].y < lm[pip].y:
                        count += 1

                # ✅ 손 마디 그리기
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                # ✅ 블럭 형태로 텍스트 배경 생성
                h, w, _ = frame.shape
                cx = int(lm[0].x * w)  # 손목 기준 위치
                cy = int(lm[0].y * h) + 80  # 손목보다 약간 아래

                # 배경 박스
                text = f'{count} Fingers'
                font = cv2.FONT_HERSHEY_SIMPLEX
                scale = 1.2
                thickness = 2
                (text_w, text_h), _ = cv2.getTextSize(text, font, scale, thickness)

                box_x1 = cx - text_w // 2 - 10
                box_y1 = cy - text_h - 10
                box_x2 = cx + text_w // 2 + 10
                box_y2 = cy + 10

                cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (48, 48, 48), -1)  # 어두운 회색 배경
                cv2.putText(frame, text, (box_x1 + 10, box_y2 - 10), font, scale, (255, 255, 255), thickness)

        # ✅ 프레임 출력
        cv2.imshow('🖐 Finger Counter (Q: 종료)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# ✅ 종료 처리
cap.release()
cv2.destroyAllWindows()
# ✅ 환경 변수 설정 (protobuf 충돌 우회용)
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# ✅ 필요한 모듈 불러오기
import cv2
import mediapipe as mp

# ✅ MediaPipe 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# ✅ 손가락 마디 인덱스 정의 (tip과 pip)
finger_tips = [4, 8, 12, 16, 20]  # 엄지, 검지, 중지, 약지, 새끼
finger_pips = [2, 6, 10, 14, 18]  # 각 손가락의 PIP 관절

# ✅ 웹캠 열기 (FHD 해상도)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("카메라에서 프레임을 불러오지 못했습니다.")
            break

        # ✅ 좌우 반전 (셀카 스타일)
        frame = cv2.flip(frame, 1)

        # ✅ BGR → RGB 변환
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, hand_label in zip(result.multi_hand_landmarks, result.multi_handedness):
                # ✅ 좌표 리스트 가져오기
                lm = hand_landmarks.landmark
                label = hand_label.classification[0].label  # 'Left' or 'Right'

                # ✅ 손가락 개수 카운트 시작
                count = 0

                # ✅ 엄지: 손 방향에 따라 좌우 비교 기준이 달라짐
                if label == 'Right':
                    if lm[finger_tips[0]].x < lm[finger_pips[0]].x:
                        count += 1
                else:  # Left hand
                    if lm[finger_tips[0]].x > lm[finger_pips[0]].x:
                        count += 1

                # ✅ 나머지 4개 손가락은 y 좌표로 비교 (tip이 pip보다 위에 있으면 펼침)
                for tip, pip in zip(finger_tips[1:], finger_pips[1:]):
                    if lm[tip].y < lm[pip].y:
                        count += 1

                # ✅ 손 마디 그리기
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                # ✅ 블럭 형태로 텍스트 배경 생성
                h, w, _ = frame.shape
                cx = int(lm[0].x * w)  # 손목 기준 위치
                cy = int(lm[0].y * h) + 80  # 손목보다 약간 아래

                # 배경 박스
                text = f'{count} Fingers'
                font = cv2.FONT_HERSHEY_SIMPLEX
                scale = 1.2
                thickness = 2
                (text_w, text_h), _ = cv2.getTextSize(text, font, scale, thickness)

                box_x1 = cx - text_w // 2 - 10
                box_y1 = cy - text_h - 10
                box_x2 = cx + text_w // 2 + 10
                box_y2 = cy + 10

                cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (48, 48, 48), -1)  # 어두운 회색 배경
                cv2.putText(frame, text, (box_x1 + 10, box_y2 - 10), font, scale, (255, 255, 255), thickness)

        # ✅ 프레임 출력
        cv2.imshow('🖐 Finger Counter (Q: 종료)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# ✅ 종료 처리
cap.release()
cv2.destroyAllWindows()
