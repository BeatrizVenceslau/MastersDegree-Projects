DROP TABLE IF EXISTS `ticket`;
DROP TABLE IF EXISTS `showtime`;
DROP TABLE IF EXISTS `seat`;
DROP TABLE IF EXISTS `cinema`;
DROP TABLE IF EXISTS `movie`;

CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `release_date` date NOT NULL,
  `ticket_price` decimal(10,2) NOT NULL,
  `poster` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `cinema` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `address` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `zip` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `seat` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `cinema_id` int(11) NOT NULL,
    `room` int(11) NOT NULL DEFAULT 1,
    `seat_row` varchar(2) NOT NULL,
    `seat_number` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`cinema_id`) REFERENCES `cinema` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `showtime` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `movie_id` int(11) NOT NULL,
    `cinema_id` int(11) NOT NULL,
    `room_id` int(11) NOT NULL DEFAULT 1,
    `showtime` datetime NOT NULL,
    PRIMARY KEY (`id`),
    KEY `movie_id` (`movie_id`),
    KEY `cinema_id` (`cinema_id`),
    CONSTRAINT `showtime_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
    CONSTRAINT `showtime_ibfk_2` FOREIGN KEY (`cinema_id`) REFERENCES `cinema` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `ticket` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `showtime_id` int(11) NOT NULL,
    `seat_id` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `showtime_id` (`showtime_id`),
    KEY `seat_id` (`seat_id`),
    CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`showtime_id`) REFERENCES `showtime` (`id`),
    CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`seat_id`) REFERENCES `seat` (`id`),
    CONSTRAINT `ticket_ibfk_3` UNIQUE (`showtime_id`, `seat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
