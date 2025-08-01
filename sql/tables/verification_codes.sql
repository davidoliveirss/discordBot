CREATE TABLE verification_codes(
  id INT NOT NULL AUTO_INCREMENT,
  id_user BIGINT NULL,
  code VARCHAR(6) NOT NULL UNIQUE,
  valid TINYINT(1) NOT NULL DEFAULT 1,
  time_created TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  time_expire TIMESTAMP NOT NULL,
  PRIMARY KEY (id),
);
