from flask import Flask, render_template, request, session, url_for, redirect, send_file
import sqlite3
import requests
import csv
from io import StringIO
from unidecode import unidecode
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__, static_folder='static')
app.secret_key = "nguyenvannam"
student_info = []

import sqlite3

# Hàm khởi tạo cơ sở dữ liệu
def init_db():
    """Khởi tạo cơ sở dữ liệu và tạo bảng sheet nếu chưa tồn tại."""
    conn = sqlite3.connect('sheet.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sheet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            full_name TEXT,
            class_name TEXT,
            project_score REAL,
            absence INTEGER,
            participation REAL,
            total_score REAL
        )
    ''')
    conn.commit()
    conn.close()


def save_to_database(data):
    """
    Lưu dữ liệu vào bảng sheet trong cơ sở dữ liệu. 
    Chỉ thêm dữ liệu mới nếu student_id chưa tồn tại.
    """
    conn = sqlite3.connect('sheet.db')
    cursor = conn.cursor()

    # Kiểm tra và tạo bảng nếu chưa tồn tại
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sheet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            full_name TEXT,
            class_name TEXT,
            project_score REAL,
            absence INTEGER,
            participation REAL,
            total_score REAL
        )
    ''')

    for row in data:
        print(f"Đang xử lý: {row}")
        if not row[0]:  # Bỏ qua nếu student_id trống hoặc không hợp lệ
            print(f"Bỏ qua dòng vì student_id không hợp lệ: {row}")
            continue

        # Kiểm tra nếu student_id đã tồn tại
        cursor.execute('SELECT COUNT(*) FROM sheet WHERE student_id = ?', (row[0],))
        if cursor.fetchone()[0] == 0:
            # Chèn dữ liệu mới nếu student_id chưa tồn tại
            cursor.execute('''
                INSERT INTO sheet (student_id, full_name, class_name, project_score, absence, participation, total_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', row)
        else:
            print(f"student_id đã tồn tại, bỏ qua: {row[0]}")

    conn.commit()
    conn.close()

# Hàm để lấy dữ liệu từ Google Sheets
def get_google_sheet_data(sheet_url):
    response = requests.get(sheet_url)
    response.encoding = 'utf-8-sig'  # Đảm bảo mã hóa là UTF-8
    response.raise_for_status()  # Kiểm tra lỗi khi tải dữ liệu
    lines = response.text.strip().split("\n")
    
    # Bỏ qua 2 dòng đầu tiên (dòng tiêu đề)
    data = [line.split(",") for line in lines[1:]]  # Lấy từ dòng thứ 3 trở đi
    return data

@app.route("/")
def home():
    return render_template("html/login.html")

@app.route("/login", methods=["POST"])
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")

    login_url = "https://sinhvien1.tlu.edu.vn/education/oauth/token"
    login_data = {
        "username": username,
        "password": password,
        "client_id": "education_client",
        "grant_type": "password",
        "client_secret": "password",
    }

    try:
        response = requests.post(login_url, json=login_data, verify=False)
        response.raise_for_status()

        if response.status_code == 200:
            user_info = response.json()
            access_token = user_info.get("access_token")

            summary_url = "https://sinhvien1.tlu.edu.vn/education/api/studentsummarymark/getbystudent"
            headers = {"Authorization": f"Bearer {access_token}"}
            summary_response = requests.get(summary_url, headers=headers, verify=False)
            summary_response.raise_for_status()

            if summary_response.status_code == 200:
                data = summary_response.json()
                display_name = data.get("student", {}).get("displayName", None)
                created_by = data.get("student", {}).get("createdBy", None)  # Mã sinh viên
                speciality_name = data.get("student", {}).get("enrollmentClass", {}).get("speciality", {}).get("name", None)
                department_name = data.get("student", {}).get("enrollmentClass", {}).get("department", {}).get("name", None)
                class_name = data.get("student", {}).get("enrollmentClass", {}).get("className", None)
                mark = data.get("mark", None)
                mark4 = data.get("mark4", None)  # Lấy giá trị GPA (mark4)

                conn = sqlite3.connect("students.db")  # Kết nối với tệp SQLite
                cursor = conn.cursor()
                
                # Tạo bảng nếu chưa có (bao gồm mark4)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        student_id TEXT UNIQUE,
                        speciality TEXT,
                        department TEXT,
                        class_name TEXT,
                        mark REAL,
                        mark4 REAL  -- Thêm trường mark4 vào bảng
                    )
                """)

                # Kiểm tra xem mã sinh viên đã tồn tại chưa
                cursor.execute("SELECT COUNT(*) FROM students WHERE student_id = ?", (created_by,))
                exists = cursor.fetchone()[0]

                if exists > 0:
                    print(f"Mã số sinh viên {created_by} đã tồn tại. Không thêm vào cơ sở dữ liệu.")
                else:
                    # Thêm thông tin sinh viên vào bảng (bao gồm mark4)
                    cursor.execute("""
                        INSERT INTO students (name, student_id, speciality, department, class_name, mark, mark4)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (display_name, created_by, speciality_name, department_name, class_name, mark, mark4))

                    conn.commit()  # Lưu thay đổi
                    print("Dữ liệu đã được lưu vào SQLite thành công.")

                conn.close()  # Đóng kết nối

                # Lưu thông tin vào session (bao gồm mark4)
                student_info = [
                    display_name if display_name else None,
                    created_by if created_by else None,
                    speciality_name if speciality_name else None,
                    department_name if department_name else None,
                    class_name if class_name else None,
                    mark,
                    mark4  # Thêm mark4 vào session để hiển thị trên Dashboard
                ]
                session['data_user'] = student_info

                return redirect(url_for('backdashboard'))
            else:
                return render_template("html/login.html", error="Không thể lấy thông tin sinh viên.")
        else:
            return render_template("html/login.html", error="Đăng nhập thất bại. Kiểm tra lại tài khoản hoặc mật khẩu.")
    except Exception as e:
        return render_template("html/login.html", error=f"Lỗi khi đăng nhập: {e}")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/sheet')
def sheet():
    # URL của Google Sheets
    sheet_url = 'https://docs.google.com/spreadsheets/d/1nq_6IFrokuaSUDooZLv9t1iXFF_GhWtZyMZVOYSerTw/export?format=csv'
    google_sheet_data = get_google_sheet_data(sheet_url)

    # Lọc dữ liệu và tính toán Tổng Điểm
    filtered_data = []
    for student in google_sheet_data:
        try:
            full_name = student[2] + ' ' + student[3]
            student_id = student[1]
            class_name = student[4]
            project_score = float(student[20]) if student[20] else 0.0
            absence = int(student[22]) if student[22] else 0
            participation = float(student[23]) if student[23] else 0.0
            total_score = (0.5*project_score) + participation + (15 - absence)

            if not student_id:  # Bỏ qua nếu không có student_id
                print(f"Dòng không hợp lệ: {student}")
                continue

            filtered_data.append([student_id, full_name, class_name, project_score, absence, participation, total_score])
        except IndexError as e:
            print(f"Lỗi thiếu dữ liệu trong dòng: {student} - {e}")
        except ValueError as e:
            print(f"Lỗi giá trị không hợp lệ trong dòng: {student} - {e}")
        except Exception as e:
            print(f"Lỗi không xác định: {student} - {e}")

    # Lưu dữ liệu vào cơ sở dữ liệu
    save_to_database(filtered_data)

    # Tính STT và thêm vào dữ liệu hiển thị
    stt_data = []
    for index, row in enumerate(filtered_data, start=1):  # Bắt đầu STT từ 1
        stt_data.append([index] + row)

    # Lấy Top 3 người có tổng điểm cao nhất và thấp nhất
    top3_high = sorted(stt_data, key=lambda x: x[-1], reverse=True)[:3]
    top3_low = sorted(stt_data, key=lambda x: x[-1])[:3]

    # Lấy số trang từ query string (default là 1 nếu không có)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    paginated_data = stt_data[(page - 1) * per_page : page * per_page]
    total_pages = len(stt_data) // per_page + (1 if len(stt_data) % per_page > 0 else 0)

    return render_template("html/GoogleSheet.html", students=paginated_data, top3_high=top3_high, top3_low=top3_low, page=page, total_pages=total_pages)

@app.route('/dashboard')
def backdashboard():
    # Lấy thông tin người dùng từ session
    data_user = session.get('data_user', None)
    if data_user is None:
        return redirect(url_for('home'))  # Quay lại trang login nếu chưa đăng nhập
    
    # Số lượng mục trên mỗi trang
    items_per_page = 4
    
    # Lấy số trang hiện tại từ query parameter (mặc định là trang 1)
    page = request.args.get('page', 1, type=int)
    
    # Tính toán offset dựa trên trang hiện tại và số mục trên mỗi trang
    offset = (page - 1) * items_per_page
    
    # Kết nối cơ sở dữ liệu
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Truy vấn lấy các mục trong phạm vi trang hiện tại, bao gồm mark4 (GPA)
    cursor.execute("""
        SELECT name, student_id, speciality, department, class_name, mark, CAST(mark4 AS REAL) as mark4
        FROM students
        ORDER BY mark4 DESC
        LIMIT ? OFFSET ?
    """, (items_per_page, offset))

    
    students = cursor.fetchall()  # Lấy tất cả kết quả trả về dưới dạng list of tuples
    
    # Truy vấn tổng số sinh viên để tính tổng số trang
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    
    # Tính tổng số trang
    total_pages = (total_students // items_per_page) + (1 if total_students % items_per_page > 0 else 0)
    
    # Thêm thứ tự (rank) vào danh sách sinh viên
    students_with_rank = [(offset + index + 1, *student) for index, student in enumerate(students)]
    
    # Đóng kết nối cơ sở dữ liệu
    conn.close()
    
    # Trả về template và dữ liệu
    return render_template('html/Dashboard.html', data_user=data_user, students=students_with_rank, page=page, total_pages=total_pages)


if __name__ == "__main__":
    init_db()  # Khởi tạo cơ sở dữ liệu
    app.run(debug=True)
