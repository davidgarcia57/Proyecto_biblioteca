Sistema de Gestión Bibliotecaria - Congreso de Durango

Este proyecto es una aplicación de escritorio desarrollada en Python para la administración integral de una biblioteca. Permite gestionar el catálogo de libros, préstamos, usuarios, visitas y generar reportes en PDF.

📋 Características Principales

Control de Acceso: Login seguro con roles (Administrador/Bibliotecario).

Inventario: Registro de libros por pasos, búsqueda avanzada y baja de ejemplares.

Circulación: Préstamos y devoluciones con validación de disponibilidad y límites por usuario.

Usuarios y Visitas: Gestión de lectores y registro de afluencia diaria.

Reportes: Generación automática de PDFs (Inventario, Préstamos, Visitas, Bajas).

🛠️ Requisitos Previos

Necesitas tener instalado Python 3.x y un servidor MySQL (o MariaDB).

Librerías necesarias

Ejecuta el siguiente comando para instalar las dependencias:

pip install customtkinter pymysql Pillow reportlab


⚙️ Configuración

Base de Datos:

Asegúrate de tener tu servidor MySQL corriendo.

Importa el esquema de la base de datos biblioteca_normalizada.

Verifica las credenciales en src/config/conexion_db.py:

self.host = "localhost"
self.user = "root"
self.password = ""  # Tu contraseña
self.database = "biblioteca_normalizada"


Ejecución:
Desde la raíz del proyecto, ejecuta:

python main.py


🚀 Uso Rápido

Iniciar Sesión: Usa las credenciales de administrador (deben estar pre-cargadas en la BD).

Navegación: Usa el menú lateral para acceder a las secciones.

Flujo Típico de Préstamo:

Ve a Préstamos.

Ingresa el ID del Libro y del Lector (o usa la lupa 🔍 para buscar).

Selecciona los días y confirma.

📂 Estructura del Proyecto

proyecto_biblioteca/
├── src/
│   ├── config/       # Conexión a BD
│   ├── controller/   # Lógica de negocio
│   ├── model/        # Datos y consultas SQL
│   ├── view/         # Interfaz gráfica (CustomTkinter)
│   └── navegador.py  # Router de pantallas
├── main.py           # Punto de entrada
└── README.md


📄 Licencia

Este proyecto es de uso exclusivo para el Congreso del Estado de Durango.
