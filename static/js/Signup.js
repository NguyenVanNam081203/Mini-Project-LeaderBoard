tailwind.config = {
    darkMode: 'class',
    theme: {
      extend: {
        colors: {
          primary: {"50":"#eff6ff","100":"#dbeafe","200":"#bfdbfe","300":"#93c5fd","400":"#60a5fa","500":"#3b82f6","600":"#2563eb","700":"#1d4ed8","800":"#1e40af","900":"#1e3a8a","950":"#172554"}
        }
      },
      fontFamily: {
        'body': [
      'Inter', 
      'ui-sans-serif', 
      'system-ui', 
      '-apple-system', 
      'system-ui', 
      'Segoe UI', 
      'Roboto', 
      'Helvetica Neue', 
      'Arial', 
      'Noto Sans', 
      'sans-serif', 
      'Apple Color Emoji', 
      'Segoe UI Emoji', 
      'Segoe UI Symbol', 
      'Noto Color Emoji'
    ],
        'sans': [
      'Inter', 
      'ui-sans-serif', 
      'system-ui', 
      '-apple-system', 
      'system-ui', 
      'Segoe UI', 
      'Roboto', 
      'Helvetica Neue', 
      'Arial', 
      'Noto Sans', 
      'sans-serif', 
      'Apple Color Emoji', 
      'Segoe UI Emoji', 
      'Segoe UI Symbol', 
      'Noto Color Emoji'
    ]
      }
    }
  }

  // Xử lý sự kiện hiển thị/ẩn mật khẩu
const togglePassword = document.getElementById('togglePassword');
const passwordField = document.getElementById('password');
const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
const confirmPasswordField = document.getElementById('confirm-password');

// Chức năng để toggle (mở/ẩn) mắt
togglePassword.addEventListener('click', function() {
    if (passwordField.type === 'password') {
        passwordField.type = 'text'; // Hiển thị mật khẩu
        togglePassword.querySelector('i').classList.remove('fa-eye-slash');
        togglePassword.querySelector('i').classList.add('fa-eye');
    } else {
        passwordField.type = 'password'; // Ẩn mật khẩu
        togglePassword.querySelector('i').classList.remove('fa-eye');
        togglePassword.querySelector('i').classList.add('fa-eye-slash');
    }
});

toggleConfirmPassword.addEventListener('click', function() {
    if (confirmPasswordField.type === 'password') {
        confirmPasswordField.type = 'text'; // Hiển thị mật khẩu xác nhận
        toggleConfirmPassword.querySelector('i').classList.remove('fa-eye-slash');
        toggleConfirmPassword.querySelector('i').classList.add('fa-eye');
    } else {
        confirmPasswordField.type = 'password'; // Ẩn mật khẩu xác nhận
        toggleConfirmPassword.querySelector('i').classList.remove('fa-eye');
        toggleConfirmPassword.querySelector('i').classList.add('fa-eye-slash');
    }
});

document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Ngừng việc gửi form mặc định

    // Lấy dữ liệu từ các trường trong form
    const name = document.getElementById("name").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm-password").value.trim();

    // Kiểm tra xem các trường có đủ dữ liệu không
    if (!name || !password || !confirmPassword) {
        alert("Vui lòng điền đầy đủ các trường!");
        return;
    }

    // Kiểm tra mật khẩu có khớp không
    if (password !== confirmPassword) {
        alert("Mật khẩu không khớp!");
        console.log(`Password: "${password}", Confirm Password: "${confirmPassword}"`);
        return;
    }

    // Gửi dữ liệu đến server
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Đăng ký thành công!");
            // Xử lý thành công (ví dụ: chuyển hướng người dùng)
        } else {
            alert("Đã có lỗi xảy ra!");
        }
    })
    .catch(error => {
        console.error("Có lỗi xảy ra:", error);
        alert("Không thể kết nối với máy chủ.");
    });
});








  