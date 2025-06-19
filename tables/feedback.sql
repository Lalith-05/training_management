<<<<<<< HEAD
CREATE TABLE `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `trainer_name` varchar(100) DEFAULT NULL,
  `training_date` date DEFAULT NULL,
  `course_helpful` tinyint(1) DEFAULT NULL,
  `course_rating` int DEFAULT NULL,
  `trainer_rating` int DEFAULT NULL,
  `course_review` text,
  `trainer_review` text,
  `manager_id` int DEFAULT NULL,
  `manager_comments` text,
  `allow_to_continue` enum('yes','no') DEFAULT NULL,
  `submitted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `manager_reviewed` tinyint(1) DEFAULT '0',
  `understood_concepts` text,
  `improvements` text,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `manager_id` (`manager_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`manager_id`) REFERENCES `users` (`id`),
  CONSTRAINT `feedback_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
=======
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    training_date DATE NOT NULL,
    course_helpful TINYINT(1) NOT NULL,
    course_rating INT NOT NULL,
    trainer_name VARCHAR(100) NOT NULL,
    trainer_rating INT NOT NULL,
    course_review TEXT NOT NULL,
    trainer_review TEXT NOT NULL,
    understood_concepts TEXT,
    improvements TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    manager_id INT NOT NULL,
    manager_comments TEXT,
    allow_to_continue TINYINT(1),
    reviewed_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (manager_id) REFERENCES users(id)
);


>>>>>>> 917fe3562ecc75c1e9819a5f372a9db57b143853
