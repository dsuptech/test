"""
지역별 날씨 정보를 가져오는 모듈
OpenWeatherMap API를 사용합니다.

사용법:
    1. https://openweathermap.org/api 에서 무료 API 키를 발급받으세요.
    2. API_KEY 환경변수를 설정하거나 직접 입력하세요.
    3. python weather.py 실행
"""

import os
import sys
import requests
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


SCRIPT_DIR = Path(__file__).parent
SUNNY_IMAGE_PATH = SCRIPT_DIR / "images" / "sunny_puppy.jpg"

SUNNY_KEYWORDS = ["맑음", "clear", "sunny", "청명"]


def is_sunny(description: str) -> bool:
    """날씨 설명이 맑음인지 확인"""
    description_lower = description.lower()
    return any(keyword in description_lower for keyword in SUNNY_KEYWORDS)


def display_image(image_path: Path) -> None:
    """이미지를 화면에 표시합니다."""
    if not image_path.exists():
        print(f"⚠️  이미지 파일을 찾을 수 없습니다: {image_path}")
        return
    
    if not HAS_PIL:
        print(f"🖼️  맑은 날씨 이미지: {image_path}")
        print("   (이미지를 직접 보려면 'pip install Pillow'를 설치하세요)")
        return
    
    try:
        img = Image.open(image_path)
        print(f"\n🖼️  맑은 날씨입니다! 이미지를 표시합니다...")
        print(f"   이미지 경로: {image_path}")
        print(f"   이미지 크기: {img.size[0]}x{img.size[1]}")
        
        if sys.platform == "darwin":
            os.system(f"open '{image_path}'")
        elif sys.platform == "win32":
            os.startfile(str(image_path))
        elif sys.platform.startswith("linux"):
            if os.environ.get("DISPLAY"):
                os.system(f"xdg-open '{image_path}' 2>/dev/null &")
            else:
                print_image_ascii(img)
    except Exception as e:
        print(f"⚠️  이미지 표시 오류: {e}")


def print_image_ascii(img: "Image.Image", width: int = 60) -> None:
    """이미지를 ASCII 아트로 터미널에 출력"""
    ascii_chars = " .:-=+*#%@"
    
    aspect_ratio = img.height / img.width
    new_height = int(width * aspect_ratio * 0.5)
    img_resized = img.resize((width, new_height))
    img_gray = img_resized.convert("L")
    
    print("\n" + "=" * width)
    for y in range(new_height):
        line = ""
        for x in range(width):
            pixel = img_gray.getpixel((x, y))
            char_idx = int(pixel / 256 * len(ascii_chars))
            char_idx = min(char_idx, len(ascii_chars) - 1)
            line += ascii_chars[char_idx]
        print(line)
    print("=" * width + "\n")


@dataclass
class WeatherInfo:
    """날씨 정보를 담는 데이터 클래스"""
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float
    
    def __str__(self) -> str:
        return f"""
┌─────────────────────────────────────────┐
│ 📍 {self.city}, {self.country}
├─────────────────────────────────────────┤
│ 🌡️  온도: {self.temperature:.1f}°C (체감: {self.feels_like:.1f}°C)
│ 💧 습도: {self.humidity}%
│ 🌤️  상태: {self.description}
│ 💨 풍속: {self.wind_speed} m/s
└─────────────────────────────────────────┘
"""
    
    def is_sunny(self) -> bool:
        """날씨가 맑음인지 확인"""
        return is_sunny(self.description)
    
    def display_with_image(self) -> None:
        """날씨 정보를 출력하고, 맑음이면 이미지도 표시"""
        print(self)
        if self.is_sunny():
            display_image(SUNNY_IMAGE_PATH)


