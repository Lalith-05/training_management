CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(15) NOT NULL,
  `staff_no` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `designation` varchar(5) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('user','manager','admin') NOT NULL,
  `manager_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `staff_no` (`staff_no`),
  UNIQUE KEY `email` (`email`),
  KEY `fk_manager_assignment` (`manager_id`),
  CONSTRAINT `fk_manager_assignment` FOREIGN KEY (`manager_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;