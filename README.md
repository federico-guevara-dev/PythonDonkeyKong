# Trabajo Práctico de Laboratorio N°2: Interfaz Gráfica de Usuario (GUI) y GitHub Fork

**Materia:** Laboratorio de Programación  
**Docentes:** Prof. Federico Coronati ([fjcoronati@gmail.com](mailto:fjcoronati@gmail.com)) | Prof. Fedullo ([mfedullo@gmail.com](mailto:mfedullo@gmail.com))  
**Alumno:** Federico Guevara  
**Email:** [federicoguevaradev@gmail.com](mailto:federicoguevaradev@gmail.com)  
**Repositorio Original:** [https://github.com/plemaster01/PythonDonkeyKong](https://github.com/plemaster01/PythonDonkeyKong)  
**Fork del Proyecto:** [https://github.com/federico-guevara-dev/PythonDonkeyKong](https://github.com/federico-guevara-dev/PythonDonkeyKong)  

---

## 1. Objetivo del Trabajo Práctico

El objetivo principal de este trabajo práctico consiste en:
1. Tomar un proyecto de código abierto existente con Interfaz Gráfica de Usuario (GUI) en Python desde GitHub.
2. Realizar un **Fork (bifurcación)** legítimo hacia la cuenta personal de GitHub para preservar autoría original y permitir contribuciones futuras.
3. Clonar el repositorio localmente, comprobar y depurar su funcionamiento.
4. Aplicar modificaciones sustanciales a la interfaz gráfica y funciones del sistema (remitente de email, imágenes personalizadas, selector de destinatarios con `OptionMenu()` y entrada manual).
5. Compilar un archivo ejecutable autónomo (`.exe` para Windows) alojado en la carpeta `output/`.
6. Diseñar un informe progresivo en este archivo `README.md` documentando las modificaciones en cada commit.
7. Mantener un historial de al menos 4 commits descriptivos en Git y sincronizarlos con GitHub.

---

## 2. Proyecto Base Seleccionado

Se seleccionó una reconstrucción completa en Python con Pygame del clásico juego arcade **Donkey Kong**. El repositorio fue bifurcado correctamente a la cuenta del alumno:
`https://github.com/federico-guevara-dev/PythonDonkeyKong`.

---

## 3. Modificaciones Fase 1: Motor Gráfico, Sprites HD y Rutas

En este primer hito de desarrollo se aplicaron mejoras sustanciales a la base del juego en `main.py`:
- **Optimización de Sprites con Smoothscale Bilineal:** El código original utilizaba `pygame.transform.scale()`, produciendo pixelado aserrado al reducir los sprites de 1440x1440 px. Se implementó `pygame.transform.smoothscale()` con filtrado bilineal y canal alfa `.convert_alpha()`, logrando que Donkey Kong, Mario, barriles, fuego, martillos y Peach se visualicen en alta definición (HD) con bordes suaves.
- **Resolución Adaptable:** Se ajustaron las dimensiones a 720x660 px con escala proporcional de secciones (`section_width`, `section_height`, `slope`) para adaptarse tanto a pantallas de netbooks escolares como a monitores estándar.
- **Rutas Relativas Dinámicas con PyInstaller:** Implementación de la función `resource_path()` para resolver recursos dinámicamente tanto en modo desarrollo como empaquetado (`sys._MEIPASS`).
- **Modularización del Loop de Juego:** Se encapsuló la lógica del juego en la función `run_game(existing_high_score)` retornando puntuaciones finales para su posterior integración con la GUI de Tkinter.

### Captura de Pantalla: Donkey Kong Rebuild (Sprites HD)
![Donkey Kong HD](docs/captura_juego_hd.png)

---

## 4. Historial de Commits (Bitácora de Desarrollo)

| N° | Commit | Descripción |
|:---:|---|---|
| **1** | `feat: optimizacion de sprites con smoothscale y documentacion inicial en README` | Carga de sprites en alta definición con filtrado bilineal y canal alfa; resolución adaptable a netbooks escolares e inicio del informe README.md. |
