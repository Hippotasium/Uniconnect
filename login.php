<?php
require 'db.php'; 
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = $_POST['id']; 
    $password = $_POST['password'];

    
    $stmt = $conn->prepare("SELECT * FROM user WHERE id = :id");
    $stmt->bindParam(':id', $id);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && password_verify($password, $user['password'])) {
     
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['role'] = $user['role'];

       
        if ($user['role'] === 'admin') {
            header('Location: dashboard.php');
        } else {
            header('Location: home.html');
        }
        exit();
    } else {
       
        echo "<script>alert('Invalid ID or password'); window.location.href = 'index.php';</script>";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UniConnect - Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: url('imgg.avif');
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #333;
            font-family: 'Poppins', sans-serif;
        }
        .navbar {
            background: rgba(255, 255, 255, 0.9);
            padding: 15px;
            width: 100%;
            position: absolute;
            top: 0;
        }
        .navbar-brand {
            font-weight: bold;
            color: #63afad;
        }
        .navbar-nav .nav-link {
            color: #333;
            font-size: 18px;
            font-weight: 500;
            margin-right: 20px;
        }
        .navbar-nav .nav-link:hover {
            color: #4A90E2;
        }
        .login-container {
            text-align: center;
            background: rgba(255, 255, 255, 0.8);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
            width: 350px;
        }
        .login-container h2 {
            margin-bottom: 20px;
        }
        .login-container input, .login-container button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border: none;
            border-radius: 5px;
        }
        .login-container input {
            border: 1px solid #ccc;
        }
        .login-container button {
            background: #4A90E2;
            color: white;
            cursor: pointer;
        }
        .login-container button:hover {
            background: #357ABD;
        }
        .register-text {
            margin-top: 15px;
            font-size: 14px;
        }
        .register-text a {
            color: #4A90E2;
            text-decoration: none;
            font-weight: bold;
        }
        .register-text a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg shadow-sm">
        <div class="container-fluid">
            <a class="navbar-brand" href="home.html">UniConnect</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="home.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="login-container">
        <h2 id="panel-title">Please log in to your account</h2>
        <form action="login.php" method="POST">
            <input type="text" name="id" placeholder="ID" required> <!-- Changed from email to ID -->
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p class="register-text" id="register-link">Don't have an account? <a href="registration.html">Register</a></p>
    </div>

    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const role = urlParams.get('role');
        const panelTitle = document.getElementById('panel-title');
        const registerLink = document.getElementById('register-link');
        
        if (role) {
            panelTitle.textContent = `Please login to your ${role.charAt(0).toUpperCase() + role.slice(1)} account`;
            
            if (role.toLowerCase() === 'student') {
                registerLink.style.display = 'none';
            }
        }
    </script>
</body>
</html>