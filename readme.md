📊 OptiSolve: Solver de Programación Lineal (PL)

OptiSolve es una herramienta web educativa diseñada para resolver problemas de Programación Lineal (PL) utilizando el Método Gráfico y, próximamente, el Método Simplex/Dos Fases. Inspirado en la funcionalidad de herramientas clásicas como PHPSimplex, este proyecto se enfoca en la claridad visual y la facilidad de uso.

💡 Motivación del Proyecto

OptiSolve surge de la necesidad de una herramienta moderna y funcional para la asignatura de Investigación de Operaciones. La herramienta anterior, PHPSimplex, se consideró desactualizada y dejó de mostrar correctamente la solución gráfica debido a problemas de actualización y credenciales. Esto motivó la creación de este sustituto robusto basado en Django y Chart.js.

✨ Características Principales

Método Gráfico Interactivo: Resuelve problemas de PL con dos variables ($X_1, X_2$), dibujando la región factible y encontrando el punto óptimo.

Visualización con Chart.js: Muestra las líneas de restricción, los vértices y la solución óptima en un gráfico de coordenadas.

Formulario Dinámico: Permite añadir y eliminar restricciones de forma dinámica usando JavaScript.

Descarga de Gráficos: Botón para descargar la solución gráfica como una imagen PNG.

Retención de Datos: Conserva los datos del formulario (función objetivo y restricciones) tras el envío, incluso si hay errores de cálculo.

Futuras Expansiones: Estructura preparada para implementar el Método Simplex y el Método de las Dos Fases.

🚀 Tecnologías Utilizadas

Componente

Tecnología

Propósito

Backend

Python 🐍

Lógica principal y manejo del servidor.

Framework

Django

Desarrollo rápido y gestión de la aplicación web.

Matemáticas

NumPy

Álgebra lineal (resolución de sistemas $2\times 2$) para intersecciones.

Frontend

Bootstrap 5

Diseño responsivo, layout y estilos de la interfaz (incluido el sidebar).

Gráficos

Chart.js

Renderizado dinámico del gráfico cartesiano de la región factible.

Interactividad

JavaScript

Lógica de retención de formularios y botones dinámicos.

🛠️ Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar OptiSolve en tu entorno local.

Prerrequisitos

Python 3.8+

pip (Administrador de paquetes de Python)

Pasos

Clonar el Repositorio (Si aplica, si no, usa tus directorios actuales)

git clone [URL_DEL_REPOSITORIO]
cd optisolve_project



Crear y Activar el Entorno Virtual

python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows (CMD/PowerShell):
# .\venv\Scripts\activate



Instalar Dependencias

pip install django numpy



Ejecutar Migraciones (Configuración de Base de Datos)

python manage.py migrate



Iniciar el Servidor de Desarrollo

python manage.py runserver



El proyecto estará disponible en tu navegador en: http://127.0.0.1:8000/

📝 Uso del Método Gráfico

Para probar la funcionalidad, puedes usar el siguiente ejemplo:

Problema: Maximizar $Z = 3X_1 + 5X_2$

Restricción

Formato de Entrada

$X_1 \le 4$

1*x1 + 0*x2 <= 4

$2X_2 \le 12$

0*x1 + 2*x2 <= 12

$3X_1 + 2X_2 \le 18$

3*x1 + 2*x2 <= 18

Solución Esperada: $Z_{máx} = 42$ en el punto $(X_1=4, X_2=6)$.

🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas añadir la funcionalidad del Método Simplex o mejorar el parsing de las ecuaciones, por favor, abre un issue o envía un Pull Request.

Pendientes Clave:

$$$$

 Implementar el Método Simplex y el Método de las Dos Fases.

$$$$

 Mejorar la robustez del parser de ecuaciones (manejar diferentes formatos de entrada del usuario).

$$$$

 Dibujar la Región Factible con relleno de color en Chart.js (requiere un plugin o librería avanzada).

📄 Licencia

Este proyecto está bajo la Licencia MIT