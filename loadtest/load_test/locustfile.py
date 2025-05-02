from locust import HttpUser, task, between
import random, string

class PastebinUser(HttpUser):
    wait_time = between(0.1, 1)

    def on_start(self):
        self.username = self._random_string()
        self.password = self._random_string()

        # Register
        self.client.post("/auth/register", json={
            "username": self.username,
            "password": self.password
        })

        # Login
        resp = self.client.post("/auth/login", json={
            "username": self.username,
            "password": self.password
        })
        self.token = resp.json().get("access_token", None)
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _random_string(self, length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _random_content(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=100))

    @task(2)
    def create_paste(self):
        data = {
            "content": self._random_content(),
            "expiration": "Never",
            "language": "plaintext"
        }
        resp = self.client.post("/paste/pastes", json=data, headers=self.headers)
        if resp.status_code == 200:
            self.paste_id = resp.json()["id"]

    @task(3)
    def view_paste(self):
        if hasattr(self, "paste_id"):
            self.client.get(f"/paste/pastes/{self.paste_id}")
