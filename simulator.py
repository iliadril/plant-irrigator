import configparser
import random
import time
import rabbit.emit_log as rabbit


def get_target_humidity(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return int(config['DEFAULT']['target_humidity'])


class Simulator:
    step: int = 30  # simulation step clock in seconds
    config_path: str = './data/settings.ini'

    def __init__(self):
        self.humidity: int = 350  # humidity in range <0, 750>
        self.target_humidity: int = 500  # target humidity
        self.water_level: float = 4  # water level in range <0, 4>

    def get_stats(self) -> dict:
        return {'date': int(time.time()),
                'humidity': self.humidity,
                'target_humidity': self.target_humidity,
                'water_level': self.water_level
                }

    def send_logs(self):
        rabbit.send_message('logs', f'{int(time.time())} {self.humidity} {self.target_humidity} {self.water_level}')

    def irrigate(self):
        if self.water_level > 0.0:
            self.water_level -= 0.01
            self.humidity += 13

    def evaporate(self):
        self.humidity -= random.randint(1, 5)

    def update_target_humidity(self):
        self.target_humidity = get_target_humidity(self.config_path)

    def simulate(self):
        while True:
            # update every step
            self.update_target_humidity()
            self.evaporate()

            # if water too low then irrigate
            if self.target_humidity > self.humidity:
                self.irrigate()

            # end current step
            time.sleep(self.step)
            print(self.get_stats())
            self.send_logs()


if __name__ == '__main__':
    s = Simulator()
    s.simulate()
