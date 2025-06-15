DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(15) NOT NULL,
  `staff_no` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `designation` varchar(5) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('user','manager') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `staff_no` (`staff_no`),
  UNIQUE KEY `email` (`email`)
)ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
