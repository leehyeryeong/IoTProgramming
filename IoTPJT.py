from sense_hat import SenseHat
import requests
import time

# Sense HAT 초기화
sense = SenseHat()

# Firebase Realtime Database URL 설정
FIREBASE_DB_URL = 'https://test-6d110-default-rtdb.asia-southeast1.firebasedatabase.app'

try:
    while True:
        # LED 상태 확인
        led_response = requests.get(f'{FIREBASE_DB_URL}/led.json')  # 여기에는 .json이 필요합니다.
        if led_response.status_code == 200:
            led_state = led_response.json()
            if led_state and led_state.get('led') == 1:
                sense.clear(255, 0, 0)  # LED ON (빨간색)
            else:
                sense.clear()  # LED OFF

        # 온도 측정 및 업로드
        temperature = sense.get_temperature()
        temp_data = {'temp': temperature}

        # Firebase에 온도 데이터 업로드
        requests.put(f'{FIREBASE_DB_URL}/temperature.json', json=temp_data)  # 여기도 .json을 포함합니다.

        time.sleep(1)

except KeyboardInterrupt:
    print("프로그램 종료")
    sense.clear()
