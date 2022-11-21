<?php
    Include 'conn.php';

    $method = $_SERVER['REQUEST_METHOD'];

    if ($method == 'GET') {
        if(isset($_GET['showtime_id'])){
            $showtime_id = $_GET['showtime_id'];
            $query = "SELECT * FROM showtime WHERE id = $showtime_id;";
        } else if(isset($_GET['cinema_id']) && isset($_GET['movie_id'])){
            $cinema_id = $_GET['cinema_id'];
            $movie_id = $_GET['movie_id'];
            $query = "SELECT * FROM showtime WHERE cinema_id = $cinema_id AND movie_id = $movie_id;";
        } else if(isset($_GET['cinema_id'])){
            $cinema_id = $_GET['cinema_id'];
            $query = "SELECT * FROM showtime WHERE cinema_id = $cinema_id;";
        } else if(isset($_GET['movie_id'])){
            $movie_id = $_GET['movie_id'];
            $query = "SELECT * FROM showtime WHERE movie_id = $movie_id;";
        } else {
            $query = "SELECT * FROM showtime;";
        }
    } else {
        exit();
    }
    $result = mysqli_query($conn,$query) or die(mysqli_error($conn));

    header("Content-Type: application/json");
    echo json_encode($result->fetch_all(MYSQLI_ASSOC));
    exit();

?>