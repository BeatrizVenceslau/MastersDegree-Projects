<?php
    Include 'conn.php';

    $method = $_SERVER['REQUEST_METHOD'];

    if ($method == 'GET') {
        if(isset($_GET['movie_id'])) {
            $movie_id = $_GET['movie_id'];
            $query = "SELECT * FROM movie WHERE id = $movie_id;";
        } else {
            $query = "SELECT * FROM movie;";
        }
    } else {
        exit();
    }
    $result = mysqli_query($conn,$query) or die(mysqli_error($conn));

    header("Content-Type: application/json");
    echo json_encode($result->fetch_all(MYSQLI_ASSOC));
    exit();

?>