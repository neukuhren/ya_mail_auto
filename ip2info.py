import requests
# from config import API_KEY_IPGEOLOCATION
API_KEY_IPGEOLOCATION = '********'


def get_ip_address():
    """Возвращает ip адрес (того прокси, который используется)"""
    url = "https://api.ipify.org?format=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        ip_address = data['ip']
        print(f'используется ip адрес: {ip_address}')
        return ip_address
    else:
        return None

def get_geolocation(ip_address) -> tuple:
    """Определение местоположения по ip адресу"""
    # url = f"https://ipvigilante.com/{ip_address}"
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY_IPGEOLOCATION}&ip={ip_address}'
    response = requests.get(url, verify=False)
    # print(response.text)
    if response.status_code == 200:
        try:
            data = response.json()
            print(f'IP адрес из города {data.get("city", "Неизвестно")}')
            latitude = data["latitude"]
            longitude = data["longitude"]
            return latitude, longitude
        except:
            return None
    else:
        pass


if __name__ == '__main__':
    ip_address = get_ip_address()

    if ip_address:
        coordinates = get_geolocation(ip_address)
        
        if coordinates:
            print(f"Широта: {coordinates[0]}, долгота: {coordinates[1]}")
        else:
            print("Неверные координаты геолокации.")
    else:
        print("Нет ip адреса")