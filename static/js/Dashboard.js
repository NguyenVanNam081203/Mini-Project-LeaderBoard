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

    // Lấy token và tên người dùng từ localStorage
    const authToken = localStorage.getItem('authToken');
    const displayName = localStorage.getItem('display_name'); // Không còn giá trị mặc định 'Khách'

    // Kiểm tra nếu không có displayName hoặc authToken thì chuyển hướng về trang đăng nhập
    if (!authToken || !displayName) {
        window.location.href = 'login.html'; // Chuyển hướng về trang đăng nhập nếu không có token hoặc displayName
    }

    // Hiển thị tên người dùng lên giao diện
    document.getElementById('display_name').textContent = displayName;

    // Đăng xuất
    document.getElementById('logoutButton').addEventListener('click', () => {
        localStorage.removeItem('authToken'); // Xóa token xác thực
        localStorage.removeItem('display_name'); // Xóa tên người dùng
        window.location.href = 'login.html'; // Chuyển hướng về trang đăng nhập
    });


