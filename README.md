<!-- ENCABEZADO CENTRADO --><div align="center"><img src="https://www.google.com/search?q=https://cdn-icons-png.flaticon.com/512/2232/2232688.png" alt="Logo Biblioteca" width="100" height="100">Sistema de Gestión BibliotecariaCongreso del Estado de Durango<!-- BADGES --><p><img src="Proyecto_biblioteca\logo.png" alt="Version"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Estado-Terminado-success%3Fstyle%3Dfor-the-badge%26logo%3Dappveyor" alt="Estado"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3.x-3776AB%3Fstyle%3Dfor-the-badge%26logo%3Dpython%26logoColor%3Dwhite" alt="Python"></p></div>💡 DescripciónAplicación de escritorio moderna desarrollada en Python para la administración integral de flujos de trabajo bibliotecarios. Gestiona catálogo, usuarios y préstamos con una interfaz intuitiva y reportes profesionales.📑 Tabla de Contenidos✨ Características🛠️ Tecnologías⚙️ Instalación🚀 Uso📂 Estructura✨ CaracterísticasMóduloDescripción🔐 Control de AccesoLogin seguro con roles (Admin/Bibliotecario).📚 InventarioRegistro por pasos, búsqueda y bajas.🔄 CirculaciónPréstamos y devoluciones con validación.👥 UsuariosGestión de lectores y visitas.📄 ReportesGeneración de PDFs automáticos.🛠️ TecnologíasEste proyecto utiliza las siguientes librerías:Interfaz: customtkinter (Diseño moderno).Base de Datos: pymysql (Conexión a MySQL).Imágenes: Pillow (Manejo de logos).Reportes: reportlab (Generación de PDF).⚙️ InstalaciónSigue estos pasos en tu terminal:1. Clonar el proyectogit clone [https://github.com/tu-usuario/proyecto_biblioteca.git](https://github.com/tu-usuario/proyecto_biblioteca.git)
cd proyecto_biblioteca
2. Instalar dependenciaspip install customtkinter pymysql Pillow reportlab
3. Configurar Base de DatosImporta el script SQL en tu servidor MySQL.Edita el archivo src/config/conexion_db.py con tu contraseña:self.host = "localhost"
self.user = "root"
self.password = "TU_CONTRASEÑA_AQUI"
self.database = "biblioteca_normalizada"
4. Ejecutar la aplicaciónpython main.py
🚀 Uso RápidoInicio de Sesión: Usa las credenciales de administrador.Menú Principal: Usa la barra lateral izquierda para navegar.Préstamos: Ve a la sección "Préstamos", busca el libro y el usuario, y confirma.📂 Estructura del Proyectoproyecto_biblioteca/
├── main.py               # Archivo principal
├── src/
│   ├── config/           # Conexión DB
│   ├── controller/       # Lógica del sistema
│   ├── model/            # Consultas SQL
│   ├── view/             # Ventanas gráficas
│   └── navegador.py      # Router
└── README.md             # Este archivo
<div align="center"><p>Desarrollado para el Congreso del Estado de Durango</p><p>© 2025 Todos los derechos reservados.</p></div>