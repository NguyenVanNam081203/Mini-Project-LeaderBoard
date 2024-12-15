import sqlite3

# Kết nối tới database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Lấy dữ liệu từ bảng sheet
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

# In ra màn hình
for row in rows:
    print(row)

# Đóng kết nối  
conn.close()
