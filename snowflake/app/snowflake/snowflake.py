import threading
import time


def wait_until():
    time.sleep(0.010)


class SnowFlake:

    def __init__(self, node_id=0, worker_id=0, epoch=None):

        # Set epoch (default: 2020-01-01T00:00:00Z)
        # twitter epoch 1288834974657
        self.epoch = epoch if epoch is not None else 1288834974657
        self.WORKER_ID_BIT = 5
        self.NODE_ID_BIT = 5
        self.SEQUENCE_BIT = 12
        self.WORKER_ID_MAX = -1 ^ (-1 << 5)  # 31       example for n =2    1111^1100 = 0011 =3
        self.NODE_ID_MAX = -1 ^ (-1 << 5)
        self.SEQUENCE_MAX = -1 ^ (-1 << 12)  # 4095
        self.last_timestamp = -1
        self.worker_id = worker_id
        self.node_id = node_id
        self.sequence = 0

        # shift bits calculation
        # node_id bit shift
        self.WORKER_ID_BIT_BIT_SHIFT = 12
        self.NODE_ID_BIT_SHIFT = 12 + 5
        self.TIMESTAMP_BIT_SHIFT = 12 + 5 + 5
        self.lock = threading.Lock()

        if worker_id < 0 or worker_id > self.WORKER_ID_MAX:
            raise ValueError(f"Worker ID must be between 0 and {self.WORKER_ID_MAX}")
        if node_id < 0 or node_id > self.NODE_ID_MAX:
            raise ValueError(f"NODE ID must be between 0 and {self.NODE_ID_MAX}")

    def get_current_timestamp(self):
        return int(time.time() * 1000 - self.epoch)

    def generate_id(self):
        with self.lock:

            current_timestamp = self.get_current_timestamp()
            # Handle clock going backwards
            if current_timestamp < self.last_timestamp:
                # In a production system, you might want to handle this differently
                # This is a simple wait-based approach
                raise RuntimeError(f"Clock moved backwards. Refusing to generate ID for {current_timestamp}")

            if current_timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.SEQUENCE_MAX
                # all the sequence used for a given timestamp
                if self.sequence == 0:
                    wait_until()
                    current_timestamp = self.get_current_timestamp()
                # If we're in a new millisecond, reset sequence
            else:
                self.sequence = 0

            self.last_timestamp = current_timestamp

            snowflake_id = ((current_timestamp << self.TIMESTAMP_BIT_SHIFT)
                            | (self.node_id << self.NODE_ID_BIT_SHIFT)
                            | (self.worker_id << self.WORKER_ID_BIT_BIT_SHIFT)
                            | self.sequence)
            return snowflake_id
