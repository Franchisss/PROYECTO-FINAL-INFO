-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3307
-- Tiempo de generación: 27-06-2025 a las 05:59:18
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto3`
--
CREATE DATABASE IF NOT EXISTS `proyecto3` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `proyecto3`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_varios`
--

CREATE TABLE `archivos_varios` (
  `id` int(11) NOT NULL,
  `tipo_archivo` enum('csv','mat','jpg','png') NOT NULL,
  `nombre_archivo` varchar(200) NOT NULL,
  `ruta_archivo` text NOT NULL,
  `fecha_subida` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dicom_nifti`
--

CREATE TABLE `dicom_nifti` (
  `id` int(11) NOT NULL,
  `nombre_paciente` varchar(200) NOT NULL,
  `identificacion` varchar(100) NOT NULL,
  `edad` int(11) NOT NULL,
  `sexo` varchar(10) NOT NULL,
  `ruta_dicom` text NOT NULL,
  `ruta_nifti` text NOT NULL,
  `fecha_subida` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre_usuario` varchar(200) NOT NULL,
  `contraseña` varchar(200) NOT NULL,
  `rol` enum('imagenes','señales') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `archivos_varios`
--
ALTER TABLE `archivos_varios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `dicom_nifti`
--
ALTER TABLE `dicom_nifti`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre_usuario` (`nombre_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `archivos_varios`
--
ALTER TABLE `archivos_varios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `dicom_nifti`
--
ALTER TABLE `dicom_nifti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
