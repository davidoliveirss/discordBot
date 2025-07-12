CREATE TABLE suport_requests(
  id INT NOT NULL AUTO_INCREMENT,
  id_user BIGINT NOT NULL,
  description TEXT NOT NULL,
  time_sent TIMESTAMP NOT NULL,
  status ENUM('pending','in_progress','resolved') DEFAULT 'pending',
  PRIMARY KEY (id)
);