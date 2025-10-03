# Quy Chế Cuộc Thi Viettel AI Race - Vòng Thi Online - Giai Đoạn 1

| Mục | Chi tiết |
| :--- | :--- |
| **Vòng thi** | Vòng thi Online - Giai đoạn 1 |
| **Thời gian** | Văn bản kỹ thuật - R1 - Public - 8 days 17:14:54 (Thời điểm hiện tại trên giao diện) |
| **Tác vụ** | Tác vụ 2: Khai phá Tri Thức từ Văn Bản Kỹ Thuật |

---

## Tổng Quan Đề Bài

Trong các lĩnh vực công nghiệp, năng lượng, hàng không, hay y sinh, hàng triệu trang **tài liệu kỹ thuật** đang được tạo ra và lưu trữ dưới định dạng PDF mỗi ngày. Bên trong đó là vô vàn bảng biểu phức tạp. Những kho dữ liệu này chính là **mỏ vàng tri thức**, nhưng hiện nay phần lớn vẫn "nằm yên" dưới dạng văn bản khó truy cập.

**Câu hỏi đặt ra:** Làm thế nào để máy tính có thể tự động đọc, hiểu và trả lời truy vấn từ những bảng dữ liệu kỹ thuật khổng lồ này?

Trong bối cảnh đó, hai nhu cầu quan trọng được xác định:
1.  **Trích xuất dữ liệu:** Chuyển đổi những bảng PDF phức tạp thành cấu trúc dữ liệu số chính xác, có thể khai thác và lưu trữ.
2.  **Truy vấn dữ liệu:** Dựa trên dữ liệu văn bản đã được chuyển đổi, thí sinh thực hiện nhiệm vụ trả lời các câu hỏi trắc nghiệm có thể có nhiều đáp án đúng (Multiple Choice Q&A).

---

## Nhiệm Vụ

Thí sinh sẽ thực hiện hai nhiệm vụ mang tính nền tảng:

### Nhiệm Vụ 1: Trích Xuất Dữ Liệu

Biến các bảng dữ liệu PDF nhiều tầng lớp thành dữ liệu số chuẩn lưu dưới dạng **`.md`**, có thể dùng ngay cho phân tích.

#### Thách Thức Dữ Liệu PDF:
* Chứa **watermark phức tạp**.
* Bảng dài hàng trăm trang, có thể **trải qua nhiều trang**.
* **Merge cells** ngang/dọc, **tiêu đề lồng nhau**.
* Nội dung pha trộn **đa ngôn ngữ**, **ký hiệu toán học** và **thuật ngữ chuyên ngành**.

#### Yêu Cầu Chi Tiết:
1.  Mô hình trích xuất làm việc với tệp dữ liệu đầu vào định dạng **`.pdf`**.
2.  Kết quả trích xuất được lưu dưới dạng tệp **`.md`** với định dạng cụ thể:
    * Các bảng được chuyển đổi sang **HTML table** trong Markdown.
    * Hình ảnh và công thức được thay thế bằng placeholder: **`|<image_n>|`**, **`|<formula_n>|`** theo thứ tự xuất hiện. Các hình ảnh và công thức sẽ được lưu cùng tệp **`.md`**.
    * Các thành phần khác (`heading`, `bullet list`, `code block`) phải **giữ nguyên định dạng Markdown**.

### Nhiệm Vụ 2: Truy Vấn Dữ Liệu (Multiple Choice Q&A)

Trả lời các câu hỏi trắc nghiệm với 4 lựa chọn A, B, C, D, trong đó **mỗi câu có thể có nhiều đáp án đúng**. Thí sinh phải dùng dữ liệu trích xuất được từ nhiệm vụ 1.

#### Yêu Cầu Chi Tiết:
1.  Các câu hỏi được lưu trong tệp **`question.csv`** chứa các câu hỏi và 4 lựa chọn A, B, C, D.
2.  Mỗi câu hỏi cần bóc ra **số lượng câu hỏi trả lời đúng** và **danh sách các câu trả lời**.

---

## Cấu Trúc Dữ Liệu

### Training Data

| Loại | Tên tệp/thư mục | Nội dung |
| :--- | :--- | :--- |
| **Input** | `training_input.zip` | Gồm các tệp **PDF** cần trích xuất và một tệp **`question.csv`**. |
| **Output** | `training_output.zip` | Gồm một tệp **`answer.md`** và một tập các **thư mục con** (tên thư mục con là tên của tệp PDF). |

