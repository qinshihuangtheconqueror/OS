import threading

class Monitor:
    """Lớp cơ sở đại diện cho khái niệm Monitor."""
    def __init__(self):
        self._lock = threading.RLock()

    def get_condition(self):
        return threading.Condition(self._lock)


class BoundedBufferMonitor(Monitor):
    """Monitor bài toán Producer-Consumer (Bộ đệm giới hạn)."""
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity
        self.buffer = []
        self.not_full = self.get_condition()
        self.not_empty = self.get_condition()

    def produce(self, item, producer_name):
        with self.not_full:
            while len(self.buffer) >= self.capacity:
                print(f"[{producer_name}] Buffer ĐẦY. Đang chờ...")
                self.not_full.wait()
            self.buffer.append(item)
            print(f"[{producer_name}] Đã sản xuất: {item}. Buffer: {len(self.buffer)}/{self.capacity}")
            self.not_empty.notify()

    def consume(self, consumer_name):
        with self.not_empty:
            while len(self.buffer) == 0:
                print(f"[{consumer_name}] Buffer RỖNG. Đang chờ...")
                self.not_empty.wait()
            item = self.buffer.pop(0)
            print(f"[{consumer_name}] Đã tiêu thụ: {item}. Buffer: {len(self.buffer)}/{self.capacity}")
            self.not_full.notify()
            return item

class ReadersWritersMonitor(Monitor):
    """Monitor bài toán Readers-Writers (Ưu tiên Writer để tránh đói/starvation)."""
    def __init__(self):
        super().__init__()
        self.readers = 0
        self.writers = 0
        self.waiting_writers = 0
        self.can_read = self.get_condition()
        self.can_write = self.get_condition()

    def start_read(self, reader_name):
        with self._lock:
            # Đợi nếu đang có người ghi hoặc có người ghi đang chờ
            while self.writers > 0 or self.waiting_writers > 0:
                print(f"[{reader_name}] Đang chờ để đọc...")
                self.can_read.wait()
            self.readers += 1
            print(f"[{reader_name}] + Bắt đầu ĐỌC. (Đang đọc: {self.readers}, Đang ghi: {self.writers})")

    def end_read(self, reader_name):
        with self._lock:
            self.readers -= 1
            print(f"[{reader_name}] - Kết thúc ĐỌC. (Đang đọc: {self.readers}, Đang ghi: {self.writers})")
            if self.readers == 0:
                self.can_write.notify()

    def start_write(self, writer_name):
        with self._lock:
            self.waiting_writers += 1
            while self.readers > 0 or self.writers > 0:
                print(f"[{writer_name}] Đang chờ để ghi...")
                self.can_write.wait()
            self.waiting_writers -= 1
            self.writers += 1
            print(f"[{writer_name}] + Bắt đầu GHI. (Đang đọc: {self.readers}, Đang ghi: {self.writers})")

    def end_write(self, writer_name):
        with self._lock:
            self.writers -= 1
            print(f"[{writer_name}] - Kết thúc GHI. (Đang đọc: {self.readers}, Đang ghi: {self.writers})")
            if self.waiting_writers > 0:
                self.can_write.notify()
            else:
                self.can_read.notify_all()

class DiningPhilosophersMonitor(Monitor):
    """Monitor bài toán Bữa tối của các triết gia (Dining Philosophers)."""
    def __init__(self, num_philosophers):
        super().__init__()
        self.num_philosophers = num_philosophers
        # 0 = THINKING (Suy nghĩ), 1 = HUNGRY (Đói), 2 = EATING (Đang ăn)
        self.state = [0] * num_philosophers
        self.self_cond = [self.get_condition() for _ in range(num_philosophers)]

    def _left(self, i):
        return (i + self.num_philosophers - 1) % self.num_philosophers

    def _right(self, i):
        return (i + 1) % self.num_philosophers

    def _test(self, i):
        if self.state[i] == 1 and self.state[self._left(i)] != 2 and self.state[self._right(i)] != 2:
            self.state[i] = 2
            self.self_cond[i].notify()

    def pickup(self, i):
        with self._lock:
            self.state[i] = 1 # Chuyển sang đói
            print(f"[Triết gia {i}] Đang ĐÓI và xin nĩa...")
            self._test(i)
            while self.state[i] != 2:
                self.self_cond[i].wait()
            print(f"[Triết gia {i}] Đang ĂN 🍝.")

    def putdown(self, i):
        with self._lock:
            self.state[i] = 0 # Chuyển sang suy nghĩ
            print(f"[Triết gia {i}] Đã ăn xong, bỏ nĩa xuống và SUY NGHĨ 💡.")
            self._test(self._left(i))
            self._test(self._right(i))
