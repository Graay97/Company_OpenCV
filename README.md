# 🎨 실시간 필터 프로그램
> OpenCV와 Dlib을 활용한 실시간 웹캠 필터 애플리케이션

## 📌 주요 기능

### 실시간 필터 효과
- 기본 화면 (0)
- 카툰 효과 (1)
- 빈티지 효과 (2) 
- 머리띠 필터 (3)
- 뷰티 필터 (4)

### 부가 기능
- 📸 스크린샷 저장 (S키)
- 🎥 동영상 녹화 (R키)
- ❌ 프로그램 종료 (Q키)

## 🛠 설치 방법

### 요구사항
- Python 3.7+
- 웹캠

### 패키지 설치
pip install opencv-python opencv-python-headless dlib numpy pillow

### 얼굴 인식 모델 설치
1. [shape_predictor_68_face_landmarks.dat](다운로드_링크) 다운로드
2. 프로젝트 루트 폴더에 파일 배치

## 💻 실행 방법
python main.py

## 📂 프로젝트 구조

<details>
<summary>전체 파일 구조 보기</summary>

```
project-root/
├── main.py                 # 메인 실행 파일
├── filters.py             # 필터 함수 모음
├── key_handler.py        # 키보드 입력 처리
│
├── config/               # 설정 관련 파일들
│   ├── settings.py      # 기본 설정
│   └── constants.py     # 상수 정의
│
├── resources/           # 리소스 파일들
│   ├── screenshots/     # 스크린샷 저장 폴더
│   └── videos/         # 녹화 영상 저장 폴더
│
├── utils/              # 유틸리티 모듈
│   ├── logger/
│   │   ├── __init__.py
│   │   ├── base_logger.py
│   │   ├── main_logger.py
│   │   └── face_logger.py
│   └── face_utils.py   # 얼굴 인식 관련 유틸리티
│
└── logs/              # 로그 파일들
    ├── application_YYYYMMDD.log
    └── face_detection_YYYYMMDD.log
```

</details>

<details>
<summary>주요 파일 설명</summary>

### 핵심 파일
- `main.py`: 프로그램의 진입점
  - 실시간 비디오 스트림 처리
  - 필터 적용 로직
  - 키보드 이벤트 처리

- `filters.py`: 이미지 필터 구현
  - 카툰 효과
  - 빈티지 효과
  - 머리띠 필터
  - 뷰티 필터

- `key_handler.py`: 키보드 입력 처리
  - 필터 전환
  - 스크린샷 저장
  - 녹화 시작/종료

### 설정 파일
- `config/settings.py`: 프로그램 설정
  - 카메라 해상도
  - 저장 경로
  - 필터 파라미터

### 유틸리티
- `utils/logger/`: 로깅 시스템
  - 애플리케이션 로그
  - 얼굴 인식 로그
  - 디버그 정보

</details>

## ⚙️ 성능 최적화
- 프레임 스킵을 통한 얼굴 인식 최적화
- 스레드 풀을 활용한 병렬 처리
- 메모리 사용량 최적화

## ⚠️ 주의사항
1. 프로그램 실행 전 웹캠 연결 상태 확인
2. shape_predictor_68_face_landmarks.dat 파일 경로 확인
3. 충분한 조명 환경에서 실행 권장

## 🔍 문제해결
- 카메라 초기화 실패 시: 웹캠 연결 상태 확인
- 얼굴 인식 실패 시: 조명 상태 확인
- 프레임 드롭 발생 시: 시스템 리소스 확인
