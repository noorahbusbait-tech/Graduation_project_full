<?php
include 'db.php';

$error = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    $sql = "SELECT * FROM login WHERE username='$username' AND password='$password'";
    $result = $conn->query($sql);

    if ($result && $result->num_rows > 0) {

        $row = $result->fetch_assoc();
        $user = $row['username'];

        echo "<script>
                localStorage.setItem('NGH_AUTH','true');
                localStorage.setItem('NGH_USER','$user');
                window.location='NGH_dashboard.html';
              </script>";
        exit();

    } else {
        $error = "Invalid credentials. Please try again.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NGH Login</title>

<style>
body{
    margin:0;
    font-family:'Segoe UI', sans-serif;
    background:url('./SANG Hospitals.jpg') no-repeat center center/cover;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

.login-box{
    background:#fff;
    padding:40px;
    border-radius:15px;
    width:350px;
    text-align:center;
    box-shadow:0 10px 25px rgba(0,0,0,0.25);
}

.login-logo{
    width:70px;
    margin-bottom:15px;
}

h1{
    margin:10px 0;
}

input{
    width:100%;
    padding:12px;
    margin:10px 0;
    border:1px solid #ddd;
    border-radius:6px;
}

button{
    width:100%;
    padding:12px;
    background:#1f7a4c;
    color:#fff;
    border:none;
    border-radius:6px;
    cursor:pointer;
}

/* 🔥 زر التسجيل */
.register-btn{
    margin-top:10px;
    background:#ffffff;
    color:#1f7a4c;
    border:1px solid #1f7a4c;
}

/* رابط التسجيل */
.register-link{
    margin-top:12px;
    font-size:14px;
}

.register-link a{
    color:#1f7a4c;
    text-decoration:none;
    font-weight:600;
}

.error{
    color:red;
    margin-top:10px;
}
</style>

</head>

<body>

<div class="login-box">

    <img src="./logo.png" class="login-logo">

    <h1>National Guard Hospital</h1>
    <p>Bed Management Decision Support System</p>

    <form method="POST">

        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>

        <button type="submit">Sign in</button>

    </form>

    <!-- 🔥 زر تسجيل -->
    <button class="register-btn" onclick="alert('Registration coming soon')">
    Create Account
</button>

<div class="register-link">
    Don’t have an account? 
    <a href="#" onclick="alert('Registration coming soon'); return false;">
        Register here
    </a>
</div>

</body>
</html>