<?php
    $servername = "db.team-13.pt";
    $username = "ticketmaster";
    $password = "popcorn123";
    $dbname = "movies_db";	

    $conn = mysqli_init();
    $conn->real_connect($servername, $username, $password, $dbname);
?>