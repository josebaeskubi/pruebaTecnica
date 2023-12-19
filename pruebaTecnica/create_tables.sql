CREATE TABLE `Route` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	`star` TEXT NOT NULL,
	`cruiseLevel` INT NOT NULL,
	`cruiseMach` FLOAT NOT NULL,
	`tow` INT NOT NULL,
	`deltaIsa` FLOAT NOT NULL,
	`tripFuel` INT NOT NULL,
	`tripDistance` INT NOT NULL,
	`fpl` TEXT NOT NULL,
	`depAirportID` INT NOT NULL,
	`arrAirportID` INT NOT NULL,
	`date` DATETIME NOT NULL,
	`aircraftID` INT NOT NULL,
	`airlineID` INT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Airports` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`info` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Waypoints` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Route-Waypoints` (
	`routePointID` INT NOT NULL AUTO_INCREMENT,
	`routeID` INT NOT NULL,
	`waypointID` INT NOT NULL,
	`eet1` INT NOT NULL,
	`eet2` INT NOT NULL,
	`eet3` INT NOT NULL,
	`eet4` INT NOT NULL,
	`flightLevel` INT,
	`track` INT NOT NULL,
	`windDir` INT NOT NULL,
	`windSpeed` INT NOT NULL,
	`oat` INT,
	`mach` FLOAT,
	`latitude` FLOAT NOT NULL,
	`longitude` FLOAT NOT NULL,
	PRIMARY KEY (`routePointID`)
);

CREATE TABLE `Airlines` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`info` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Aircrafts` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`info` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `Route` ADD CONSTRAINT `FK_depAirport` FOREIGN KEY (`depAirportID`) REFERENCES `Airports`(`id`);

ALTER TABLE `Route` ADD CONSTRAINT `FK_arrAirport` FOREIGN KEY (`arrAirportID`) REFERENCES `Airports`(`id`);

ALTER TABLE `Route` ADD CONSTRAINT `FK_aircraft` FOREIGN KEY (`aircraftID`) REFERENCES `Aircrafts`(`id`);

ALTER TABLE `Route` ADD CONSTRAINT `FK_airline` FOREIGN KEY (`airlineID`) REFERENCES `Airlines`(`id`);

ALTER TABLE `Route-Waypoints` ADD CONSTRAINT `FK_route` FOREIGN KEY (`routeID`) REFERENCES `Route`(`id`);

ALTER TABLE `Route-Waypoints` ADD CONSTRAINT `FK_waypoint` FOREIGN KEY (`waypointID`) REFERENCES `Waypoints`(`id`);





