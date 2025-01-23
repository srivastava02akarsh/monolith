from locust import task, run_single_user, FastHttpUser


class Browse(FastHttpUser):
    host = "http://localhost:5000"
    
    # Define default headers globally to avoid duplication
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
    }

    # Task: Browse Page
    @task
    def browse_page(self):
        # Create a copy of default headers and modify if necessary
        headers = self.default_headers.copy()
        headers["Host"] = "localhost:5000"  # If you want to change host dynamically

        # Perform the GET request with modified headers
        with self.client.get("/browse", headers=headers, catch_response=True) as resp:
            # Error handling if the response status code is not 200
            if resp.status_code != 200:
                resp.failure(f"Request failed with status code {resp.status_code}")
            # Add additional checks on the response body if needed
            else:
                # You can log or track successful responses if needed
                pass

if __name__ == "__main__":
    run_single_user(Browse)