#### Chi tiết Output:
* **Trong mỗi thư mục con PDF:**
    * Tệp **`main.md`** chứa nội dung trích xuất.
    * Thư mục con **`images`** chứa ảnh và công thức được trích xuất.
* **Tệp `answer.md`** (kết quả tổng hợp):
    * **Phần trích xuất:** Bắt đầu từ `### TASK EXTRACT`, tiếp theo là `# tên_tệp_pdf` và nội dung trích xuất (trùng với `main.md`).
    * **Phần QA:** Bắt đầu từ `### TASK QA`, sau đó là thông tin gồm **số lượng câu đúng** và **danh sách các đáp án đúng**. Thứ tự các câu trả lời giữ nguyên như trong `training_question.csv`.

### Public Test Data & Private Test Data

* **Input:** Tệp **`public_test_input.zip`** / **`private_test_input.zip`** có cấu trúc như `training_input.zip`.
* **Output (Nộp bài):** Tệp **`public_test_output.zip`** / **`private_test_output.zip`** có cấu trúc như `training_output.zip` và phải chứa thêm tệp **`main.py`** (chứa tất cả source code, không yêu cầu chạy được, dùng để kiểm tra tính trung thực).

---

## Yêu Cầu Kỹ Thuật

1.  Bắt buộc sử dụng các mô hình **mã nguồn mở** với số lượng tham số **dưới 4B** cho mỗi nhiệm vụ.
2.  Được phép áp dụng các phương pháp **data augmentation**.

### Yêu Cầu Hậu Kiểm:
Mỗi đội phải cung cấp **đường dẫn (link)** chứa toàn bộ **mã nguồn**, tệp **`requirement`**, **checkpoint** và **hướng dẫn huấn luyện** (GitHub ở chế độ chỉ chia sẻ cho BTC).

Hệ thống nộp phải là một pipeline thống nhất:
* Chạy tệp **`run_extract.sh`**: Tự động chuyển đổi dữ liệu đầu vào PDF thành tập dữ liệu Markdown. Dữ liệu cần được xử lý và lập chỉ mục **hoàn toàn trên môi trường cục bộ** (RAM hoặc file local), **không được sử dụng cơ sở dữ liệu bên ngoài**.
* Chạy tệp **`run_choose_answer.sh`**: Tự động duyệt qua các câu hỏi và xuất ra tệp kết quả.

---

## Cách Thức Chấm Điểm

Điểm tổng hợp cho 2 nhiệm vụ được tính theo công thức:

$$\text{Score} = \alpha \cdot \text{Score}_{\text{Extraction}} + \beta \cdot \text{Score}_{\text{QA}}$$

Trong đó:
* $\alpha$: hệ số cho phần trích xuất.
* $\beta$: hệ số cho phần truy vấn.
* $\text{Score}_{\text{Extraction}}$: điểm trích xuất dữ liệu (thang 100).
* $\text{Score}_{\text{QA}}$: điểm truy vấn dữ liệu (thang 100).

### Nhiệm Vụ 1 (Extraction)

* **Độ đo:** Phương pháp **Evaluation Suite** trong paper **"READOC: A Unified Benchmark for Realistic Document Structured Extraction"** ([https://www.arxiv.org/pdf/2409.05137](https://www.arxiv.org/pdf/2409.05137)).
* **Thang điểm:** 100.
* **Lưu ý:** Ban tổ chức sử dụng thêm hàm `normalize` để quy các chuỗi chứa nhiều dấu cách liên tiếp về một dấu cách duy nhất.

### Nhiệm Vụ 2 (QA)

* **Độ đo:** Cơ chế **Partial Credit** với **Halves Method** cho các câu hỏi có nhiều đáp án đúng. Chuẩn hóa về thang 100.
* **Chi tiết Halves Method (áp dụng cho $N=4$ lựa chọn):**

| Số lỗi ($E$) | Điểm ($S / S_{\max}$) |
| :---: | :---: |
| $E=0$ | $100\%$ |
| $E=1$ | $50\%$ |
| $E \ge 2$ | $0\%$ |

**Tóm tắt:** Với $N=4$, chỉ có ba trường hợp cho điểm: **100%** (không lỗi), **50%** (1 lỗi), hoặc **0%** (2 lỗi trở lên).

---

## Dữ Liệu

* `training_out.zip`
* `public_test_input.zip`
* `training_input.zip`

## Tham khảo
-  https://competition.viettel.vn/contest/online_vbkt_r1_public
