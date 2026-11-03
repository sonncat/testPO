from locust import HttpUser, task, between

class PublicAPIUser(HttpUser):
    """
    Класс для тестирования публичного API 
    """
    wait_time = between(1, 3)
    host = "https://jsonplaceholder.typicode.com"

    @task
    def get_posts(self):
        with self.client.get("/posts", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    response.success()
                else:
                    response.failure("Пустой список постов или неверный формат")
            else:
                response.failure(f"Ошибка: статус {response.status_code}")