from PIL import Image
import requests
import io 
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

def get_latitude_longitude(address):
    client_id = os.environ["id"]
    client_secret = os.environ["key"]
    
    endpoint = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    url = f"{endpoint}?query={address}"

    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
    }
    res = requests.get(url, headers=headers)
    x_coordinate = res.json()['addresses'][0]['x']
    y_coordinate = res.json()['addresses'][0]['y']
    
    lat, lon = str(x_coordinate), str(y_coordinate)
    
    
    return lon, lat

def get_static_map(x, y):
    client_id = os.environ["id"]
    client_secret = os.environ["key"]
    endpoint = "https://naveropenapi.apigw.ntruss.com/map-static/v2/raster"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
    }
    lon, lat = x, y
    lon, lat = "127.020326886309", "37.5164324582415"
    _center = f"{lon},{lat}"
    # 줌 레벨 - 0 ~ 20
    _level = 16
    # 가로 세로 크기 (픽셀)
    _w, _h = 500, 300
    # 지도 유형 - basic, traffic, satellite, satellite_base, terrain
    _maptype = "satellite"
    # 반환 이미지 형식 - jpg, jpeg, png8, png
    _format = "png"
    # 고해상도 디스펠레이 지원을 위한 옵션 - 1, 2
    _scale = 1
    # 마커
    _markers = f"""type:d|size:mid|pos:{lon} {lat}|color:red"""
    # 라벨 언어 설정 - ko, en, ja, zh
    _lang = "ko"
    # 대중교통 정보 노출 - Boolean
    _public_transit = True
    # 서비스에서 사용할 데이터 버전 파라미터 전달 CDN 캐시 무효화
    _dataversion = ""

    # URL
    url = f"{endpoint}?center={_center}&level={_level}&w={_w}&h={_h}&maptype={_maptype}&format={_format}&scale={_scale}&markers={_markers}&lang={_lang}&public_transit={_public_transit}&dataversion={_dataversion}"
    res = requests.get(url, headers=headers)

    image_data = io.BytesIO(res.content)
    return image_data

