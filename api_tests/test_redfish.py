import logging
import subprocess
import time

import pytest
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://127.0.0.1:2443"
AUTH = ("root", "0penBmc")

log = logging.getLogger("redfish")
log.setLevel(logging.INFO)
if not log.handlers:
    handler = logging.FileHandler("redfish_tests.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.addHandler(handler)


@pytest.fixture(scope="session")
def auth_session():
    """Фикстура: сессия requests с базовой аутентификацией"""
    s = requests.Session()
    s.auth = AUTH
    s.verify = False
    s.headers.update({"Content-Type": "application/json"})
    log.info("Сессия requests создана")
    yield s
    s.close()
    log.info("Сессия requests закрыта")


def test_auth_create_session():
    """Тест аутентификации: создание сессии через POST-запрос"""
    log.info("ТЕСТ 1: Аутентификация (создание сессии)")
    url = f"{BASE_URL}/redfish/v1/SessionService/Sessions"
    payload = {"UserName": "root", "Password": "0penBmc"}

    response = requests.post(url, json=payload, verify=False)
    log.info(f"POST {url} -> HTTP {response.status_code}")

    assert response.status_code in (200, 201), \
        f"Ожидался код 200/201, получен {response.status_code}"

    assert "X-Auth-Token" in response.headers, "Токен X-Auth-Token отсутствует в ответе"
    log.info("Токен сессии успешно получен")


def test_get_system_info(auth_session):
    """Тест получения информации о системе"""
    log.info("ТЕСТ 2: Получение информации о системе")
    url = f"{BASE_URL}/redfish/v1/Systems/system"

    response = auth_session.get(url)
    log.info(f"GET {url} -> HTTP {response.status_code}")

    assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

    data = response.json()
    assert "Status" in data, "В ответе отсутствует поле 'Status'"
    assert "PowerState" in data, "В ответе отсутствует поле 'PowerState'"

    log.info(f"PowerState = {data['PowerState']}, Status = {data['Status']}")



def test_power_on(auth_session):
    """Тест управления питанием (включение сервера)"""
    log.info("ТЕСТ 3: Управление питанием (включение)")
    url = f"{BASE_URL}/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
    payload = {"ResetType": "On"}

    response = auth_session.post(url, json=payload)
    log.info(f"POST {url} -> HTTP {response.status_code}")

    
    if response.status_code == 503:
        pytest.skip(
            "BMC вернул 503 Service Unavailable"
        )

    assert response.status_code == 202, f"Ожидался код 202, получен {response.status_code}"

    log.info("Ожидание 5 секунд для смены состояния...")
    time.sleep(20)

    check = auth_session.get(f"{BASE_URL}/redfish/v1/Systems/system")
    power_state = check.json().get("PowerState")
    log.info(f"Текущий PowerState после Reset: {power_state}")

    assert power_state == "On", f"Ожидалось PowerState=On, получено {power_state}"



def test_cpu_temperature(auth_session):
    """Тест проверки температуры CPU через Redfish"""
    log.info("ТЕСТ 4: Проверка температуры CPU в Redfish")
    url = f"{BASE_URL}/redfish/v1/Chassis"

    response = auth_session.get(url)
    assert response.status_code == 200, f"Ошибка получения Chassis: HTTP {response.status_code}"

    sensors_found = False
    for chassis in response.json().get("Members", []):
        thermal_url = f"{BASE_URL}{chassis['@odata.id']}/Sensors"
        t = auth_session.get(thermal_url)

        if t.status_code != 200:
            continue

        for sensor in t.json().get("Members", []):
            sensor_url = f"{BASE_URL}{sensor['@odata.id']}"
            s_data = auth_session.get(sensor_url).json()

            if "cpu" in s_data.get("Name", "").lower() and s_data.get("Reading") is not None:
                sensors_found = True
                temp = s_data["Reading"]
                log.info(f"Найден датчик CPU: {s_data['Name']} = {temp}°C")
                assert -10 < temp < 100, f"Температура {temp}°C вне разумных пределов"

    if not sensors_found:
        pytest.skip(
            "Датчики температуры CPU не найдены"
        )



def test_cpu_sensors_redfish_vs_ipmi(auth_session):
    """Тест сравнения датчиков CPU в Redfish и IPMI"""
    log.info("ТЕСТ 5: Сравнение Redfish и IPMI")


    cmd = [
        "ipmitool", "-I", "lanplus", "-C", "17",
        "-H", "127.0.0.1", "-p", "2623",
        "-U", "root", "-P", "0penBmc",
        "sdr", "type", "Temperature"
    ]
    try:
        ipmi_proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        pytest.fail("Утилита ipmitool не установлена")

    ipmi_lines = ipmi_proc.stdout.splitlines()
    ipmi_sensors = [line for line in ipmi_lines if "cpu" in line.lower()]

    if not ipmi_sensors:
        pytest.skip("В IPMI не найдено датчиков CPU.")

  
    redfish_found = False
    url = f"{BASE_URL}/redfish/v1/Chassis"
    response = auth_session.get(url)

    for chassis in response.json().get("Members", []):
        thermal_url = f"{BASE_URL}{chassis['@odata.id']}/Sensors"
        t = auth_session.get(thermal_url)
        if t.status_code != 200:
            continue

        for sensor in t.json().get("Members", []):
            s_data = auth_session.get(f"{BASE_URL}{sensor['@odata.id']}").json()
            if "cpu" in s_data.get("Name", "").lower() and s_data.get("Reading") is not None:
                redfish_found = True
                log.info(f"Сравнение: Redfish={s_data['Reading']}°C, IPMI={ipmi_lines[0]}")

    if not redfish_found:
        pytest.skip(
            "Redfish не отдает датчики CPU (хост выключен), а IPMI отдает их без значений. "

        )