import sqlite3

# Kết nối tới database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Xóa bảng sheet
cursor.execute("DROP TABLE IF EXISTS students")

# Commit các thay đổi và đóng kết nối
conn.commit()
conn.close()
