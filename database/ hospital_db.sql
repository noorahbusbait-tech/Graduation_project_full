-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 25, 2026 at 01:54 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hospital_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `mrn` int(11) NOT NULL,
  `patient_name` varchar(120) DEFAULT NULL,
  `diagnosis` varchar(150) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`mrn`, `patient_name`, `diagnosis`, `status`) VALUES
(1001, 'محمد القحطاني', 'Pneumonia', 'Discharged'),
(1002, 'أحمد الغامدي', 'Diabetes', 'D1'),
(1003, 'عبدالله الحربي', 'Hypertension', 'ER'),
(1004, 'خالد العتيبي', 'Asthma', 'Critical'),
(1005, 'سعد الدوسري', 'COVID-19', 'ER'),
(1006, 'ناصر الزهراني', 'Kidney Stones', 'Discharged'),
(1007, 'فهد الشمري', 'Heart Disease', 'ICU'),
(1008, 'يوسف العنزي', 'Fracture', 'Surgery'),
(1009, 'عبدالرحمن المطيري', 'Anemia', 'Stable'),
(1010, 'تركي القحطاني', 'Migraine', 'Discharged');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `role` varchar(20) DEFAULT 'staff'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `full_name`, `password`, `role`) VALUES
(1, 'sara', 'سارة', '1234', 'admin'),
(2, 'raghad', 'رغد', '1234', 'staff'),
(3, 'walaa', 'ولاء', '1234', 'staff'),
(4, 'fatimah', 'فاطمه', '1234', 'staff'),
(5, 'noura', 'نوره', '1234', 'staff'),
(6, 'amal', 'امل', '1234', 'staff'),
(7, 'rana', 'رنا', '1234', 'staff'),
(8, 'shahd', 'شهد', '1234', 'staff'),
(9, 'dana', 'دانه', '1234', 'staff'),
(10, 'maram', 'مرام', '1234', 'staff');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`mrn`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
