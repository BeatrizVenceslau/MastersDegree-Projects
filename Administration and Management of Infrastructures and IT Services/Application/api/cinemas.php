<?php
    Include 'conn.php';

    $method = $_SERVER['REQUEST_METHOD'];

    if ($method == 'GET') {
        if(isset($_GET['cinema_id'])) {
            $cinema_id = $_GET['cinema_id'];
            $query = "SELECT * FROM cinema WHERE id = $cinema_id;";
        } else {
            $query = "SELECT * FROM cinema;";
        }
    } else {
        exit();
    }
    $result = mysqli_query($conn,$query) or die(mysqli_error($conn));

    header("Content-Type: application/json");
    echo json_encode($result->fetch_all(MYSQLI_ASSOC));
    exit();

?>