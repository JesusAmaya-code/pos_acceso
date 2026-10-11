# Sistema POS: Control de acceso y base de datos

Proyecto escolar que simula el control de acceso a un sistema de punto de venta (POS) con Python y Flask, e incluye el script de la base de datos en MySQL/MariaDB.

## Características

- Inicio de sesión con contraseñas cifradas (hash)
- Control de acceso por roles: administrador, supervisor y cajero
- Protección de rutas (error 403 si el rol no tiene permiso)
- Bloqueo temporal tras 3 intentos fallidos
- Bitácora de accesos

## Requisitos

- Python 3.10 o superior
- MySQL o MariaDB

## Cómo ejecutar la aplicación

1. Crear y activar el entorno virtual:

```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
```

2. Instalar dependencias:

```bash
   pip install -r requirements.txt
```

3. Ejecutar:

```bash
   python app.py
```

4. Abrir `http://127.0.0.1:5000` en el navegador.

## Usuarios de prueba

| Usuario    | Contraseña | Rol           |
|------------|------------|---------------|
| admin      | admin123   | administrador |
| supervisor | super123   | supervisor    |
| cajero     | caja123    | cajero        |

## Base de datos

El script `database/pos.sql` crea la base de datos `pos` con las tablas `productos`, `usuarios` y `clientes`, cada una con 6 campos y 5 registros de ejemplo.

Para crearla:

```bash
mysql -u root -p < database/pos.sql
```

Para verificarla:

```sql
USE pos;
SHOW TABLES;
SELECT COUNT(*) FROM productos;
```

> El script incluye `DROP DATABASE IF EXISTS pos;`, por lo que reemplaza la base `pos` si ya existe.

## Estructura del proyecto

```
pos_acceso/
├── app.py
├── requirements.txt
├── database/
│   └── pos.sql
├── static/
│   └── style.css
└── templates/
    └── (plantillas HTML)
```

## Autor

Tu Nombre