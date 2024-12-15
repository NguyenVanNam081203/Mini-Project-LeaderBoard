import requests
from getpass import getpass

# URL API đăng nhập
login_url = "https://sinhvien1.tlu.edu.vn/education/oauth/token"

# Thông tin tài khoản và mật khẩu để kiểm tra
username = input("Nhập tên đăng nhập: ")
password = input("Nhập mật khẩu: ")

# Dữ liệu đăng nhập
login_data = {
    "username": username,
    "password": password,
    "client_id": "education_client",
    "grant_type": "password",
    "client_secret": "password",
}

try:
    # Gửi yêu cầu POST để đăng nhập
    response = requests.post(login_url, json=login_data, verify=False)  # verify=False để bỏ qua lỗi SSL
    response.raise_for_status()  # Kiểm tra nếu có lỗi HTTP

    if response.status_code == 200:
        print("Đăng nhập thành công!")
        user_info = response.json()  # Lấy thông tin người dùng từ phản hồi

        # Lấy thông tin điểm và sinh viên
        summary_url = "https://sinhvien1.tlu.edu.vn/education/api/studentsummarymark/getbystudent"
        headers = {
            'Authorization': 'Bearer ' + user_info["access_token"]
        }
        summary_response = requests.get(summary_url, headers=headers, verify=False)
        summary_response.raise_for_status()

        if summary_response.status_code == 200:
            data = summary_response.json()

            # Trích xuất dữ liệu
            mark = data.get("mark", None)
            mark4 = data.get("mark4",None)
            display_name = data.get("student", {}).get("displayName", None)
            created_by = data.get("student", {}).get("createdBy", None)

            # Hiển thị thông tin
            print("Thông tin sinh viên:")
            print(f"- Họ tên: {display_name}")
            print(f"- Mã số sinh viên: {created_by}")
            print(f"- Điểm toàn khóa: {mark}")
            print(f"- GPA: {mark4}")
        else:
            print(f"Lỗi khi lấy dữ liệu: Mã lỗi {summary_response.status_code}, Nội dung: {summary_response.text}")
    else:
        print(f"Đăng nhập thất bại: Mã lỗi {response.status_code}, Thông báo: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Lỗi khi gửi yêu cầu: {e}")
except Exception as ex:
    print(f"Lỗi: {ex}")
