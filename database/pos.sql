-- ============================================
-- Base de datos: POS (Punto de Venta)
-- Tablas: productos, usuarios, clientes
-- ============================================

DROP DATABASE IF EXISTS pos;
CREATE DATABASE pos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pos;

-- --------------------------------------------
-- Tabla: productos
-- --------------------------------------------
CREATE TABLE productos (
    id_producto   INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100)  NOT NULL,
    categoria     VARCHAR(50)   NOT NULL,
    precio        DECIMAL(10,2) NOT NULL,
    stock         INT           NOT NULL DEFAULT 0,
    fecha_alta    DATE          NOT NULL
);

-- --------------------------------------------
-- Tabla: usuarios
-- --------------------------------------------
CREATE TABLE usuarios (
    id_usuario     INT AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(30)  NOT NULL UNIQUE,
    nombre         VARCHAR(100) NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,
    rol            ENUM('administrador','supervisor','cajero') NOT NULL,
    activo         BOOLEAN      NOT NULL DEFAULT TRUE
);

-- --------------------------------------------
-- Tabla: clientes
-- --------------------------------------------
CREATE TABLE clientes (
    id_cliente      INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    telefono        VARCHAR(15),
    email           VARCHAR(100),
    direccion       VARCHAR(150),
    fecha_registro  DATE NOT NULL
);

-- --------------------------------------------
-- Datos: productos
-- --------------------------------------------
INSERT INTO productos (nombre, categoria, precio, stock, fecha_alta) VALUES
('Coca-Cola 600 ml',      'Bebidas',    18.00, 120, '2026-01-10'),
('Sabritas Original 45 g','Botanas',    19.50,  80, '2026-01-10'),
('Pan blanco Bimbo',      'Panadería',  42.00,  35, '2026-01-12'),
('Leche Lala 1 L',        'Lácteos',    26.50,  60, '2026-01-15'),
('Jabón Zote 400 g',      'Limpieza',   22.00,  45, '2026-01-20');

-- --------------------------------------------
-- Datos: usuarios
-- (los hashes son de ejemplo; en el sistema real se generan con werkzeug)
-- --------------------------------------------
INSERT INTO usuarios (username, nombre, password_hash, rol, activo) VALUES
('admin',      'Ana Torres',   'hash_ejemplo_admin123',  'administrador', TRUE),
('supervisor', 'Luis Pérez',   'hash_ejemplo_super123',  'supervisor',    TRUE),
('cajero',     'María López',  'hash_ejemplo_caja123',   'cajero',        TRUE),
('cajero2',    'Carlos Ruiz',  'hash_ejemplo_caja456',   'cajero',        TRUE),
('cajero3',    'Sofía Medina', 'hash_ejemplo_caja789',   'cajero',        FALSE);

-- --------------------------------------------
-- Datos: clientes
-- --------------------------------------------
INSERT INTO clientes (nombre, telefono, email, direccion, fecha_registro) VALUES
('Juan Hernández',  '6621234567', 'juan.hernandez@correo.com', 'Blvd. Kino 120, Hermosillo',     '2026-02-01'),
('Laura Gómez',     '6629876543', 'laura.gomez@correo.com',    'Calle Serdán 45, Hermosillo',    '2026-02-03'),
('Pedro Ramírez',   '6625551122', 'pedro.ramirez@correo.com',  'Av. Rosales 300, Hermosillo',    '2026-02-10'),
('Daniela Castro',  '6623334455', 'daniela.castro@correo.com', 'Col. Modelo 78, Hermosillo',     '2026-02-14'),
('Roberto Salazar', '6627778899', 'roberto.salazar@correo.com','Calle Reforma 210, Hermosillo',  '2026-02-20');

-- --------------------------------------------
-- Consultas de verificación
-- --------------------------------------------
SELECT * FROM productos;
SELECT * FROM usuarios;
SELECT * FROM clientes;