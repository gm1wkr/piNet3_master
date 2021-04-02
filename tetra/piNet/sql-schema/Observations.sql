-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 23, 2020 at 12:26 PM
-- Server version: 5.6.47-cll-lve
-- PHP Version: 7.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wxObs`
--

-- --------------------------------------------------------

--
-- Table structure for table `Observations`
--

CREATE TABLE `Observations` (
  `id` int(6) NOT NULL,
  `station_id` int(4) NOT NULL,
  `apiUser` varchar(80) NOT NULL,
  `ts` int(11) DEFAULT NULL,
  `delay` int(3) DEFAULT NULL,
  `inHumidity` float DEFAULT NULL,
  `inTemp` float DEFAULT NULL,
  `outHumidity` float DEFAULT NULL,
  `outTemp` float DEFAULT NULL,
  `pressure` float DEFAULT NULL,
  `ptr` int(4) DEFAULT NULL,
  `radiation` float DEFAULT NULL,
  `rain` float(4,2) DEFAULT NULL,
  `rainTotal` float(5,3) DEFAULT NULL,
  `rxCheckPercent` float DEFAULT NULL,
  `status` float DEFAULT NULL,
  `usUnits` float DEFAULT NULL,
  `windDir` float DEFAULT NULL,
  `windGust` float DEFAULT NULL,
  `windSpeed` float DEFAULT NULL,
  `UV` float DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Observations`
--
ALTER TABLE `Observations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `station_id` (`station_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Observations`
--
ALTER TABLE `Observations`
  MODIFY `id` int(6) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
