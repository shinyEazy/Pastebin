from locust import HttpUser, task, between
import random
import string

class PastebinUser(HttpUser):
    wait_time = between(1, 3)
    
    def generate_random_content(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=50))

    @task(3)  
    def create_paste(self):
        content = self.generate_random_content()
        response = self.client.post(
            "/api/pastes/",
            json={
                "content": content,
                "expiration": "Never"
            }
        )
        if response.status_code == 200:
            self.paste_id = response.json()["id"]

    @task(1)
    def view_paste(self):
        if hasattr(self, "paste_id"):
            self.client.get(f"/api/pastes/{self.paste_id}")