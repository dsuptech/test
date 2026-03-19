"""
weather.py 모듈의 단위 테스트
pytest를 사용하여 실행: pytest test_weather.py -v
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import requests

from weather import (
    is_sunny,
    display_image,
    WeatherInfo,
    WeatherAPI,
    KOREAN_CITIES,
    get_korean_city_weather,
    get_multiple_cities_weather,
    SUNNY_KEYWORDS,
)


class TestIsSunny:
    """is_sunny 함수 테스트"""

    @pytest.mark.parametrize("description,expected", [
        ("맑음", True),
        ("clear sky", True),
        ("sunny", True),
        ("청명", True),
        ("Clear Sky", True),
        ("SUNNY day", True),
        ("partly clear", True),
    ])
    def test_sunny_descriptions_return_true(self, description, expected):
        """맑음 관련 키워드가 포함되면 True 반환"""
        assert is_sunny(description) == expected

    @pytest.mark.parametrize("description,expected", [
        ("흐림", False),
        ("비", False),
        ("cloudy", False),
        ("rainy", False),
        ("snow", False),
        ("fog", False),
        ("thunderstorm", False),
    ])
    def test_non_sunny_descriptions_return_false(self, description, expected):
        """맑음이 아닌 날씨는 False 반환"""
        assert is_sunny(description) == expected

    def test_empty_string_returns_false(self):
        """빈 문자열은 False 반환"""
        assert is_sunny("") is False

    def test_case_insensitive(self):
        """대소문자 구분 없이 동작"""
        assert is_sunny("CLEAR") is True
        assert is_sunny("Sunny") is True
        assert is_sunny("SUNNY") is True


class TestWeatherInfo:
    """WeatherInfo 클래스 테스트"""

    @pytest.fixture
    def sunny_weather(self):
        """맑은 날씨 정보 fixture"""
        return WeatherInfo(
            city="Seoul",
            country="KR",
            temperature=25.5,
            feels_like=26.0,
            humidity=60,
            description="맑음",
            wind_speed=3.5
        )

    @pytest.fixture
    def cloudy_weather(self):
        """흐린 날씨 정보 fixture"""
        return WeatherInfo(
            city="Busan",
            country="KR",
            temperature=20.0,
            feels_like=19.5,
            humidity=80,
            description="흐림",
            wind_speed=5.0
        )

    def test_weather_info_creation(self, sunny_weather):
        """WeatherInfo 객체 생성 확인"""
        assert sunny_weather.city == "Seoul"
        assert sunny_weather.country == "KR"
        assert sunny_weather.temperature == 25.5
        assert sunny_weather.feels_like == 26.0
        assert sunny_weather.humidity == 60
        assert sunny_weather.description == "맑음"
        assert sunny_weather.wind_speed == 3.5

    def test_str_contains_city_info(self, sunny_weather):
        """__str__에 도시 정보 포함 확인"""
        result = str(sunny_weather)
        assert "Seoul" in result
        assert "KR" in result

    def test_str_contains_temperature(self, sunny_weather):
        """__str__에 온도 정보 포함 확인"""
        result = str(sunny_weather)
        assert "25.5" in result
        assert "26.0" in result

    def test_str_contains_humidity(self, sunny_weather):
        """__str__에 습도 정보 포함 확인"""
        result = str(sunny_weather)
        assert "60%" in result

    def test_str_contains_description(self, sunny_weather):
        """__str__에 날씨 상태 포함 확인"""
        result = str(sunny_weather)
        assert "맑음" in result

    def test_str_contains_wind_speed(self, sunny_weather):
        """__str__에 풍속 정보 포함 확인"""
        result = str(sunny_weather)
        assert "3.5" in result

    def test_is_sunny_returns_true_for_sunny_weather(self, sunny_weather):
        """맑은 날씨에서 is_sunny() True 반환"""
        assert sunny_weather.is_sunny() is True

    def test_is_sunny_returns_false_for_cloudy_weather(self, cloudy_weather):
        """흐린 날씨에서 is_sunny() False 반환"""
        assert cloudy_weather.is_sunny() is False

    @patch('weather.display_image')
    def test_display_with_image_calls_display_when_sunny(
        self, mock_display, sunny_weather, capsys
    ):
        """맑은 날씨일 때 display_image 호출 확인"""
        sunny_weather.display_with_image()
        mock_display.assert_called_once()

    @patch('weather.display_image')
    def test_display_with_image_not_calls_display_when_cloudy(
        self, mock_display, cloudy_weather, capsys
    ):
        """흐린 날씨일 때 display_image 호출 안함 확인"""
        cloudy_weather.display_with_image()
        mock_display.assert_not_called()


class TestWeatherAPI:
    """WeatherAPI 클래스 테스트"""

    def test_init_with_api_key(self):
        """API 키로 초기화"""
        api = WeatherAPI(api_key="test-api-key")
        assert api.api_key == "test-api-key"

    def test_init_with_env_variable(self):
        """환경변수로 초기화"""
        with patch.dict(os.environ, {"OPENWEATHERMAP_API_KEY": "env-api-key"}):
            api = WeatherAPI()
            assert api.api_key == "env-api-key"

    def test_init_without_api_key_raises_error(self):
        """API 키 없이 초기화 시 에러"""
        with patch.dict(os.environ, {}, clear=True):
            if "OPENWEATHERMAP_API_KEY" in os.environ:
                del os.environ["OPENWEATHERMAP_API_KEY"]
            with pytest.raises(ValueError, match="API 키가 필요합니다"):
                WeatherAPI()

    @patch('weather.requests.get')
    def test_get_weather_by_city_success(self, mock_get):
        """도시 이름으로 날씨 조회 성공"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Seoul",
            "sys": {"country": "KR"},
            "main": {"temp": 25.0, "feels_like": 26.0, "humidity": 60},
            "weather": [{"description": "맑음"}],
            "wind": {"speed": 3.5}
        }
        mock_get.return_value = mock_response

        api = WeatherAPI(api_key="test-key")
        weather = api.get_weather_by_city("Seoul")

        assert weather.city == "Seoul"
        assert weather.country == "KR"
        assert weather.temperature == 25.0
        assert weather.description == "맑음"

    @patch('weather.requests.get')
    def test_get_weather_by_city_not_found(self, mock_get):
        """존재하지 않는 도시 조회 시 에러"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        api = WeatherAPI(api_key="test-key")
        with pytest.raises(ValueError, match="도시를 찾을 수 없습니다"):
            api.get_weather_by_city("InvalidCity")

    @patch('weather.requests.get')
    def test_get_weather_by_city_invalid_api_key(self, mock_get):
        """잘못된 API 키로 조회 시 에러"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        api = WeatherAPI(api_key="invalid-key")
        with pytest.raises(ValueError, match="유효하지 않은 API 키"):
            api.get_weather_by_city("Seoul")

    @patch('weather.requests.get')
    def test_get_weather_by_coords_success(self, mock_get):
        """좌표로 날씨 조회 성공"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Seoul",
            "sys": {"country": "KR"},
            "main": {"temp": 25.0, "feels_like": 26.0, "humidity": 60},
            "weather": [{"description": "맑음"}],
            "wind": {"speed": 3.5}
        }
        mock_get.return_value = mock_response

        api = WeatherAPI(api_key="test-key")
        weather = api.get_weather_by_coords(37.5665, 126.9780)

        assert weather.city == "Seoul"
        mock_get.assert_called_once()
        call_params = mock_get.call_args[1]['params']
        assert call_params['lat'] == 37.5665
        assert call_params['lon'] == 126.9780

    @patch('weather.requests.get')
    def test_network_error_raises_connection_error(self, mock_get):
        """네트워크 오류 시 ConnectionError 발생"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        api = WeatherAPI(api_key="test-key")
        with pytest.raises(ConnectionError, match="네트워크 오류"):
            api.get_weather_by_city("Seoul")


