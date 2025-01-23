from locust import task, run_single_user, FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    # Use on_start method to perform login
    def on_start(self):
        self.username = "test123"
        self.password = "test123"
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")

    host = "http://localhost:5000"

    # Set default headers globally
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def t(self):
        # Prepare the request headers with token injected
        headers = self.default_headers.copy()
        headers.update({
            "Cookies": f"token={self.token}",
            "Referer": "http://localhost:5000/product/1",
        })
        
        with self.client.get(
            "/cart",
            headers=headers,
            catch_response=True,
        ) as resp:
            # Optional: Add response validation or checks
            if resp.status_code != 200:
                resp.failure("Request failed")

