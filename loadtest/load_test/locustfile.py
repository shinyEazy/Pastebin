from locust import HttpUser, task, between
import random
import string

class PastebinUser(HttpUser):
    wait_time = between(1, 3)
    
    def generate_random_content(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    
    def random_string(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    @task
    def register(self):
        username = self.random_string()
        password = self.random_string()
        response = self.client.post(
            "/auth/register", 
            json={
                "username": username,
                "password": password,
            }
        )
        if response.status_code != 200:
            return
        self.client.post(
            "/auth/login", 
            json={
                "username": username,
                "password": password,
            }
        )

    @task(3)  
    def create_paste(self):
        content = self.generate_random_content()
        response = self.client.post(
            "/paste/pastes/",
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
            self.client.get(f"/paste/pastes/{self.paste_id}")

    @task(1)
    def view_user_paste(self):
        response = self.client.get(f"/my-pastes")
        response = self.client.get("/user/pastes")
        if response == 200:
            data = response.json()
            if not data:
                return
            random_paste = random.choice(data)
            paste_id = random_paste.get("id")
            if not paste_id:
                return
            self.client.get(f"/paste/pastes/{paste_id}")


