from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Simulate wait time between requests of 1 to 5 seconds

    @task
    def generate_text(self):
        payload = {"text": "Write a poem about the sea.", "max_length": 100, "seed": 42}
        headers = {"Content-Type": "application/json"}
        # Set timeout to 10 seconds
        self.client.post("/generate/", json=payload, headers=headers, timeout=50)
