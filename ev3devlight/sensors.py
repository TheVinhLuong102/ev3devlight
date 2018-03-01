from .fileio import read_int, read_str, get_sensor_or_motor_path
from time import sleep

class Touch():
    """Configure Touch Sensor"""
    def __init__(self, port):
        self.port = port
        self.path = get_sensor_or_motor_path('lego-sensor', self.port)
        self.value_file = open(self.path + '/value0', 'rb')

    @property
    def pressed(self):
        """Return True if sensor is pressed, return False if released."""
        return True if read_int(self.value_file) else False

    @property
    def released(self):
        """Return True if sensor is released, return False if pressed."""
        return not self.pressed

    def wait_for_press(self):
        "Pause until the sensor is pressed."
        while not self.pressed:
            sleep(0.001)

    def wait_for_release(self):
        "Pause until the sensor is released."
        while self.pressed:
            sleep(0.001)           

    def wait_for_bump(self):
        "Pause until the sensor is pressed and then released. If already pressed, then just wait for a release."
        self.wait_for_press()
        self.wait_for_release()


class IRProximity():
    """Configure an IR sensor in proximity mode."""
    def __init__(self, port, threshold=50):
        self.port = port
        self.threshold = threshold
        self.path = get_sensor_or_motor_path('lego-sensor', self.port)
        with open(self.path + '/mode', 'w') as f:
            f.write('IR-PROX')
        self.value_file = open(self.path + '/value0', 'rb')

    @property
    def proximity(self):
        """Return proximity value (0 = closest, 100 = farthest)"""
        return read_int(self.value_file)

    @property
    def detected(self):
        """Return True if detected object is closer than specified threshold. Returns false otherwise"""
        return True if self.proximity <= self.threshold else False

    def wait_for_detection(self):
        "Pause until the an object is detected."
        while not self.detected:
            sleep(0.001)        