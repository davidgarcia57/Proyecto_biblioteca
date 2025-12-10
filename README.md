Markdown<div align="center">

# Sistema de Gestión Bibliotecaria  
### Congreso del Estado de Durango

<img src="src/resources/logo.png" width="120"/>

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
- [Estructura del proyecto](#-estructura-del-proyecto)

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

## Estructura del proyecto

```text
proyecto_biblioteca/
├── src/
│   ├── config/          # Configuración y conexión DB
│   ├── controller/      # Lógica de la aplicación
│   ├── model/           # Consultas SQL
│   ├── view/            # Ventanas e interfaz
│   └── navegador.py     # Sistema de navegación entre pantallas
├── database/            # Script SQL de la base de datos
├── assets/              # Imágenes y recursos (opcional)
├── main.py              # Punto de entrada
└── README.md
```

<div align="center">

Créditos Desarrollado para el H. Congreso del Estado de Durango

© 2025 Todos los derechos reservados.

</div>
