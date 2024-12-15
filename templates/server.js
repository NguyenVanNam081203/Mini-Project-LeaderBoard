const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');

// Khởi tạo ứng dụng Express
const app = express();
const port = 3000;

// Middleware để parse JSON body
app.use(bodyParser.json());

// Mở kết nối đến SQLite database
const db = new sqlite3.Database('./users.db', (err) => {
    if (err) {
        console.error("Không thể mở database:", err.message);
    }
    console.log('Connected to the SQLite database.');
});

// API để xử lý đăng ký người dùng
app.post('/register', (req, res) => {
    const { name, password } = req.body;

    // Kiểm tra dữ liệu
    if (!name || !password) {
        return res.json({ success: false, message: 'Dữ liệu không hợp lệ.' });
    }

    // Chèn dữ liệu vào bảng users
    const query = `INSERT INTO users (name, password) VALUES (?, ?)`;
    db.run(query, [name, password], function(err) {
        if (err) {
            return res.json({ success: false, message: 'Đã có lỗi xảy ra khi lưu dữ liệu.' });
        }
        res.json({ success: true, message: 'Đăng ký thành công!' });
    });
});

// Lắng nghe cổng
app.listen(port, () => {
    console.log(`Server đang chạy tại http://localhost:${port}`);
});