class TestKoreanCities:
    """한국 도시 관련 테스트"""

    def test_korean_cities_contains_major_cities(self):
        """주요 한국 도시 포함 확인"""
        expected_cities = ["서울", "부산", "인천", "대구", "대전", "광주", "울산", "세종", "제주", "수원"]
        for city in expected_cities:
            assert city in KOREAN_CITIES

    def test_korean_cities_have_valid_coordinates(self):
        """모든 도시에 유효한 좌표 확인"""
        for city, coords in KOREAN_CITIES.items():
            assert "lat" in coords
            assert "lon" in coords
            assert -90 <= coords["lat"] <= 90
            assert -180 <= coords["lon"] <= 180


class TestGetKoreanCityWeather:
    """get_korean_city_weather 함수 테스트"""

    @patch.object(WeatherAPI, 'get_weather_by_coords')
    def test_korean_city_uses_coords(self, mock_coords):
        """한국 도시명은 좌표로 조회"""
        mock_coords.return_value = WeatherInfo(
            city="Seoul", country="KR", temperature=25.0,
            feels_like=26.0, humidity=60, description="맑음", wind_speed=3.5
        )

        api = WeatherAPI(api_key="test-key")
        weather = get_korean_city_weather(api, "서울")

        mock_coords.assert_called_once()
        assert weather.city == "Seoul"

    @patch.object(WeatherAPI, 'get_weather_by_city')
    def test_non_korean_city_uses_name(self, mock_city):
        """영문 도시명은 이름으로 조회"""
        mock_city.return_value = WeatherInfo(
            city="Tokyo", country="JP", temperature=28.0,
            feels_like=29.0, humidity=70, description="sunny", wind_speed=2.0
        )

        api = WeatherAPI(api_key="test-key")
        weather = get_korean_city_weather(api, "Tokyo")

        mock_city.assert_called_once_with("Tokyo")
        assert weather.city == "Tokyo"


