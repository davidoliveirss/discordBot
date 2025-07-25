CREATE TABLE license_keys(
  id INT NOT NULL AUTO_INCREMENT,
  id_user BIGINT NULL,
  code VARCHAR(14) NOT NULL UNIQUE,
  valid TINYINT(1) NOT NULL DEFAULT 0, --0 sendo codigo banido/nao ativo
  time_created TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  time_expire TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);