class WeatherAPI:
    """OpenWeatherMap API를 사용한 날씨 조회 클래스"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API 키가 필요합니다. "
                "OPENWEATHERMAP_API_KEY 환경변수를 설정하거나 "
                "api_key 파라미터로 전달해주세요."
            )
    
    def get_weather_by_city(self, city: str, lang: str = "kr") -> WeatherInfo:
        """도시 이름으로 날씨 정보를 가져옵니다."""
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": lang
        }
        return self._fetch_weather(params)
    
    def get_weather_by_coords(
        self, lat: float, lon: float, lang: str = "kr"
    ) -> WeatherInfo:
        """위도/경도로 날씨 정보를 가져옵니다."""
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": lang
        }
        return self._fetch_weather(params)
    
    def _fetch_weather(self, params: dict) -> WeatherInfo:
        """API 호출 및 응답 파싱"""
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return WeatherInfo(
                city=data["name"],
                country=data["sys"]["country"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                humidity=data["main"]["humidity"],
                description=data["weather"][0]["description"],
                wind_speed=data["wind"]["speed"]
            )
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"도시를 찾을 수 없습니다: {params.get('q', 'unknown')}")
            elif response.status_code == 401:
                raise ValueError("유효하지 않은 API 키입니다.")
            raise ValueError(f"API 오류: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"네트워크 오류: {e}")


# 주요 한국 도시 좌표
KOREAN_CITIES = {
    "서울": {"lat": 37.5665, "lon": 126.9780},
    "부산": {"lat": 35.1796, "lon": 129.0756},
    "인천": {"lat": 37.4563, "lon": 126.7052},
    "대구": {"lat": 35.8714, "lon": 128.6014},
    "대전": {"lat": 36.3504, "lon": 127.3845},
    "광주": {"lat": 35.1595, "lon": 126.8526},
    "울산": {"lat": 35.5384, "lon": 129.3114},
    "세종": {"lat": 36.4800, "lon": 127.2890},
    "제주": {"lat": 33.4996, "lon": 126.5312},
    "수원": {"lat": 37.2636, "lon": 127.0286},
}


def get_korean_city_weather(api: WeatherAPI, city_name: str) -> WeatherInfo:
    """한국 도시 이름(한글)으로 날씨 조회"""
    if city_name in KOREAN_CITIES:
        coords = KOREAN_CITIES[city_name]
        return api.get_weather_by_coords(coords["lat"], coords["lon"])
    return api.get_weather_by_city(city_name)


def get_multiple_cities_weather(
    api: WeatherAPI, cities: list[str]
) -> dict[str, WeatherInfo]:
    """여러 도시의 날씨를 한번에 조회"""
    results = {}
    for city in cities:
        try:
            results[city] = get_korean_city_weather(api, city)
        except (ValueError, ConnectionError) as e:
            print(f"⚠️  {city} 조회 실패: {e}")
    return results


def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("🌤️  지역별 날씨 조회 프로그램")
    print("=" * 50)
    
    try:
        api = WeatherAPI()
    except ValueError as e:
        print(f"\n❌ 오류: {e}")
        print("\n💡 API 키 설정 방법:")
        print("   export OPENWEATHERMAP_API_KEY='your-api-key'")
        print("\n   또는 https://openweathermap.org/api 에서 무료 키를 발급받으세요.")
        return
    
    # 예시: 여러 도시 날씨 조회
    cities = ["서울", "부산", "제주", "대전"]
    print(f"\n📊 조회 도시: {', '.join(cities)}\n")
    
    weather_data = get_multiple_cities_weather(api, cities)
    
    for city, weather in weather_data.items():
        weather.display_with_image()
    
    # 특정 도시 조회 예시
    print("\n" + "=" * 50)
    print("🔍 특정 도시 검색 예시")
    print("=" * 50)
    
    try:
        tokyo_weather = api.get_weather_by_city("Tokyo")
        tokyo_weather.display_with_image()
    except (ValueError, ConnectionError) as e:
        print(f"⚠️  도쿄 조회 실패: {e}")


if __name__ == "__main__":
    main()
