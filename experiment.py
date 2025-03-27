import os
import time
import json
import psutil


class NetworkMonitor():

    def __init__(self):
        super().__init__()
        self.config_dir = "Config/"
        self.config_file =  "config.json"
        self.filePath  = os.path.join(self.config_dir, self.config_file)   
        self.default_json: dict = {
            "unit": "Bps"
        }


    def fetch_unit(self):
        if os.path.exists(self.config_dir):
            with open(self.filePath, '+r') as file:
                data = json.load(file)
            print(data)
        else:
            os.makedirs(self.config_dir, exist_ok=True)         
            file = open(self.filePath, "w")
            file.write(json.dumps(self.default_json))
            file.close()
            


    def get_network_speed(self):

        previous_packets = psutil.net_io_counters()
        time.sleep(1)
        next_packets = psutil.net_io_counters()

        download_speed = next_packets.bytes_recv - previous_packets.bytes_recv
        upload_speed =  next_packets.bytes_sent - previous_packets.bytes_sent


        print("\r" + " " * 50, end="")  # Clear previous text
        print(f"\r↓: {download_speed:.2f} Bps | ↑: {upload_speed:.2f} Bps", end="", flush=True)

    def main(self):
        # while  True:
        #     self.get_network_speed()
        self.fetch_unit()


if __name__ == "__main__":
    try:
        monitor = NetworkMonitor()
        monitor.main()
    except KeyboardInterrupt:
        print("Execution interepted.")