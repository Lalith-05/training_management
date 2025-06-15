DROP TABLE IF EXISTS `course_selection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_selection` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `manager_id` int DEFAULT NULL,
  `status` varchar(20) DEFAULT 'pending',
  `rejection_reason` text,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `course_selection_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `course_selection_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE,
  CONSTRAINT `course_selection_ibfk_3` FOREIGN KEY (`manager_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
