<?php
    Include 'conn.php';

    $method = $_SERVER['REQUEST_METHOD'];

    if ($method == 'GET') {
        if(isset($_GET['ticket_id'])) {
            $ticket_id = $_GET['ticket_id'];
            $query = "SELECT * FROM ticket WHERE id = $ticket;";
        } else if(isset($_GET['showtime_id'])) {
            $showtime_id = $_GET['showtime_id'];
            $query = "SELECT * FROM ticket WHERE showtime_id = $showtime_id;";
        } else {
            $query = "SELECT * FROM ticket;";
        }
    } else if($method == 'POST') {
        $showtime_id = $_POST['showtime_id'];
        $seat_id = $_POST['seat_id'];
        $query = "INSERT INTO ticket (showtime_id, seat_id) VALUES ($showtime_id, $seat_id);";
    } else {
        exit();
    }
    if($method == 'GET') {
        $result = mysqli_query($conn,$query) or die(mysqli_error($conn));
        header("Content-Type: application/json");
        echo json_encode($result->fetch_all(MYSQLI_ASSOC));
        exit();
    }
    if($method == 'POST') {
        mysqli_query($conn,$query) or die(mysqli_error($conn));
    }
?>