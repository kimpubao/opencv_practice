# 🎯 OpenCV + MediaPipe 기반 객체 인식 연습 프로젝트

이 프로젝트는 Python의 OpenCV와 MediaPipe 라이브러리를 활용하여
**얼굴 인식, 손 마디 인식, 몸 자세 인식 등 다양한 시각적 객체 인식**을 연습하기 위한 학습용 레포지토리입니다.

**실시간 웹캠 영상 처리**, **FHD 해상도 지원**, **좌표 시각화/저장** 등 다양한 연습을 통해
LLM / RAG 기반 멀티모달 처리 흐름에서 중요한 **비정형 입력 전처리 기술**을 습득하는 것을 목표로 합니다.

---

## 📑 목차

1. [손 마디 인식 (Hand Landmark Detection)](#손-마디-인식-hand-landmark-detection)
2. [손가락 개수 인식 (Finger Counting)](#손가락-개수-인식-finger-counting)

---

## 📦 사용 환경 및 라이브러리 버전

```text
Python 3.10.x 기준

opencv-python   == 4.11.0.86
mediapipe       == 0.10.5
protobuf        == 3.20.3
numpy           == 1.26.4
```

---

## ✋ 손 마디 인식 (Hand Landmark Detection)

이 실습은 OpenCV와 MediaPipe를 이용하여
**실시간 손 마디(21개 포인트) 인식 및 시각화**를 수행하는 예제입니다.

* MediaPipe의 `Hands` 솔루션을 이용하여 **실시간 손 추적**
* 최대 2개의 손을 추적하며, **각 마디와 연결선 시각화**
* FHD 해상도(`1920x1080`)로 웹캠 프레임 처리

---

## 📽️ 예제 영상

| 예시 영상                                                           |
| --------------------------------------------------------------- |
| ▶️ [hand\_landmark\_video.mp4 (영상 보기)](hand_landmark_video.mp4) |

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

---

## 🧩 주요 특징 및 옵션 설명

| 설정 항목                      | 설명                                           |
| -------------------------- | -------------------------------------------- |
| `max_num_hands=2`          | 최대 2개의 손 인식 (기본값은 1, 3 이상은 정확도 떨어질 수 있음)     |
| `min_detection_confidence` | 손이 존재하는지 판단하는 신뢰도 (0\~1 사이, 일반적으로 0.7 이상 권장) |
| `min_tracking_confidence`  | 추적의 안정성 판단 기준 (0.5 이상이면 충분히 안정적)             |
| `cap.set(CV_CAP_PROP_*)`   | 해상도 설정: HD (1280x720), FHD (1920x1080) 등 가능  |

---

## ✅ 참고 사항

* `protobuf` 오류 해결을 위해 환경 변수 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` 사용
* `cv2.flip`은 영상 좌우 반전(거울 효과) 적용용
* `mp_drawing.draw_landmarks`는 손 마디 및 연결선 자동 시각화

---

## ✌️ 손가락 개수 인식 (Finger Counting)

이 실습은 손 마디 좌표를 기반으로
**펴진 손가락의 개수를 인식하여 실시간으로 숫자 출력**하는 예제입니다.

* MediaPipe가 제공하는 21개 손 관절 중 Tip과 PIP 관절을 비교하여 손가락이 펼쳐졌는지 여부 판단
* 손목 기준으로 화면 하단에 손가락 개수 정보를 **투명한 블럭과 함께 텍스트로 출력**
* 엄지 손가락은 손 방향(왼손/오른손)을 고려하여 좌우 비교
* **손등 방향에서도 안정적으로 작동**하도록 보완됨

```python
# 손가락 개수 인식 주요 로직 요약
if label == 'Right':
    if lm[4].x < lm[3].x:  # 엄지
        count += 1
else:
    if lm[4].x > lm[3].x:
        count += 1

for tip, pip in zip([8,12,16,20], [6,10,14,18]):  # 검~새끼손가락
    if lm[tip].y < lm[pip].y:
        count += 1
```

---

### 🔍 손등 방향 처리가 어려운 이유

손바닥 기준으로 손가락이 접혀 있는지 펼쳐져 있는지 판단할 때는
Tip과 PIP의 y좌표 비교로 대부분 안정적인 결과를 얻을 수 있습니다.
하지만 손등 방향에서는 손가락이 살짝 굽혀져 있어도 Tip과 PIP의 위치관계가 뒤바뀌며 오판이 발생할 수 있습니다.

또한 MediaPipe는 손의 z축 좌표도 제공하지만, 정확한 방향 판별에는 3D 좌표 해석이 필요하며
이는 단순한 2D 비교보다 복잡도가 높고, 손의 회전/기울기/왜곡에 따라 추가 보정이 필요합니다.

따라서 **손등 방향을 완벽히 판별하려면 3D 벡터 비교 또는 시계방향/반시계방향 마디 순서 분석 등의 보완 기법이 요구**됩니다.
본 실습에서는 이러한 복잡성을 피하고, 단순한 좌표 비교로도 충분히 안정적인 결과를 얻을 수 있도록 보정된 로직을 사용합니다.

---

## 📂 사용 코드: `02_finger_count.py`

|📹 예시 영상|
| --------------------------------------------------------------- |
|[finger\_count.mp4 (영상 보기)](finger_count.mp4) |

전체 구현 코드는 해당 `.py` 파일을 참고하세요.
