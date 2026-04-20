# Selenium Grid & Selenoid — Suite de pruebas distribuidas

Proyecto de automatización de pruebas end-to-end ejecutable indistintamente contra **Selenium Grid 4** y **Selenoid**, cambiando únicamente una variable de entorno. Toda la infraestructura se despliega con Docker Compose.

> **Stack:** Python 3.12 · pytest · Selenium 4 · Docker Compose · WSL2 (Ubuntu 22.04)

---
 
## 📋 Tabla de contenidos

- [Requisitos previos](#requisitos-previos)
- [Instalación paso a paso](#instalación-paso-a-paso)
- [Ejecución de las pruebas](#ejecución-de-las-pruebas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Limitaciones conocidas](#limitaciones-conocidas)
- [Troubleshooting](#troubleshooting)

---

## Requisitos previos

| Componente | Versión mínima | Nota |
|---|---|---|
| Docker Desktop | 4.x | En Windows, con integración WSL2 activada |
| WSL2 + Ubuntu | 22.04 | Sólo para Windows; en Linux/macOS no aplica |
| Python | 3.10+ | El proyecto se probó con 3.12 |
| Git | Cualquiera | Para clonar |
| RAM asignada a Docker | 6 GB | Mínimo recomendado para paralelización |

**Verificación rápida:**
```bash
docker --version
docker compose version
python3 --version
git --version
```

---

## Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPO> selenium-grid-selenoid
cd selenium-grid-selenoid
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate          # Linux/WSL/macOS
# .venv\Scripts\activate           # Windows PowerShell
pip install -r requirements.txt
```

### 3. Descargar las imágenes Docker

#### Imágenes de Selenium Grid

```bash
docker pull selenium/hub:4.27.0
docker pull selenium/node-chrome:4.27.0
docker pull selenium/node-firefox:4.27.0
```

#### Imágenes de Selenoid

```bash
docker pull aerokube/selenoid:latest-release
docker pull aerokube/selenoid-ui:latest-release
docker pull selenoid/vnc:chrome_128.0
docker pull selenoid/vnc:firefox_125.0
docker pull selenoid/video-recorder:latest-release
```

> **Nota:** Las imágenes de Selenoid sólo están disponibles hasta Chrome 128 y Firefox 125 porque Aerokube detuvo las actualizaciones. Es el estado actual del ecosistema.

### 4. Ajustar rutas absolutas en el compose de Selenoid (sólo primera vez)

El archivo `docker/docker-compose-selenoid.yml` contiene rutas absolutas del autor. Debes reemplazarlas por las tuyas:

```bash
# Ver cuál es tu ruta
realpath selenoid

# Editar el compose reemplazando /home/yhurtado/proyectos/selenium-grid-selenoid
# por la ruta que te devolvió el comando anterior
```

O automatizarlo:

```bash
CURRENT_PATH=$(pwd)
sed -i "s|/home/yhurtado/proyectos/selenium-grid-selenoid|$CURRENT_PATH|g" docker/docker-compose-selenoid.yml
```

---

## Ejecución de las pruebas

### Opción A — Contra Selenium Grid

```bash
# 1. Levantar el Grid
cd docker
docker compose -f docker-compose-grid.yml up -d
cd ..

# 2. Verificar que está operativo: abrir http://localhost:4444

# 3. Ejecutar la suite
REMOTE_URL=http://localhost:4444/wd/hub BROWSER=chrome pytest tests/ -v -n 3

# 4. Apagar el Grid
cd docker
docker compose -f docker-compose-grid.yml down
cd ..
```

### Opción B — Contra Selenoid

```bash
# 1. Levantar Selenoid
cd docker
docker compose -f docker-compose-selenoid.yml up -d
cd ..

# 2. Verificar Selenoid UI: abrir http://localhost:8080

# 3. Ejecutar la suite
REMOTE_URL=http://localhost:4444/wd/hub BROWSER=chrome pytest tests/ -v -n 3

# 4. Ver sesiones en vivo (opcional, mientras corren las pruebas)
# En Selenoid UI haz clic en una sesión activa para abrir VNC

# 5. Apagar Selenoid
cd docker
docker compose -f docker-compose-selenoid.yml down
cd ..
```

### Variables de entorno soportadas

| Variable | Valores | Default | Descripción |
|---|---|---|---|
| `REMOTE_URL` | URL completa | *(vacío)* | URL del Grid/Selenoid. Si está vacío, corre local. |
| `BROWSER` | `chrome`, `firefox` | `chrome` | Navegador a utilizar |
| `ENABLE_VIDEO` | `true`, `false` | `false` | Activa grabación (solo Selenoid, ver limitaciones) |
| `ENABLE_VNC` | `true`, `false` | `true` | Activa visor VNC en Selenoid |

### Ejecuciones útiles

```bash
# Solo pruebas de humo
pytest tests/ -m smoke -v

# Todas menos las lentas
pytest tests/ -m "not slow" -v -n auto

# Solo un archivo específico
pytest tests/test_auth.py -v

# Firefox en lugar de Chrome
REMOTE_URL=http://localhost:4444/wd/hub BROWSER=firefox pytest tests/ -v

# Medir tiempo de ejecución
time REMOTE_URL=http://localhost:4444/wd/hub BROWSER=chrome pytest tests/ -v -n 3

# Local sin Grid (sólo Chrome, con chromedriver automático)
pytest tests/ -v
```

---

## Estructura del proyecto

```
selenium-grid-selenoid/
├── docker/
│   ├── docker-compose-grid.yml        # Hub + nodos Chrome y Firefox
│   └── docker-compose-selenoid.yml    # Selenoid + Selenoid UI
├── selenoid/
│   ├── browsers.json                  # Declaración de navegadores disponibles
│   └── video/                         # Carpeta para videos grabados
├── tests/
│   ├── base/
│   │   └── driver_factory.py          # Construcción del WebDriver según entorno
│   ├── pages/                         # Page Object Model
│   │   ├── home_page.py
│   │   ├── login_page.py
│   │   ├── checkboxes_page.py
│   │   ├── dropdown_page.py
│   │   ├── dynamic_loading_page.py
│   │   ├── javascript_alerts_page.py
│   │   ├── add_remove_page.py
│   │   └── key_presses_page.py
│   ├── test_auth.py                   # Pruebas de autenticación (5)
│   ├── test_forms.py                  # Pruebas de formularios (4)
│   ├── test_interactions.py           # Interacciones UI + JS (9)
│   └── test_dynamic.py                # Carga dinámica (1)
├── conftest.py                        # Fixture del driver
├── pytest.ini                         # Configuración de pytest y marcadores
├── requirements.txt                   # Dependencias Python
└── README.md
```

**19 pruebas organizadas** en 4 archivos temáticos, cubriendo autenticación, formularios, interacciones con teclado, alertas JavaScript, adición/eliminación de elementos y carga asíncrona.

---

## Limitaciones conocidas

### 1. Grabación de video no funciona en Windows + WSL2

**Síntoma:** al activar `ENABLE_VIDEO=true`, los logs de Selenoid muestran:
```
[VIDEO_ERROR] [Failed to rename /opt/selenoid/video/selenoid<hash>.mp4
to /opt/selenoid/video/<session>.mp4: no such file or directory]
```

**Causa:** bug conocido documentado en [aerokube/cm#293](https://github.com/aerokube/cm/issues/293). El contenedor `video-recorder` que Selenoid crea dinámicamente no logra renombrar el archivo final debido a la traducción de rutas entre Docker Desktop y WSL2. El mantenedor ha declarado que no planea resolverlo.

**Mitigación:** dejar `ENABLE_VIDEO=false` y mantener `ENABLE_VNC=true` (que funciona perfectamente). Para capturar evidencia, usar la grabación nativa de Windows (Win+G) o herramientas externas.

**Plataformas sin este bug:** Linux nativo y macOS.

### 2. Imágenes de Selenoid descontinuadas

La última versión disponible oficialmente es **Chrome 128** y **Firefox 125**. Aerokube dejó de actualizar las imágenes públicas en 2024. Para navegadores más recientes hay dos caminos: construir imágenes propias usando los Dockerfiles de [aerokube/selenoid-images](https://github.com/aerokube/selenoid-images) o usar Selenium Grid que sí recibe actualizaciones.

### 3. `test_key_press[ENTER]` marcado como xfail

La tecla ENTER en un `<input type="text">` dispara el "submit implícito" del formulario en Chrome, lo que impide que el listener JavaScript de la página de prueba capture el evento `keyup`. No es un bug de Selenium ni del proyecto: es comportamiento nativo del navegador. Se documentó como `xfail` con justificación en `tests/test_interactions.py`.

---

## Troubleshooting

### Docker no encuentra las imágenes

```bash
# Verificar qué tienes descargado
docker images | grep -E "selenium|selenoid|aerokube"

# Re-descargar si falta alguna
docker pull <nombre_imagen>:<tag>
```

### El Grid arranca pero las pruebas fallan con "no nodes"

Espera unos segundos tras `docker compose up -d` para que los nodos se registren en el Hub. Verifica en `http://localhost:4444` que aparezcan los nodos antes de lanzar las pruebas.

### Chrome/Firefox se cierran aleatoriamente en Grid

Asegúrate de que `docker-compose-grid.yml` tenga `shm_size: 2gb` en cada nodo. Sin este ajuste el navegador muere por falta de memoria compartida.

### Selenoid da error `No such image: selenoid/vnc:chrome_XXX`

La versión declarada en `browsers.json` no existe en tu Docker local. Ejecuta `docker pull selenoid/vnc:chrome_128.0` (o la versión que tengas configurada).

### Error de permisos con `/var/run/docker.sock`

Tu usuario no pertenece al grupo `docker`. Ejecuta:
```bash
sudo usermod -aG docker $USER
# Cerrar sesión y volver a abrir
```

### `fixture 'driver' not found`

Te falta ejecutar pytest desde la raíz del proyecto, o el `conftest.py` está vacío. Verifica:
```bash
pwd          # debe ser la raíz del proyecto
cat conftest.py    # debe contener la fixture
```

### En Windows/WSL2: "command not found" para docker

Verifica que Docker Desktop tenga activada la integración WSL en Settings → Resources → WSL Integration → tu distro de Ubuntu.

---

## Resultados medidos

| Métrica | Valor |
|---|---|
| Pruebas totales | 19 (4 archivos, 6 Page Objects) |
| Tiempo suite inicial de 3 pruebas, secuencial | 11.11 s |
| Tiempo suite inicial de 3 pruebas, `-n 3` | 7.40 s |
| Mejora por paralelización | 33 % |
| Tiempo suite completa de 19 pruebas, `-n 3` | 33-36 s |
| Resultado final | 18 passed, 1 xfailed |
| Estabilidad | 100 % (0 fallos reales) |

---

## Recursos

- [Documentación oficial de Selenium Grid](https://www.selenium.dev/documentation/grid/)
- [Repositorio docker-selenium](https://github.com/SeleniumHQ/docker-selenium)
- [Documentación de Selenoid](https://aerokube.com/selenoid/latest/)
- [Aplicación bajo prueba: The Internet Herokuapp](https://the-internet.herokuapp.com)
- [pytest-xdist](https://pytest-xdist.readthedocs.io/)

---

## Licencia

Proyecto educativo. Libre para uso y modificación.