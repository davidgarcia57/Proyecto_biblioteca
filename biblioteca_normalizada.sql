-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-12-2025 a las 15:32:52
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
-- Base de datos: `biblioteca_normalizada`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `autores`
--

CREATE TABLE `autores` (
  `id_autor` int(11) NOT NULL,
  `nombre_completo` varchar(200) NOT NULL,
  `tipo` enum('Persona','Corporativo') DEFAULT 'Persona'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `autores`
--

INSERT INTO `autores` (`id_autor`, `nombre_completo`, `tipo`) VALUES
(1, 'Jose madero', 'Persona'),
(2, 'Quijote', 'Persona'),
(3, 'Autor Prueba de eliminación de libros', 'Persona'),
(4, 'Autor prueba de vista', 'Persona'),
(5, 'prueba', 'Persona');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `autores_obras`
--

CREATE TABLE `autores_obras` (
  `id_obra` int(11) NOT NULL,
  `id_autor` int(11) NOT NULL,
  `rol` enum('Autor Principal','Coautor','Traductor','Ilustrador','Editor') DEFAULT 'Autor Principal'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `autores_obras`
--

INSERT INTO `autores_obras` (`id_obra`, `id_autor`, `rol`) VALUES
(1, 1, 'Autor Principal'),
(2, 2, 'Autor Principal'),
(3, 3, 'Autor Principal'),
(4, 4, 'Autor Principal'),
(5, 5, 'Autor Principal');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `editoriales`
--

CREATE TABLE `editoriales` (
  `id_editorial` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `ciudad` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `editoriales`
--

INSERT INTO `editoriales` (`id_editorial`, `nombre`, `ciudad`) VALUES
(1, '', ''),
(2, 'Corp DEMO', 'Uno-dos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ejemplares`
--

CREATE TABLE `ejemplares` (
  `id_ejemplar` int(11) NOT NULL,
  `id_obra` int(11) NOT NULL,
  `numero_copia` varchar(50) DEFAULT 'Copia 1',
  `ubicacion_fisica` varchar(100) DEFAULT 'General' COMMENT 'Ej: Pasillo 3, Estante B',
  `fecha_adquisicion` datetime DEFAULT current_timestamp(),
  `estado` enum('Disponible','Prestado','Reparación','Perdido','Baja') DEFAULT 'Disponible'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ejemplares`
--

INSERT INTO `ejemplares` (`id_ejemplar`, `id_obra`, `numero_copia`, `ubicacion_fisica`, `fecha_adquisicion`, `estado`) VALUES
(1, 1, 'Copia 1', 'General', '2025-11-24 14:48:49', 'Disponible'),
(2, 2, 'Copia 1', 'General', '2025-11-27 10:45:25', 'Prestado'),
(3, 3, 'Copia 1', 'General', '2025-12-02 14:54:45', 'Baja'),
(4, 4, 'Copia 1', 'General', '2025-12-03 00:42:24', 'Disponible'),
(5, 5, 'Copia 1', 'General', '2025-12-04 10:55:07', 'Disponible');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `obras`
--

CREATE TABLE `obras` (
  `id_obra` int(11) NOT NULL,
  `ficha_no` varchar(50) DEFAULT NULL COMMENT 'Para el campo Ficha No.',
  `titulo` varchar(500) NOT NULL,
  `isbn` varchar(20) DEFAULT NULL,
  `id_editorial` int(11) DEFAULT NULL,
  `lugar_publicacion` varchar(100) DEFAULT NULL COMMENT 'Campo 260 Lugar',
  `autor_corporativo` varchar(255) DEFAULT NULL COMMENT 'Campo 110 y 610',
  `asientos_secundarios` text DEFAULT NULL COMMENT 'Campo 700',
  `idioma` varchar(50) DEFAULT 'Español',
  `anio_publicacion` int(4) DEFAULT NULL COMMENT 'Ej: 2023',
  `edicion` varchar(50) DEFAULT NULL COMMENT 'Ej: 2da Edición',
  `clasificacion` varchar(50) DEFAULT NULL,
  `paginas` int(11) DEFAULT NULL COMMENT 'Solo números',
  `dimensiones` varchar(50) DEFAULT NULL COMMENT 'Ej: 20x15 cm',
  `codigo_ilustracion` varchar(255) DEFAULT NULL,
  `serie` varchar(200) DEFAULT NULL COMMENT 'Ej: Harry Potter',
  `tomo` varchar(50) DEFAULT NULL,
  `volumen` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `obras`
--

INSERT INTO `obras` (`id_obra`, `ficha_no`, `titulo`, `isbn`, `id_editorial`, `lugar_publicacion`, `autor_corporativo`, `asientos_secundarios`, `idioma`, `anio_publicacion`, `edicion`, `clasificacion`, `paginas`, `dimensiones`, `codigo_ilustracion`, `serie`, `tomo`, `volumen`, `descripcion`) VALUES
(1, '1', 'Cuentos de terror', '', 1, '', '', '', 'SPA', 0, '', 'accion', 0, '', 'A,C,D', '', '', '', ''),
(2, '1545', 'Cuento', '54', 1, '', '', '', 'Español', 0, '', '789', 0, '', 'X', '', '', '', ''),
(3, '1001', 'Libro de eliminación', '1002', 2, 'Uno-dos', 'Corp', 'Lorem lipsum', 'Español', 2, 'Uno', 'PG18', 300, '30 x 50', 'X', 'Serie dos de tres DEMOS', '', '', 'En gran stadium'),
(4, '12152', 'Vista 1', '4684', 1, '', '', '', 'Español', 0, '', 'PG 16', 0, '', 'A', '', '', '', ''),
(5, '456', 'libro 1', '', 1, '', '', '', 'Español', 0, '', 'PG18', 0, '', '', '', '', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos`
--

CREATE TABLE `prestamos` (
  `id_prestamo` int(11) NOT NULL,
  `id_prestatario` int(11) NOT NULL,
  `id_usuario_sistema` int(11) NOT NULL,
  `fecha_prestamo` datetime DEFAULT current_timestamp(),
  `fecha_devolucion_esperada` date NOT NULL,
  `fecha_devolucion_real` datetime DEFAULT NULL,
  `estado` enum('Activo','Finalizado','Vencido') DEFAULT 'Activo',
  `id_ejemplar` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `prestamos`
--

INSERT INTO `prestamos` (`id_prestamo`, `id_prestatario`, `id_usuario_sistema`, `fecha_prestamo`, `fecha_devolucion_esperada`, `fecha_devolucion_real`, `estado`, `id_ejemplar`) VALUES
(1, 1, 1, '2025-12-02 13:02:43', '2025-12-09', NULL, 'Activo', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitantes`
--

CREATE TABLE `solicitantes` (
  `id_prestatario` int(11) NOT NULL,
  `nombre_completo` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `solicitantes`
--

INSERT INTO `solicitantes` (`id_prestatario`, `nombre_completo`, `telefono`, `email`, `direccion`, `fecha_registro`) VALUES
(1, 'juaquin torres', '1234567899', 'asteriscouno@gmail.pilin', 'nazas', '2025-12-02 13:02:18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_sistema`
--

CREATE TABLE `usuarios_sistema` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` enum('Admin','Bibliotecario') DEFAULT 'Bibliotecario',
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios_sistema`
--

INSERT INTO `usuarios_sistema` (`id_usuario`, `nombre`, `usuario`, `password_hash`, `rol`, `activo`) VALUES
(1, 'Administrador', 'admin', '12345', 'Admin', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `autores`
--
ALTER TABLE `autores`
  ADD PRIMARY KEY (`id_autor`);

--
-- Indices de la tabla `autores_obras`
--
ALTER TABLE `autores_obras`
  ADD PRIMARY KEY (`id_obra`,`id_autor`),
  ADD KEY `fk_ao_autor` (`id_autor`);

--
-- Indices de la tabla `editoriales`
--
ALTER TABLE `editoriales`
  ADD PRIMARY KEY (`id_editorial`);

--
-- Indices de la tabla `ejemplares`
--
ALTER TABLE `ejemplares`
  ADD PRIMARY KEY (`id_ejemplar`),
  ADD KEY `idx_obra` (`id_obra`);

--
-- Indices de la tabla `obras`
--
ALTER TABLE `obras`
  ADD PRIMARY KEY (`id_obra`),
  ADD KEY `idx_obra_editorial` (`id_editorial`);

--
-- Indices de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD PRIMARY KEY (`id_prestamo`),
  ADD KEY `idx_prestamo_lector` (`id_prestatario`),
  ADD KEY `fk_pres_user` (`id_usuario_sistema`),
  ADD KEY `fk_pres_ejemplar` (`id_ejemplar`);

--
-- Indices de la tabla `solicitantes`
--
ALTER TABLE `solicitantes`
  ADD PRIMARY KEY (`id_prestatario`);

--
-- Indices de la tabla `usuarios_sistema`
--
ALTER TABLE `usuarios_sistema`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `autores`
--
ALTER TABLE `autores`
  MODIFY `id_autor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `editoriales`
--
ALTER TABLE `editoriales`
  MODIFY `id_editorial` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `ejemplares`
--
ALTER TABLE `ejemplares`
  MODIFY `id_ejemplar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `obras`
--
ALTER TABLE `obras`
  MODIFY `id_obra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  MODIFY `id_prestamo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `solicitantes`
--
ALTER TABLE `solicitantes`
  MODIFY `id_prestatario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios_sistema`
--
ALTER TABLE `usuarios_sistema`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `autores_obras`
--
ALTER TABLE `autores_obras`
  ADD CONSTRAINT `fk_ao_autor` FOREIGN KEY (`id_autor`) REFERENCES `autores` (`id_autor`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_ao_obra` FOREIGN KEY (`id_obra`) REFERENCES `obras` (`id_obra`) ON DELETE CASCADE;

--
-- Filtros para la tabla `ejemplares`
--
ALTER TABLE `ejemplares`
  ADD CONSTRAINT `fk_ejemplar_obra` FOREIGN KEY (`id_obra`) REFERENCES `obras` (`id_obra`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `obras`
--
ALTER TABLE `obras`
  ADD CONSTRAINT `fk_obra_editorial` FOREIGN KEY (`id_editorial`) REFERENCES `editoriales` (`id_editorial`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD CONSTRAINT `fk_pres_ejemplar` FOREIGN KEY (`id_ejemplar`) REFERENCES `ejemplares` (`id_ejemplar`),
  ADD CONSTRAINT `fk_pres_lector` FOREIGN KEY (`id_prestatario`) REFERENCES `solicitantes` (`id_prestatario`),
  ADD CONSTRAINT `fk_pres_user` FOREIGN KEY (`id_usuario_sistema`) REFERENCES `usuarios_sistema` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
