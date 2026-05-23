
                README - TICK_EZ 

Este es el proyecto oficial de nuestra ticketera web con 
generación de códigos QR, funcionamiento de reproductor 
Spotify y descarga automática de boletos en PDF.

Para ello deberas abrir la carpeta WinRAR donde se 
encuentran todos los archivos con codigos desarrollados que 
dan creacion al sistema de tickets "Tick_ez".


    REQUISITOS ANTES DE EMPEZAR (Instalar en PC)

Instalar:
1. Python (Versión 3.11 o 3.12) -> Marcar casilla "Add to PATH"
2. Node.js (Versión LTS) -> ¡Obligatorio para que funcione Reflex!


    CÓMO HACER FUNCIONAR EL PROYECTO EN TU COMPUTADORA

Sigue estos 4 pasos en la terminal de VS Code 
para encender la página:

Paso 1: Crear el entorno virtual (Cerebro del proyecto)
Escribe y presiona Enter:
python -m venv venv

Paso 2: Activar el entorno virtual
Escribe y presiona Enter:
.\venv\Scripts\Activate.ps1
(Sabrás que funcionó si aparece un "(venv)" verde en la terminal)

Paso 3: Instalar todas las librerías necesarias
Escribe y presiona Enter:
pip install -r requirements.txt

Paso 4: Sincronizar e inicializar Reflex
Escribe y presiona Enter:
reflex init


    LIBRERÍAS QUE INCLUYE ESTE PROYECTO (requirements.txt)

* reflex (Framework Base)
* qrcode (Para generar el código del boleto)
* pillow (Para procesar los gráficos del QR)
* reportlab (Para maquetar y diseñar el ticket en PDF)


  CÓMO ENCENDER EL SERVIDOR

Para ver la página web corriendo, escribe:
reflex run

Despues, abre el navegador de internet e ingresa a:
http://localhost:3000


PARA TENER NOCION

Reflex es un framework de codigo abierto PARA Python que 
permite crear y desplegar aplicaciones web full-stack 
(frontend y backend) utilizando unicamente Python.
Backend: FastAPI y SQLAlchemy 
Fronted: React.
Compilacion: Fronted Next.js + backend FastAPI.

Para interfaz de usuario (UI) usa funciones de Python que 
representan componentes creando variables (Vars) y 
funciones (Events) que manejan la logica y actualizan 
la interfaz.
============================================================