<!-- HEADER CENTRADO --><div align="center"><!-- Puedes reemplazar este link con tu propio logo si tienes uno --><img src="https://www.google.com/search?q=https://cdn-icons-png.flaticon.com/512/2232/2232688.png" alt="Logo Biblioteca" width="100" height="100"><h1 align="center">Sistema de Gestión Bibliotecaria</h1><p align="center"><strong>Congreso del Estado de Durango</strong></p><!-- BADGES CENTRADOS --><p align="center"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Versi%C3%B3n-1.0.0-blue%3Fstyle%3Dfor-the-badge%26logo%3Dappveyor" alt="Version"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Estado-Terminado-success%3Fstyle%3Dfor-the-badge%26logo%3Dappveyor" alt="Estado"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Licencia-Privada-red%3Fstyle%3Dfor-the-badge" alt="Licencia"></p></div><!-- DESCRIPCIÓN CON ESTILO -->💡 Descripción: Aplicación de escritorio moderna desarrollada en Python para la administración integral de flujos de trabajo bibliotecarios. Gestiona catálogo, usuarios y préstamos con una interfaz intuitiva y reportes profesionales.<!-- TABLA DE CONTENIDOS -->📑 Tabla de Contenidos✨ Características🛠️ Tecnologías⚙️ Instalación🚀 Uso📂 Estructura📸 Capturas✨ CaracterísticasMóduloDescripción🔐 Control de AccesoSistema de login seguro con roles diferenciados (Admin/Bibliotecario).📚 InventarioRegistro guiado por pasos, búsqueda en tiempo real y bajas controladas.🔄 CirculaciónGestión de préstamos y devoluciones con validación automática de stock.👥 UsuariosAdministración de lectores y control de afluencia (visitas) diaria.📄 Reportes PDFGeneración automática de reportes de inventario, préstamos y bajas.🛠️ TecnologíasEl proyecto ha sido construido utilizando las siguientes herramientas:Core: Lógica principal del sistema (v3.x).UI: Interfaz gráfica moderna y responsiva.Base de Datos: Persistencia de datos relacional.Reportes: Motor de generación de PDFs.⚙️ InstalaciónSigue estos pasos para desplegar el proyecto en tu entorno local:Clonar el repositoriogit clone [https://github.com/tu-usuario/proyecto_biblioteca.git](https://github.com/tu-usuario/proyecto_biblioteca.git)
cd proyecto_biblioteca
Instalar dependenciaspip install customtkinter pymysql Pillow reportlab
Configurar Base de DatosImporta el script SQL biblioteca_normalizada.sql en tu servidor MySQL.Edita src/config/conexion_db.py:self.host = "localhost"
self.user = "root"
self.password = "TU_CONTRASEÑA"  # <--- Actualiza esto
self.database = "biblioteca_normalizada"
Ejecutarpython main.py
🚀 UsoLogin: Ingresa con las credenciales de administrador predeterminadas.Dashboard: Visualiza estadísticas rápidas en la pantalla principal.Menú Lateral: Navega entre Inventario, Préstamos y Reportes.📂 Estructura del ProyectoUna vista rápida de cómo está organizado el código fuente:proyecto_biblioteca/
├── 📄 main.py              # Punto de entrada
├── 📂 src/
│   ├── 📂 config/          # Conexión a BD
│   ├── 📂 controller/      # Lógica de negocio (Puente entre Vista y Modelo)
│   ├── 📂 model/           # Consultas SQL y Objetos de datos
│   ├── 📂 view/            # Interfaces Gráficas (Ventanas y Forms)
│   │   ├── 📂 admin/
│   │   ├── 📂 circulacion/
│   │   ├── 📂 inventario/
│   │   └── 📂 reportes/
│   └── 📄 navegador.py     # Router de pantallas
└── 📄 README.md            # Documentación
📸 Capturas de PantallaNota: Puedes agregar aquí imágenes de tu aplicación para mostrar cómo se ve.<details> <summary>Ver Capturas</summary>LoginMenú Principal</details><div align="center"><p>Desarrollado para el Congreso del Estado de Durango</p><p>© 2025 Todos los derechos reservados.</p></div>
