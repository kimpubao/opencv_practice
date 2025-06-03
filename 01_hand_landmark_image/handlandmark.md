# ✋ 손 마디 인식 (Hand Landmark Detection)

이 실습은 OpenCV와 MediaPipe를 이용하여  
**실시간 손 마디(21개 포인트) 인식 및 시각화**를 수행하는 예제입니다.

- MediaPipe의 `Hands` 솔루션을 이용하여 **실시간 손 추적**  
- 최대 2개의 손을 추적하며, **각 마디와 연결선 시각화**
- FHD 해상도(`1920x1080`)로 웹캠 프레임 처리

---

## 📽️ 예제 영상

| 예시 영상 |
|-----------|
| ▶️ [hand_landmark_video.mp4 (영상 보기)](hand_landmark_video.mp4) |

> ℹ️ GitHub에서는 자동 재생되지 않으며, 클릭하면 다운로드 또는 새 탭에서 열립니다.

---

## 💻 사용 코드: `01_hand_landmark_video.py`

```python
# 환경 변수 설정 (protobuf 충돌 우회용)
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# 필요한 모듈 불러오기
import cv2
import mediapipe as mp

# MediaPipe 모듈 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# 웹캠 열기
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

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow('📸 Hand Tracking (Press Q to quit)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
```

# 🧩 주요 특징 및 옵션 설명
| 설정 항목                      | 설명                                           |
| -------------------------- | -------------------------------------------- |
| `max_num_hands=2`          | 최대 2개의 손 인식 (기본값은 1, 3 이상은 정확도 떨어질 수 있음)     |
| `min_detection_confidence` | 손이 존재하는지 판단하는 신뢰도 (0\~1 사이, 일반적으로 0.7 이상 권장) |
| `min_tracking_confidence`  | 추적의 안정성 판단 기준 (0.5 이상이면 충분히 안정적)             |
| `cap.set(CV_CAP_PROP_*)`   | 해상도 설정: HD (1280x720), FHD (1920x1080) 등 가능  |

# ✅ 참고 사항
- `protobuf` 오류 해결을 위해 환경 변수 PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python 사용
- `cv2.flip`은 영상 좌우 반전(거울 효과) 적용용
- `mp_drawing.draw_landmarks`는 손 마디 및 연결선 자동 시각화

# 🔧 사용된 패키지 버전
``` text
opencv-python   == 4.11.0.86  
mediapipe       == 0.10.5  
protobuf        == 3.20.3  
numpy           == 1.26.4  
```