class TestGetMultipleCitiesWeather:
    """get_multiple_cities_weather 함수 테스트"""

    @patch('weather.get_korean_city_weather')
    def test_returns_weather_for_all_cities(self, mock_get_weather):
        """모든 도시의 날씨 반환"""
        mock_get_weather.side_effect = [
            WeatherInfo("Seoul", "KR", 25.0, 26.0, 60, "맑음", 3.5),
            WeatherInfo("Busan", "KR", 22.0, 23.0, 70, "흐림", 4.0),
        ]

        api = WeatherAPI(api_key="test-key")
        result = get_multiple_cities_weather(api, ["서울", "부산"])

        assert len(result) == 2
        assert "서울" in result
        assert "부산" in result

    @patch('weather.get_korean_city_weather')
    def test_handles_failed_city_gracefully(self, mock_get_weather, capsys):
        """실패한 도시는 건너뛰고 계속 진행"""
        mock_get_weather.side_effect = [
            WeatherInfo("Seoul", "KR", 25.0, 26.0, 60, "맑음", 3.5),
            ValueError("도시를 찾을 수 없습니다"),
            WeatherInfo("Jeju", "KR", 20.0, 21.0, 65, "맑음", 2.0),
        ]

        api = WeatherAPI(api_key="test-key")
        result = get_multiple_cities_weather(api, ["서울", "실패도시", "제주"])

        assert len(result) == 2
        assert "서울" in result
        assert "제주" in result
        assert "실패도시" not in result

    @patch('weather.get_korean_city_weather')
    def test_empty_cities_list_returns_empty_dict(self, mock_get_weather):
        """빈 도시 목록은 빈 딕셔너리 반환"""
        api = WeatherAPI(api_key="test-key")
        result = get_multiple_cities_weather(api, [])

        assert result == {}
        mock_get_weather.assert_not_called()


class TestDisplayImage:
    """display_image 함수 테스트"""

    def test_nonexistent_image_prints_warning(self, capsys):
        """존재하지 않는 이미지 파일 경고 출력"""
        fake_path = Path("/nonexistent/path/image.jpg")
        display_image(fake_path)
        
        captured = capsys.readouterr()
        assert "이미지 파일을 찾을 수 없습니다" in captured.out

    @patch('weather.HAS_PIL', False)
    def test_without_pil_prints_path(self, capsys, tmp_path):
        """PIL 없이 실행 시 경로만 출력"""
        test_image = tmp_path / "test.jpg"
        test_image.write_bytes(b"fake image data")
        
        display_image(test_image)
        
        captured = capsys.readouterr()
        assert "pip install Pillow" in captured.out


class TestSunnyKeywords:
    """SUNNY_KEYWORDS 상수 테스트"""

    def test_contains_korean_keywords(self):
        """한국어 키워드 포함 확인"""
        assert "맑음" in SUNNY_KEYWORDS
        assert "청명" in SUNNY_KEYWORDS

    def test_contains_english_keywords(self):
        """영어 키워드 포함 확인"""
        assert "clear" in SUNNY_KEYWORDS
        assert "sunny" in SUNNY_KEYWORDS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
