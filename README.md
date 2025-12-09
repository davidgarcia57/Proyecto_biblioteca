Markdown<div align="center">

# Sistema de Gestión Bibliotecaria  
### Congreso del Estado de Durango

<img src="https://cdn-icons-png.flaticon.com/512/2232/2232688.png" alt="Logo Biblioteca" width="120"/>

<br>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern_UI-1f1f1f?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-Terminado-brightgreen?style=for-the-badge)

</div>

<br>

### Aplicación de escritorio moderna desarrollada en Python para la administración completa de bibliotecas: catálogo, usuarios, préstamos, reportes en PDF y más.

---

## Tabla de contenidos
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso rápido](#-uso-rápido)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Capturas](#-capturas-de-pantalla)
- [Créditos](#-créditos)

<br>

## Características

| Módulo             | Descripción                                           |
|---------------------|--------------------------------------------------------|
| Control de Acceso   | Login seguro con roles (Administrador / Bibliotecario)    |
| Inventario          | Alta, búsqueda, modificación y baja de libros por pasos |
| Circulación         | Préstamos y devoluciones con validación automática     |
| Usuarios            | Gestión de lectores y registro de visitas              |
| Reportes            | Generación automática de PDFs profesionales            |

<br>

## Tecnologías

- **Interfaz gráfica**: `customtkinter` (diseño moderno tipo dark/light)
- **Base de datos**: `pymysql` + MySQL 8.0
- **Manejo de imágenes**: `Pillow`
- **Reportes PDF**: `reportlab`

<br>

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/proyecto_biblioteca.git
cd proyecto_biblioteca

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install customtkinter pymysql Pillow reportlab

# 4. Configurar la base de datos
#   - Importa el archivo .sql incluido en /database/
#   - Edita src/config/conexion_db.py con tus credenciales:
#       self.password = "TU_CONTRASEÑA_AQUI"

# 5. Ejecutar
python main.py


Uso rápido

Iniciar sesión
Usuario administrador por defecto:
usuario: admin | contraseña: admin123
Usa el menú lateral izquierdo para navegar entre módulos.
Para realizar un préstamo → sección Préstamos → busca libro y lector → confirma.



Estructura del proyecto
textproyecto_biblioteca/
├── main.py                # Punto de entrada
├── src/
│   ├── config/            # Configuración y conexión DB
│   ├── controller/        # Lógica de la aplicación
│   ├── model/             # Consultas SQL
│   ├── view/              # Ventanas e interfaz
│   └── navegador.py       # Sistema de navegación entre pantallas
├── database/              # Script SQL de la base de datos
├── assets/                # Imágenes y recursos (opcional)
└── README.md


Capturas de pantalla

  Login
  Dashboard
  Préstamos
  Reporte PDF

(Cuando tengas las capturas, guárdalas en una carpeta /screenshots y actualiza las rutas)


Créditos
Desarrollado para el H. Congreso del Estado de Durango
© 2025 Todos los derechos reservados.

¡Listo para usar y con muy buena presencia en GitHub!

```