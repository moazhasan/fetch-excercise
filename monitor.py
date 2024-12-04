import sys
import yaml
import requests
from collections import defaultdict
from urllib.parse import urlparse
import time
import signal

class EndpointMonitor:
    def __init__(self, config_path):
        self.endpoints = self.loadConfig(config_path)  # Load endpoints from the config file
        self.urlStats = defaultdict(lambda: {'up': 0, 'total': 0})  # Track stats for each URL
        self.running = True
        signal.signal(signal.SIGINT, self.handleExit)

    def loadConfig(self, config_path):
        try:   
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)  # Load configuration from YAML file
        except Exception as e:
            print(f"Error loading YAML file: {e}")
            sys.exit(1)

    def getDomain(self, url):
        return urlparse(url).netloc

    def checkEndpoint(self, endpoint):
        method = endpoint.get('method', 'GET')
        url, headers, body = endpoint['url'], endpoint.get('headers', {}), endpoint.get('body')
        retries = 3  # Number of retries
        delay = 1  # Initial delay in seconds

        for attempt in range(retries + 1):  # Retries + initial attempt
            try:
                startTime = time.time()
                response = requests.request(method=method,url=url,headers=headers,data=body,timeout=5)
                latency = (time.time() - startTime) * 1000  # Convert to milliseconds

                # Check if endpoint is UP (status 2xx and latency < 500ms)
                isUp = response.status_code >= 200 and response.status_code < 300 and latency < 500


                # Update stats for this URL
                self.urlStats[url]['total'] += 1
                if isUp:
                    self.urlStats[url]['up'] += 1

                return isUp

            except requests.RequestException:
                if attempt < retries:
                    print(f"Error accessing {url}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    self.urlStats[url]['total'] += 1  # Increment total even on failure
                    return False

    def runHealthChecks(self):
        while self.running:
            # Check each endpoint
            for endpoint in self.endpoints:
                self.checkEndpoint(endpoint)

            # Log availability percentages for each URL
            self.logAvailability()

            # Wait for next cycle
            time.sleep(5)

    def logAvailability(self):
        for endpoint in self.endpoints:
            url = endpoint['url']
            stats = self.urlStats[url]  # Access stats for each URL
            percentage = round(100 * stats['up'] / stats['total']) if stats['total'] > 0 else 0
            if percentage == 0:
                self.slackNotification(url)
                print(f"{url} has {percentage}% availability percentage")
            else:
                print(f"{url} has {percentage}% availability percentage")
        print()  # Empty line for readability

    def handleExit(self, signum, frame):
        print("\nShutting down...")
        self.running = False
    def slackNotification(self,url):
        print(f"sending slack notif for down URL {url} ",)

def main():
    if len(sys.argv) != 2:
        print("Usage: python monitor.py <yaml_file_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    monitor = EndpointMonitor(config_path)
    monitor.runHealthChecks()

if __name__ == "__main__":
    main()
