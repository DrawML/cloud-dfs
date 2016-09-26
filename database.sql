CREATE DATABASE `cloud_dfs` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'drawml'@'localhost' IDENTIFIED BY 'password_is_secret';
GRANT ALL PRIVILEGES ON `cloud_dfs`.* TO 'drawml'@'localhost';
FLUSH PRIVILEGES;