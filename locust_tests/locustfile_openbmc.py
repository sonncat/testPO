from locust import HttpUser, task, between
import urllib3

# сертификат commit
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OpenBMCUser(HttpUser):
    """
    Класс тестирования локального OpenBMC 
    """
    wait_time = between(1, 3)
    host = "https://localhost:2443"
    
    def on_start(self):
        self.client.auth = ("root", "0penBmc")
        self.client.verify = False  # сертификат

    @task(3)
    def get_system_info(self):
        with self.client.get("/redfish/v1/Systems/system", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if "PowerState" in data:
                    response.success()
                else:
                    response.failure("В ответе нет поля PowerState")
            else:
                response.failure(f"Ошибка: статус {response.status_code}")

    @task(1)
    def get_power_state(self):
        with self.client.get("/redfish/v1/Systems/system", catch_response=True) as response:
            if response.status_code == 200:
                power_state = response.json().get("PowerState")
                if power_state in ["On", "Off", "Not available"]:
                    response.success()
                else:
                    response.failure(f"Неожиданное состояние питания: {power_state}")
            else:
                response.failure(f"Ошибка: статус {response.status_code}")