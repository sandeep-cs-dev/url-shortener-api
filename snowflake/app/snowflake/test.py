import threading
import time


class SnowFlak:

    def __init__(self, node_id=0, worker_id=0, epoch=None):

        self.TIMESTAMP_BITS = 41
        self.NODE_ID_BITS = 5
        self.WORKER_ID_BITS = 5
        self.SEQUENCE_BITS = 12
        self.last_timestamp = -1

        self.MAX_WORKER_ID = -1 ^ (-1 << self.WORKER_ID_BITS)  # 31
        self.MAX_NODE_ID = -1 ^ (-1 << self.NODE_ID_BITS)  # 31
        self.MAX_SEQUENCE = -1 ^ (-1 << self.SEQUENCE_BITS)  # 4095

        self.worker_id = worker_id
        self.node_id = node_id
        self.sequence = 0

        self.TIMESTAMP_BITS_SHIFT = 12 + 5 + 5
        self.NODE_ID_BITS_SHIFT = 12 + 5
        self.WORKER_ID_BITS_SHIFT = 5
        # Set epoch (default: 2020-01-01T00:00:00Z)
        self.epoch = epoch if epoch is not None else 1577836800000

        # Thread safety
        self.lock = threading.Lock()

        if worker_id < 0 or worker_id > self.MAX_WORKER_ID:
            raise ValueError(f"Worker ID must be between 0 and {self.MAX_WORKER_ID}")
        if node_id < 0 or node_id > self.MAX_NODE_ID:
            raise ValueError(f"NODE ID must be between 0 and {self.MAX_NODE_ID}")

    def get_current_timestamp(self):
        return int(time.time() * 1000 - self.epoch)

    def _wait_for_next_millisecond(self, last_timestamp):
        """Wait until the next millisecond."""
        timestamp = self.get_current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self.get_current_timestamp()
        return timestamp

    def generate_id(self):

        with self.lock:
            current_timestamp = self.get_current_timestamp()

            # Handle clock going backwards
            if current_timestamp < self.last_timestamp:
                # In a production system, you might want to handle this differently
                # This is a simple wait-based approach
                raise RuntimeError(
                    f"Clock moved backwards. Refusing to generate ID for {self.last_timestamp - current_timestamp} milliseconds")

            # If we're still in the same millisecond as the last ID generation
            if current_timestamp == self.last_timestamp:

                # Increment sequence
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE

                # If we've reached the max sequence for this millisecond, wait for the next millisecond
                if self.sequence == 0:
                    current_timestamp = self._wait_for_next_millisecond(self.last_timestamp)
            else:
                # If we're in a new millisecond, reset sequence
                self.sequence = 0

            self.last_timestamp = current_timestamp

            # Combine components to create the ID
            snowflake_id = (
                    (current_timestamp << self.TIMESTAMP_BITS_SHIFT) |
                    (self.node_id << self.NODE_ID_BITS_SHIFT) |
                    (self.worker_id << self.WORKER_ID_BITS_SHIFT) |
                    self.sequence
            )

            return snowflake_id


snow = SnowFlak(1, 1, None)

res = snow.generate_id()

print(res)
