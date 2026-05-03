import threading
import time
import random
import sys
from monitor import BoundedBufferMonitor, ReadersWritersMonitor, DiningPhilosophersMonitor

# Cấu hình in tiếng Việt trên console Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# 1. BÀI TOÁN PRODUCER - CONSUMER
# ==========================================
def producer_task(monitor, pid, items):
    for i in range(items):
        time.sleep(random.uniform(0.1, 0.4))
        monitor.produce(f"Data_{pid}_{i+1}", f"Producer-{pid}")

def consumer_task(monitor, cid, items):
    for i in range(items):
        time.sleep(random.uniform(0.3, 0.6))
        monitor.consume(f"Consumer-{cid}")

def run_producer_consumer():
    print("\n" + "-"*50)
    print("CHẠY BÀI TOÁN PRODUCER - CONSUMER")
    print("-"*50)
    monitor = BoundedBufferMonitor(capacity=3)
    threads = []
    # 2 Producer, 2 Consumer
    for i in range(2):
        threads.append(threading.Thread(target=producer_task, args=(monitor, i+1, 4)))
        threads.append(threading.Thread(target=consumer_task, args=(monitor, i+1, 4)))
    
    for t in threads: t.start()
    for t in threads: t.join()
    print("Hoàn thành Producer - Consumer.")

# ==========================================
# 2. BÀI TOÁN READERS - WRITERS
# ==========================================
def reader_task(monitor, rid, times):
    for _ in range(times):
        time.sleep(random.uniform(0.2, 0.5)) # Mô phỏng làm việc gì đó trước khi đọc
        monitor.start_read(f"Reader-{rid}")
        time.sleep(random.uniform(0.1, 0.3)) # Mô phỏng đang đọc
        monitor.end_read(f"Reader-{rid}")

def writer_task(monitor, wid, times):
    for _ in range(times):
        time.sleep(random.uniform(0.3, 0.7)) # Mô phỏng làm việc gì đó trước khi ghi
        monitor.start_write(f"Writer-{wid}")
        time.sleep(random.uniform(0.2, 0.5)) # Mô phỏng đang ghi
        monitor.end_write(f"Writer-{wid}")

def run_readers_writers():
    print("\n" + "-"*50)
    print("CHẠY BÀI TOÁN READERS - WRITERS")
    print("-"*50)
    monitor = ReadersWritersMonitor()
    threads = []
    # 3 Readers, 2 Writers
    for i in range(3):
        threads.append(threading.Thread(target=reader_task, args=(monitor, i+1, 3)))
    for i in range(2):
        threads.append(threading.Thread(target=writer_task, args=(monitor, i+1, 2)))
    
    for t in threads: t.start()
    for t in threads: t.join()
    print("Hoàn thành Readers - Writers.")

# ==========================================
# 3. BÀI TOÁN DINING PHILOSOPHERS
# ==========================================
def philosopher_task(monitor, pid, times):
    for _ in range(times):
        time.sleep(random.uniform(0.1, 0.5)) # Suy nghĩ
        monitor.pickup(pid)
        time.sleep(random.uniform(0.1, 0.4)) # Ăn
        monitor.putdown(pid)

def run_philosophers():
    print("\n" + "-"*50)
    print("CHẠY BÀI TOÁN DINING PHILOSOPHERS")
    print("-"*50)
    num_philo = 5
    monitor = DiningPhilosophersMonitor(num_philo)
    threads = []
    # 5 Triết gia
    for i in range(num_philo):
        threads.append(threading.Thread(target=philosopher_task, args=(monitor, i, 2)))
    
    for t in threads: t.start()
    for t in threads: t.join()
    print("Hoàn thành Dining Philosophers.")

# ==========================================
# MAIN MENU
# ==========================================
if __name__ == "__main__":
    while True:
        print("\n" + "="*60)
        print("  MÔ PHỎNG ĐỒNG BỘ HÓA SỬ DỤNG MONITOR (PYTHON)")
        print("="*60)
        print("1. Producer - Consumer (Bộ đệm giới hạn)")
        print("2. Readers - Writers (Người đọc - Người ghi)")
        print("3. Dining Philosophers (Bữa tối của các triết gia)")
        print("0. Thoát")
        print("="*60)
        
        try:
            choice = input("Nhập lựa chọn của bạn (0-3): ").strip()
            if choice == '1':
                run_producer_consumer()
            elif choice == '2':
                run_readers_writers()
            elif choice == '3':
                run_philosophers()
            elif choice == '0':
                print("Đã thoát chương trình. Chúc bạn qua môn Hệ Điều Hành xuất sắc!")
                break
            else:
                print("=> Lựa chọn không hợp lệ, vui lòng nhập lại.")
        except KeyboardInterrupt:
            print("\nĐã thoát chương trình.")
            break
