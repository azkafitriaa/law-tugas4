from locust import HttpUser, task

class Tugas4StressTest(HttpUser):
    @task
    def read_service(self):
        # self.client.get("/read/1906292950")
        self.client.get("/read/1906292950/111")