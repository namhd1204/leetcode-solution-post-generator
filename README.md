# 🚀 LeetCode Solution Post Generator

Công cụ tự động hóa siêu nhẹ viết bằng Python giúp tự động lấy mã nguồn đã nộp thành công (Accepted), nội dung mô tả bài toán từ LeetCode, sau đó sử dụng các mô hình LLM (như Google Gemini hoặc Local Ollama) để tạo ra một bài viết giải thích giải thuật hoàn chỉnh, cấu trúc rõ ràng theo đúng template chuẩn của LeetCode.

---

## ✨ Tính Năng Nổi Bật

* **Siêu nhẹ & Hiệu năng cao**: Tương tác trực tiếp với API GraphQL chính thức của LeetCode qua thư viện `requests` thuần túy. Không cần cài đặt các trình duyệt ảo nặng nề như Selenium hay Playwright.
* **Hỗ trợ đa mô hình LLM**:
  * **Google Gemini API** (Mặc định sử dụng `gemini-3.5-flash` qua Google AI Studio - cực kỳ nhanh và hoàn toàn miễn phí).
  * **Local LLM** (Chạy ngoại tuyến thông qua Ollama, ví dụ: `llama3`).
* **Cơ chế xác thực an toàn**: Tự động chẩn đoán và hướng dẫn chi tiết cách lấy Session Cookie trong trường hợp cookie hết hạn hoặc bị lỗi xác thực.
* **Giao diện CLI thân thiện**: Logging theo từng bước trực quan, đầy đủ màu sắc, hỗ trợ hiển thị Emoji mượt mà trên Windows console mà không gây lỗi Encoding.
* **Template chuẩn chỉ**: Bài viết được tạo ra dưới dạng Markdown, khớp 100% với cấu trúc bài đăng giải pháp trên LeetCode:
  ```markdown
  # [Insert Short, Concise Title Here]
  # Intuition
  # Approach
  # Complexity
  * Time complexity:
  * Space complexity:
  ```

---

## 🛠️ Hướng Dẫn Cài Đặt

### Bước 1: Cài đặt thư viện phụ thuộc
Đảm bảo bạn đã cài đặt Python 3.10 trở lên. Trong thư mục dự án, chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### Bước 2: Thiết lập cấu hình hệ thống
Sao chép tệp tin cấu hình mẫu `.env.example` thành `.env`:
* **Trên Windows (PowerShell):**
  ```powershell
  cp .env.example .env
  ```
* **Trên Linux/macOS:**
  ```bash
  cp .env.example .env
  ```

Mở file `.env` vừa tạo và điền các thông tin của bạn:
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy... (API Key của bạn từ Google AI Studio)
GEMINI_MODEL=gemini-3.5-flash

# Thông tin đăng nhập LeetCode (Xem hướng dẫn lấy cookie phía dưới)
LEETCODE_SESSION=eyJhbGci...
CSRF_TOKEN=GMmb7jht...
```

---

## 🔑 Hướng Dẫn Lấy Session Cookie LeetCode

Để công cụ có thể tải được code private của bạn, bạn cần cung cấp Session Cookie từ trình duyệt đang đăng nhập LeetCode:

1. Mở trình duyệt Web (Chrome, Edge, Firefox,...) và truy cập [leetcode.com](https://leetcode.com), đảm bảo bạn **đã đăng nhập**.
2. Nhấn phím `F12` (hoặc click chuột phải -> chọn **Inspect**) để mở Developer Tools.
3. Chuyển sang tab:
   * **Chrome/Edge:** Chọn **Application** -> tại mục **Storage** ở thanh bên trái, mở rộng mục **Cookies** -> chọn `https://leetcode.com`.
   * **Firefox:** Chọn **Storage** -> mở rộng mục **Cookies** -> chọn `https://leetcode.com`.
4. Tìm 2 cookies có tên sau và copy giá trị (Value) của chúng dán vào file `.env`:
   * `LEETCODE_SESSION` ➡️ Điền vào dòng `LEETCODE_SESSION=`
   * `csrftoken` ➡️ Điền vào dòng `CSRF_TOKEN=`
5. Lưu file `.env` lại.

---

## 🚀 Hướng Dẫn Sử Dụng

Cách sử dụng vô cùng đơn giản, bạn chỉ cần truyền URL của bài toán LeetCode vào lệnh chạy:

```bash
python generate.py "https://leetcode.com/problems/unique-number-of-occurrences/"
```

### Các tùy chọn nâng cao (CLI Flags)

* **`-o` hoặc `--output`**: Chỉ định đường dẫn lưu file markdown tùy chọn. Mặc định bài viết sẽ tự động tạo thư mục và lưu tại `solutions/<slug>.md`.
  ```bash
  python generate.py "https://leetcode.com/problems/two-sum/" -o "solutions/my_two_sum_post.md"
  ```
* **`-p` hoặc `--provider`**: Thay đổi nhanh LLM provider trực tiếp từ CLI (bỏ qua giá trị mặc định trong `.env`). Hỗ trợ `gemini` hoặc `local`.
  ```bash
  python generate.py "https://leetcode.com/problems/two-sum/" --provider local
  ```
* **`-m` hoặc `--model`**: Thay đổi nhanh tên mô hình Ollama đang chạy local.
  ```bash
  python generate.py "https://leetcode.com/problems/two-sum/" --provider local --model llama3.1
  ```

---

## 🧪 Kiểm Tra Thử (Mock Pipeline Test)

Nếu bạn chưa muốn cấu hình Cookie LeetCode ngay lập tức nhưng vẫn muốn kiểm tra kết nối với mô hình LLM và xem bài viết được định dạng ra sao, hãy chạy script kiểm tra giả lập:

```bash
python verify_pipeline.py
```

Lệnh này sẽ sử dụng dữ liệu mô phỏng bài toán **Two Sum** và mã nguồn Python, gửi trực tiếp tới Gemini API và tạo ra file kết quả mẫu tại `solutions/mock-two-sum.md` giúp bạn đánh giá độ mượt mà của hệ thống prompt.

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
leetcode-solution-post-generator/
├── .env                  # Tệp lưu cấu hình cá nhân (Đừng chia sẻ file này!)
├── .env.example          # Tệp cấu hình mẫu
├── requirements.txt      # Khai báo các thư viện Python
├── config.py             # Module đọc và kiểm định cấu hình hệ thống
├── leetcode_client.py    # Client tương tác API GraphQL LeetCode & xử lý HTML
├── llm_client.py         # Client tích hợp API Gemini & Ollama
├── generate.py           # CLI entry point - giao diện tương tác người dùng
├── verify_pipeline.py    # Script chạy thử nghiệm giả lập pipeline
└── solutions/            # Thư mục tự động sinh ra chứa các bài viết giải thuật
```
