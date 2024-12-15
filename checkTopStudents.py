import sqlite3

# Kết nối tới database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Lấy dữ liệu từ bảng students, sắp xếp theo GPA (mark4) giảm dần
cursor.execute("""
    SELECT student_id, name, mark4
    FROM students
    ORDER BY mark4 DESC
""")
rows = cursor.fetchall()

# In ra màn hình với thứ tự sắp xếp và rank ở cuối
rank = 1
for row in rows:
    student_id, name, mark4 = row
    print(f"MSV: {student_id}, Tên: {name}, GPA: {mark4}, Rank: {rank}")
    rank += 1

# Đóng kết nối
conn.close()
