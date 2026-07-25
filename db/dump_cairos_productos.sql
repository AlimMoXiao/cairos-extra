-- Cairos - dump parcial de la base de datos
-- Solo tablas de productos y promocioness
-- NO contiene: usuarios, bodegas, ordenes, entregas, empleados ni datos personales
-- Generado automaticamente. Ejecutar scripts/dump_productos.py para actualizacion.

-- =====================================================
-- producto
-- catalogo de productos disponibles
-- =====================================================
CREATE TABLE IF NOT EXISTS producto (
  id           INT PRIMARY KEY AUTO_INCREMENT,
  nombre       VARCHAR(255)   NOT NULL,
  descripcion  TEXT,
  marca        VARCHAR(100),
  categoria    VARCHAR(100),
  status       ENUM('activo','inactivo','oculto') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- INSERT INTO producto ... ;  -- ejecutar scripts/dump_productos.py

-- =====================================================
-- precioProducto
-- historial de precios por producto (fechaActualizacion es la clave)
-- =====================================================
CREATE TABLE IF NOT EXISTS precioProducto (
  idProducto          INT NOT NULL,
  precioBase          DECIMAL(10,2),
  precioVenta         DECIMAL(10,2),
  precioSugerido      DECIMAL(10,2),
  fechaActualizacion  DATETIME NOT NULL,
  PRIMARY KEY (idProducto, fechaActualizacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- INSERT INTO precioProducto ... ;

-- =====================================================
-- almacen
-- stock disponible por producto y almacen
-- (solo se vuelca la estructura; cantidades no se incluyen en el dump)
-- =====================================================
CREATE TABLE IF NOT EXISTS almacen (
  idProducto  INT NOT NULL,
  nombre      VARCHAR(100) NOT NULL,
  cantidad    INT DEFAULT 0,
  PRIMARY KEY (idProducto, nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- INSERT INTO almacen ... ;

-- =====================================================
-- promocion
-- cabecera de promociones activas
-- =====================================================
CREATE TABLE IF NOT EXISTS promocion (
  id        INT PRIMARY KEY AUTO_INCREMENT,
  nombre    VARCHAR(255) NOT NULL,
  descripcion TEXT,
  estatus   ENUM('activa','inactiva') DEFAULT 'activa'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- INSERT INTO promocion ... ;

-- =====================================================
-- promocionPorcentual
-- promo de descuento porcentual sobre un producto trigger
-- =====================================================
CREATE TABLE IF NOT EXISTS promocionPorcentual (
  idpromocion      INT NOT NULL,
  idProducto       INT NOT NULL,
  cantidad         INT NOT NULL DEFAULT 1,
  porcentajeDescuento DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (idpromocion, idProducto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- INSERT INTO promocionPorcentual ... ;

-- =====================================================
-- promocionBogo
-- compra N unidades de un producto y lleva M de otro gratis
-- tipo = 'compra' o 'regalo'
-- =====================================================
CREATE TABLE IF NOT EXISTS promocionBogo (
  idPromocion  INT NOT NULL,
  idProducto   INT NOT NULL,
  cantidad     INT NOT NULL DEFAULT 1,
  tipo         ENUM('compra','regalo') NOT NULL,
  PRIMARY KEY (idPromocion, idProducto, tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- INSERT INTO promocionBogo ... ;
