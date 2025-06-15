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


