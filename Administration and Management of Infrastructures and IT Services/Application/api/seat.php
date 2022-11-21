<?php
    Include 'conn.php';

    $method = $_SERVER['REQUEST_METHOD'];

    if ($method == 'GET') {
        $available = False;
        if(isset($_GET['available'])){
            $available = True;
        }
        if(isset($_GET['seat_id'])) {
            $seat_id = $_GET['seat_id'];
            $query = "SELECT * FROM seat WHERE id = $seat_id;";
        } else if(isset($_GET['showtime_id'])) {
            $showtime_id = $_GET['showtime_id'];
            if($available){
                $query = "SELECT room_seats.* FROM (SELECT seat.* FROM (SELECT cinema_id, room_id, showtime FROM showtime WHERE showtime.id=$showtime_id) crs JOIN seat WHERE seat.cinema_id=crs.cinema_id AND seat.room=crs.room_id) room_seats LEFT JOIN ticket ON room_seats.id=ticket.seat_id AND ticket.showtime_id = $showtime_id WHERE ticket.id IS NULL;";
            } else {
                $query = "SELECT seat.* FROM (SELECT cinema_id, room_id, showtime FROM showtime WHERE showtime.id=$showtime_id) crs JOIN seat WHERE seat.cinema_id=crs.cinema_id AND seat.room=crs.room_id;";
            }
        } else {
            $query = "SELECT * FROM seat;";
        }
    } else {
        exit();
    }
    $result = mysqli_query($conn,$query) or die(mysqli_error($conn));

    header("Content-Type: application/json");
    echo json_encode($result->fetch_all(MYSQLI_ASSOC));
    exit();

?>