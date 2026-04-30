-- phpMyAdmin SQL Dump
-- Database: `gate_pass`

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Table structure for table `student_register`
--

CREATE TABLE IF NOT EXISTS `student_register` (
  `stud_id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `address` text NOT NULL,
  `phone` varchar(15) NOT NULL,
  `course_name` varchar(100) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`stud_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `staff_register`
--

CREATE TABLE IF NOT EXISTS `staff_register` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `staff_type` varchar(50) NOT NULL,
  `designation` varchar(100) NOT NULL,
  `experience` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `staff_image` varchar(255) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `status` varchar(50) DEFAULT 'Active',
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `gate_pass_details`
--

CREATE TABLE IF NOT EXISTS `gate_pass_details` (
  `request_detail_id` int(11) NOT NULL AUTO_INCREMENT,
  `stud_id` varchar(50) DEFAULT NULL,
  `roll_no` varchar(50) NOT NULL,
  `reason` text NOT NULL,
  `out_time` datetime DEFAULT NULL,
  `in_time` datetime DEFAULT NULL,
  `request_date` datetime NOT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  PRIMARY KEY (`request_detail_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `gate_pass_history`
--

CREATE TABLE IF NOT EXISTS `gate_pass_history` (
  `gate_pass_history_id` int(11) NOT NULL AUTO_INCREMENT,
  `stud_id` varchar(50) NOT NULL,
  `passing_date` date NOT NULL,
  `passing_time` time NOT NULL,
  `auth_status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`gate_pass_history_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `nfc_tags`
--

CREATE TABLE IF NOT EXISTS `nfc_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_uid` varchar(100) NOT NULL,
  `stud_id` varchar(50) NOT NULL,
  `assigned_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag_uid` (`tag_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
