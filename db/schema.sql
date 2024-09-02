CREATE TABLE `companies` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL
);

CREATE TABLE `profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `img_url` VARCHAR(400) NOT NULL, dasdsa
    `name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `tel` VARCHAR(20) NOT NULL,
    `rank` VARCHAR(100) NOT NULL,
    `address` VARCHAR(500),
    `birthday` DATE,
    `web_site` VARCHAR(400),
    `memo` TEXT,
    `company_id` INT,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`) ON DELETE SET NULL
);

CREATE TABLE `labels` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL,
    `profile_id` INT NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    FOREIGN KEY (`profile_id`) REFERENCES `profiles` (`id`) ON DELETE CASCADE
);