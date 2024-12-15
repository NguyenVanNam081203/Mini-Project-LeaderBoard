// Cấu hình Tailwind
tailwind.config = {
  darkMode: 'class',
  theme: {
      extend: {
          colors: {
              primary: {
                  "50": "#eff6ff",
                  "100": "#dbeafe",
                  "200": "#bfdbfe",
                  "300": "#93c5fd",
                  "400": "#60a5fa",
                  "500": "#3b82f6",
                  "600": "#2563eb",
                  "700": "#1d4ed8",
                  "800": "#1e40af",
                  "900": "#1e3a8a",
                  "950": "#172554"
              }
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
};


let container = document.getElementById('container');
let count = 50;
for(var i = 0; i<50; i++){
    let leftSnow = Math.floor(Math.random() * container.clientWidth);
    let topSnow = Math.floor(Math.random() * container.clientHeight);
    let widthSnow = Math.floor(Math.random() * 50);
    let timeSnow = Math.floor((Math.random() * 5) + 5);
    let blurSnow = Math.floor(Math.random() * 10);
    console.log(leftSnow);
    let div = document.createElement('div');
    div.classList.add('snow');
    div.style.left = leftSnow + 'px';
    div.style.top = topSnow + 'px';
    div.style.width = widthSnow + 'px';
    div.style.height = widthSnow + 'px';
    div.style.animationDuration = timeSnow + 's';
    div.style.filter = "blur(" + blurSnow + "px)";
    container.appendChild(div);
}

  // Xử lý sự kiện hiển thị/ẩn mật khẩu
  const togglePassword = document.getElementById('togglePassword');
  const passwordField = document.getElementById('password');
  
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


document.getElementById('signInBtn').addEventListener('click', async function (event) {
    event.preventDefault(); // Ngăn form gửi yêu cầu mặc định khi nhấn nút đăng nhập
  
    const username = document.getElementById('name').value.trim();
    const password = document.getElementById('password').value.trim();
  
    if (!username || !password) {
        alert("Vui lòng nhập đủ tên đăng nhập và mật khẩu!");
        return;
    }
  
    // URL API đăng nhập
    const loginUrl = "https://sinhvien1.tlu.edu.vn/education/oauth/token";
  
    // Dữ liệu gửi đi
    const loginData = {
        username: username,
        password: password,
        client_id: "education_client",
        grant_type: "password",
        client_secret: "password"
    };
  
    try {
        // Gửi yêu cầu đăng nhập
        const loginResponse = await fetch(loginUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
        });
  
        if (!loginResponse.ok) {
            const errorData = await loginResponse.json();
            alert(`Đăng nhập thất bại: ${errorData.error_description || "Thông tin không chính xác."}`);
            return;
        }
  
        // Lấy token từ phản hồi
        const userInfo = await loginResponse.json();
        const token = userInfo.access_token;
        const displayName = userInfo.display_name || 'Khách'; // Giả sử 'display_name' có trong phản hồi
  
        // Lưu thông tin vào localStorage
        localStorage.setItem('authToken', token);
        localStorage.setItem('display_name', displayName);
  
        // Chuyển hướng tới trang dashboard
        alert("Đăng nhập thành công!");
        window.location.href = '/html/Dashboard.html'; // Đảm bảo có trang Dashboard.html
    } catch (error) {
        console.error("Lỗi khi kết nối API:", error);
        alert("Không thể kết nối với máy chủ. Vui lòng thử lại sau.");
    }
  });
  
