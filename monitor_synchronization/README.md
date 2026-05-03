# Đồ án / Bài tập: Đồng bộ hóa bằng Monitor (Monitor-Based Synchronization)

Dự án này mô phỏng cơ chế đồng bộ hóa **Monitor** bằng ngôn ngữ Python, áp dụng để giải quyết bài toán kinh điển **Producer-Consumer (Bộ đệm giới hạn - Bounded Buffer)**.

## 1. Monitor là gì?

**Monitor** là một cấu trúc đồng bộ hóa bậc cao được cung cấp bởi các ngôn ngữ lập trình (như Java, C#, hoặc thông qua thư viện của Python/C++). Monitor đóng gói các biến chia sẻ (shared data), các thủ tục tác động lên biến đó, và cơ chế đồng bộ hóa vào trong một module duy nhất. 

Đặc điểm cốt lõi của Monitor:
- **Mutual Exclusion (Loại trừ tương hỗ):** Chỉ có MỘT luồng (thread) được phép thực thi code bên trong monitor tại một thời điểm.
- **Condition Variables (Biến điều kiện):** Cho phép các luồng tạm dừng (block) và chờ đợi (wait) cho đến khi một điều kiện nào đó thỏa mãn, và luồng khác có thể gửi tín hiệu (notify/signal) để đánh thức chúng.

## 2. Ưu điểm của việc sử dụng Monitor

1. **An toàn và Dễ sử dụng (Safety & Simplicity):** Khóa (lock) được quản lý ngầm định. Người lập trình không cần gọi `acquire()` và `release()` ở khắp mọi nơi một cách thủ công, từ đó giảm thiểu tối đa rủi ro gây ra Deadlock (do quên nhả khóa).
2. **Tính Đóng gói (Encapsulation):** Toàn bộ logic chia sẻ và đồng bộ hóa được gom gọn vào trong một lớp (Class), giúp mã nguồn sạch sẽ, dễ đọc và dễ bảo trì.
3. **Mô hình hóa tốt hơn:** Giúp lập trình viên tư duy ở mức trừu tượng cao hơn thay vì phải đối mặt trực tiếp với các cơ chế cấp thấp.

## 3. So sánh Monitor với các cơ chế khác

| Tiêu chí | Monitor | Semaphore | Mutex (Khóa) |
| :--- | :--- | :--- | :--- |
| **Mức độ trừu tượng** | Bậc cao (High-level) | Bậc thấp (Low-level) | Bậc thấp |
| **Loại trừ tương hỗ** | Ngầm định (Implicit) | Phải tự gọi Wait(P) / Signal(V) | Phải tự gọi Lock / Unlock |
| **Quản lý trạng thái** | Sử dụng Biến điều kiện (Condition Variables) | Dùng giá trị số nguyên (Integer counter) | Không có (chỉ có trạng thái Khóa/Mở) |
| **Nguy cơ lỗi (Bugs)** | Thấp (Ít rủi ro Deadlock hơn) | Cao (Rất dễ nhầm lẫn thứ tự Wait/Signal) | Trung bình (Quên nhả khóa gây Deadlock) |

**Tóm lại:** Monitor có thể được xem như sự kết hợp giữa **Mutex** (để khóa) và một hoặc nhiều **Biến điều kiện** (để quản lý luồng chờ).

## 4. Cấu trúc Dự án

- `monitor.py`: Định nghĩa lớp `Monitor` cốt lõi và lớp `BoundedBufferMonitor` (triển khai bài toán Producer-Consumer).
- `main.py`: Kịch bản chạy mô phỏng, tạo ra nhiều luồng (threads) Producer và Consumer chạy song song.

## 5. Hướng dẫn chạy

Dự án sử dụng thuần thư viện chuẩn của Python, không cần cài đặt thêm bất kỳ thư viện bên ngoài nào.

1. Mở terminal / command prompt.
2. Điều hướng đến thư mục chứa dự án.
3. Chạy file main:

```bash
python main.py
```

Bạn sẽ thấy log in ra luân phiên quá trình các luồng sản xuất và tiêu thụ dữ liệu, cách chúng chờ đợi nhau khi buffer ĐẦY (Full) hoặc RỖNG (Empty).
