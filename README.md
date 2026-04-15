# test
test

## 이미지 분석 스크립트

`image_analyzer.py`는 OpenCV 기반으로 이미지를 분석해 다음 결과를 생성합니다.

- 해상도/채널/파일 크기
- 평균 밝기, 대비(표준편차), 엣지 밀도
- 윤곽선 기반 객체 개수 추정
- 대표 색상(BGR 평균, HEX)
- 결과 이미지(객체 박스, 엣지맵) 및 JSON 리포트

### 설치

```bash
pip install opencv-python numpy
```

### 실행 예시

```bash
python3 image_analyzer.py "/path/to/image.jpg"
```

결과 파일은 기본적으로 `analysis_output/` 디렉터리에 저장됩니다.
