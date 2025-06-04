from sense_hat import SenseHat
import requests
import time

sense = SenseHat()
FIREBASE_DB_URL = 'https://test-6d110-default-rtdb.asia-southeast1.firebasedatabase.app'

last_message = ""

try:
    while True:
        # LED 제어
        led_response = requests.get(f'{FIREBASE_DB_URL}/led.json')
        if led_response.status_code == 200:
            led_state = led_response.json()
            if led_state and led_state.get('led') == 1:
                sense.clear(255, 0, 0)  # 빨간색
            else:
                sense.clear()  # OFF

        # 센서 데이터 읽기
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()

        # 자이로와 가속도 raw 데이터로 받기 (x, y, z)
        gyro_raw = sense.get_gyroscope_raw()
        accel_raw = sense.get_accelerometer_raw()

        sensor_data = {
            'temp': round(temperature, 4),
            'humidity': round(humidity, 4),
            'pressure': round(pressure, 4),
            'gyro': {
                'x': round(gyro_raw['x'], 4),
                'y': round(gyro_raw['y'], 4),
                'z': round(gyro_raw['z'], 4)
            },
            'accel': {
                'x': round(accel_raw['x'], 4),
                'y': round(accel_raw['y'], 4),
                'z': round(accel_raw['z'], 4)
            },
            'last_update': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        # sensor 경로에 PUT (전체 교체)
        requests.put(f'{FIREBASE_DB_URL}/sensor.json', json=sensor_data)

        # 메시지 받아오기 및 표시
        msg_response = requests.get(f'{FIREBASE_DB_URL}/message.json')
        if msg_response.status_code == 200:
            msg_data = msg_response.json()
            new_msg = msg_data.get('text', '')

        if new_msg and new_msg != last_message:
            last_message = new_msg
            clean_msg = str(new_msg).replace('\n', ' ').replace('\r', ' ')
            print("표시할 새 메시지:", repr(clean_msg))
            sense.show_message(clean_msg, scroll_speed=0.15, text_colour=[0, 0, 255])

            # ✅ message.text만 빈 문자열로 변경
            clear_response = requests.patch(f'{FIREBASE_DB_URL}/message.json', json={"text": ""})
            if clear_response.status_code == 200:
                print("메시지 초기화 완료")
            else:
                print("메시지 초기화 실패:", clear_response.status_code)

        time.sleep(1)

except KeyboardInterrupt:
    print("종료됨")
    sense.clear()
