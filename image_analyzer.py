#!/usr/bin/env python3
"""기본 이미지 분석 스크립트.

기능:
1) 이미지 메타 정보(해상도, 채널, 파일 크기)
2) 밝기/대비/엣지 밀도 계산
3) 윤곽선 기반 객체 개수 추정
4) 대표 색상(평균 BGR/HEX) 계산
5) 분석 시각화 이미지와 JSON 리포트 저장
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OpenCV 기반 이미지 분석 스크립트",
    )
    parser.add_argument("image_path", type=Path, help="분석할 이미지 파일 경로")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("analysis_output"),
        help="분석 결과를 저장할 디렉터리 (기본값: analysis_output)",
    )
    parser.add_argument(
        "--min-contour-area",
        type=float,
        default=1200.0,
        help="객체로 간주할 최소 윤곽선 면적 (기본값: 1200)",
    )
    return parser


def bgr_to_hex(color_bgr: tuple[int, int, int]) -> str:
    b, g, r = color_bgr
    return f"#{r:02X}{g:02X}{b:02X}"


def analyze_image(image_path: Path, output_dir: Path, min_contour_area: float) -> dict:
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise SystemExit(
            "필수 패키지 설치가 필요합니다. 다음 명령어를 실행하세요:\n"
            "pip install opencv-python numpy"
        ) from exc

    if not image_path.exists():
        raise SystemExit(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        raise SystemExit(f"이미지를 읽을 수 없습니다: {image_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    height, width = image.shape[:2]
    channels = image.shape[2] if len(image.shape) == 3 else 1
    file_size_bytes = image_path.stat().st_size

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 80, 180)

    _, thresh = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= min_contour_area]
    annotated = image.copy()
    total_contour_area = 0.0

    for idx, contour in enumerate(valid_contours, start=1):
        x, y, w, h = cv2.boundingRect(contour)
        area = float(cv2.contourArea(contour))
        total_contour_area += area
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            annotated,
            f"obj-{idx}",
            (x, max(25, y - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    # 평균 색상(대표 색상) 계산
    mean_bgr_float = image.reshape(-1, 3).mean(axis=0)
    mean_bgr = tuple(int(round(v)) for v in mean_bgr_float.tolist())
    mean_hex = bgr_to_hex(mean_bgr)

    brightness = float(gray.mean())
    contrast = float(gray.std())
    edge_density = float((edges > 0).sum() / edges.size)
    object_coverage_ratio = float(total_contour_area / (width * height))

    # 4분할 영역별 평균 밝기(간단한 공간 정보)
    mid_h, mid_w = height // 2, width // 2
    quadrants = {
        "top_left": gray[:mid_h, :mid_w],
        "top_right": gray[:mid_h, mid_w:],
        "bottom_left": gray[mid_h:, :mid_w],
        "bottom_right": gray[mid_h:, mid_w:],
    }
    quadrant_brightness = {name: float(region.mean()) for name, region in quadrants.items()}

    base_name = image_path.stem
    annotated_path = output_dir / f"{base_name}_annotated.jpg"
    edge_path = output_dir / f"{base_name}_edges.jpg"
    report_path = output_dir / f"{base_name}_report.json"

    cv2.imwrite(str(annotated_path), annotated)
    cv2.imwrite(str(edge_path), edges)

    report = {
        "input": {
            "image_path": str(image_path),
            "file_size_bytes": file_size_bytes,
            "width": width,
            "height": height,
            "channels": channels,
        },
        "statistics": {
            "brightness_mean": brightness,
            "contrast_stddev": contrast,
            "edge_density": edge_density,
            "estimated_object_count": len(valid_contours),
            "object_coverage_ratio": object_coverage_ratio,
        },
        "color": {
            "dominant_color_bgr_mean": {
                "b": mean_bgr[0],
                "g": mean_bgr[1],
                "r": mean_bgr[2],
            },
            "dominant_color_hex": mean_hex,
        },
        "quadrant_brightness": quadrant_brightness,
        "outputs": {
            "annotated_image": str(annotated_path),
            "edge_image": str(edge_path),
            "report_json": str(report_path),
        },
    }

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return report


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    report = analyze_image(args.image_path, args.output_dir, args.min_contour_area)

    print("분석 완료")
    print(f"- 입력 이미지: {report['input']['image_path']}")
    print(f"- 해상도: {report['input']['width']}x{report['input']['height']}")
    print(f"- 객체 추정 개수: {report['statistics']['estimated_object_count']}")
    print(f"- 대표 색상(HEX): {report['color']['dominant_color_hex']}")
    print(f"- 리포트 파일: {report['outputs']['report_json']}")


if __name__ == "__main__":
    main()
