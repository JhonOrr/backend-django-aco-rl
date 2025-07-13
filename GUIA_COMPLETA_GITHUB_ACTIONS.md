# 🚀 Guía Completa: GitHub Actions para Django con Base de Datos en la Nube

## 📋 Índice

1. [¿Qué es GitHub Actions?](#qué-es-github-actions)
2. [¿Por qué necesitamos esto?](#por-qué-necesitamos-esto)
3. [Configuración paso a paso](#configuración-paso-a-paso)
4. [Explicación detallada del workflow](#explicación-detallada-del-workflow)
5. [Variables de entorno y secrets](#variables-de-entorno-y-secrets)
6. [Problemas comunes y soluciones](#problemas-comunes-y-soluciones)
7. [Glosario de términos](#glosario-de-términos)

---

## 🤔 ¿Qué es GitHub Actions?

**GitHub Actions** es como un "robot" que vive en GitHub y hace tareas automáticamente cuando tú haces ciertas acciones (como hacer push de código).

### Analogía simple:

Imagina que tienes un asistente personal que:

- Ve cuando subes código nuevo
- Instala las herramientas necesarias
- Prueba que todo funcione
- Lo sube a internet automáticamente

**Sin GitHub Actions:** Tú tendrías que hacer todo manualmente cada vez
**Con GitHub Actions:** El robot lo hace automáticamente

---

## 🎯 ¿Por qué necesitamos esto?

### Problema sin automatización:

1. Haces cambios en tu código
2. Tienes que conectarte manualmente al servidor
3. Subir los archivos manualmente
4. Instalar dependencias manualmente
5. Configurar la base de datos manualmente
6. Reiniciar el servidor manualmente

### Solución con GitHub Actions:

1. Haces cambios en tu código
2. Haces `git push`
3. **¡Todo lo demás pasa automáticamente!**

---

## ⚙️ Configuración paso a paso

### Paso 1: Entender la estructura del proyecto

Tu proyecto Django tiene esta estructura:

```
backend_django_aco_rl/
├── .github/workflows/          ← Aquí van los workflows
│   └── main_backen-django-aco-rl.yml
├── backend_django_aco_rl/      ← Tu aplicación Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── optimization/               ← Tu app de optimización
├── orders/                    ← Tu app de órdenes
├── requirements.txt           ← Dependencias de Python
├── startup.txt               ← Script para iniciar en Azure
├── web.config                ← Configuración para Azure
└── manage.py                 ← Comando principal de Django
```

### Paso 2: Crear el archivo de workflow

El archivo `.github/workflows/main_backen-django-aco-rl.yml` es como una "receta" que le dice al robot qué hacer.

### Paso 3: Configurar secrets en GitHub

Los **secrets** son como contraseñas que GitHub guarda de forma segura.

---

## 📝 Explicación detallada del workflow

Vamos a analizar línea por línea el archivo `main_backen-django-aco-rl.yml`:

### 1. **Encabezado del archivo**

```yaml
name: Build and deploy Python app to Azure Web App - backen-django-aco-rl
```

- `name:`: El nombre que aparece en GitHub Actions
- Es como ponerle un título a tu receta

### 2. **Cuándo se ejecuta**

```yaml
on:
  push:
    branches:
      - main
  workflow_dispatch:
```

- `on:`: Define cuándo se ejecuta el workflow
- `push:`: Se ejecuta cuando haces push
- `branches: - main`: Solo cuando haces push a la rama "main"
- `workflow_dispatch:`: Permite ejecutarlo manualmente desde GitHub

### 3. **Jobs (Trabajos)**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
```

- `jobs:`: Son las tareas principales
- `build:`: Nombre del primer trabajo
- `runs-on: ubuntu-latest`: Se ejecuta en un servidor Linux

### 4. **Steps (Pasos) del job build**

#### Step 1: Descargar el código

```yaml
- uses: actions/checkout@v4
```

- `uses:`: Usa una acción predefinida
- `actions/checkout@v4`: Descarga tu código del repositorio

#### Step 2: Crear archivo de variables de entorno

```yaml
- name: Create .env file from secret
  run: echo "DATABASE_URL=${{ secrets.ENV_DATABASE_URL }}" > .env
```

- `name:`: Nombre del paso (aparece en los logs)
- `run:`: Comando que se ejecuta
- `echo "DATABASE_URL=..." > .env`: Crea un archivo .env con la URL de la base de datos
- `${{ secrets.ENV_DATABASE_URL }}`: Obtiene el valor del secret

#### Step 3: Configurar Python

```yaml
- name: Set up Python version
  uses: actions/setup-python@v5
  with:
    python-version: "3.11"
```

- Instala Python 3.11 en el servidor
- `with:`: Parámetros para la acción

#### Step 4: Instalar dependencias

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

- `|`: Permite escribir múltiples líneas
- Actualiza pip e instala las dependencias de `requirements.txt`

#### Step 5: Ejecutar migraciones

```yaml
- name: Run migrations
  run: python manage.py migrate --noinput
```

- Ejecuta las migraciones de Django para crear las tablas
- `--noinput`: No pide confirmación

#### Step 6: Recolectar archivos estáticos

```yaml
- name: Collect static files
  run: python manage.py collectstatic --noinput
```

- Copia archivos CSS, JS, imágenes a una carpeta para servir

#### Step 7: Crear archivo ZIP

```yaml
- name: Zip artifact for deployment
  run: zip release.zip ./* -r
```

- Crea un archivo ZIP con todo el proyecto
- `-r`: Incluye subcarpetas

#### Step 8: Subir el artifact

```yaml
- name: Upload artifact for deployment jobs
  uses: actions/upload-artifact@v4
  with:
    name: python-app
    path: release.zip
```

- Sube el ZIP a GitHub para que el siguiente job lo use

### 5. **Job deploy**

#### Step 1: Descargar el artifact

```yaml
- name: Download artifact from build job
  uses: actions/download-artifact@v4
  with:
    name: python-app
```

- Descarga el ZIP que creó el job anterior

#### Step 2: Descomprimir

```yaml
- name: Unzip artifact for deployment
  run: unzip release.zip
```

- Descomprime el archivo ZIP

#### Step 3: Crear .env en Azure

```yaml
- name: Create .env file for Azure
  run: echo "DATABASE_URL=${{ secrets.ENV_DATABASE_URL }}" > .env
```

- **¡IMPORTANTE!** Crea el archivo .env en Azure también
- Sin esto, la app no encuentra la base de datos

#### Step 4: Conectarse a Azure

```yaml
- name: Login to Azure
  uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZUREAPPSERVICE_CLIENTID_... }}
    tenant-id: ${{ secrets.AZUREAPPSERVICE_TENANTID_... }}
    subscription-id: ${{ secrets.AZUREAPPSERVICE_SUBSCRIPTIONID_... }}
```

- Se conecta a tu cuenta de Azure usando credenciales

#### Step 5: Desplegar

```yaml
- name: Deploy to Azure Web App
  uses: azure/webapps-deploy@v3
  with:
    app-name: backen-django-aco-rl
    slot-name: Production
```

- Sube tu aplicación a Azure

---

## 🔐 Variables de entorno y secrets

### ¿Qué son las variables de entorno?

Son como "notas" que tu aplicación lee para saber cómo configurarse.

### Ejemplo:

```python
# En tu código
DATABASE_URL = os.getenv('DATABASE_URL')
```

- `os.getenv('DATABASE_URL')`: Busca una variable llamada DATABASE_URL
- Si la encuentra, la usa; si no, usa un valor por defecto

### ¿Qué son los secrets?

Son variables de entorno que contienen información sensible (contraseñas, URLs de base de datos, etc.)

### Cómo configurar secrets:

1. Ve a tu repositorio en GitHub
2. Click en "Settings" (Configuración)
3. En el menú izquierdo, click en "Secrets and variables" → "Actions"
4. Click en "New repository secret"
5. Nombre: `ENV_DATABASE_URL`
6. Valor: `postgresql://usuario:contraseña@servidor:puerto/base_de_datos`

### Ejemplo de DATABASE_URL:

```
postgresql://mi_usuario:mi_contraseña@mi-servidor.postgres.database.azure.com:5432/mi_base_de_datos
```

---

## 🔧 Problemas comunes y soluciones

### ❌ Error: "Failed to fetch federated token"

**Problema:** GitHub no puede autenticarse con Azure
**Solución:** Agregar permisos en el workflow:

```yaml
permissions:
  id-token: write
  contents: read
```

### ❌ Error: "no such table: orders_order"

**Problema:** La base de datos no está configurada correctamente
**Solución:**

1. Verificar que el secret `ENV_DATABASE_URL` esté configurado
2. Crear el archivo .env en el job de deploy
3. Ejecutar migraciones

### ❌ Error: "DATABASE_URL is None"

**Problema:** El archivo .env no se está creando
**Solución:** Agregar el paso para crear .env en el job deploy

### ❌ Error: "Connection refused"

**Problema:** La URL de la base de datos es incorrecta
**Solución:** Verificar que la URL de PostgreSQL sea válida

---

## 📚 Glosario de términos

### **Workflow**

- Es como una "receta" que le dice a GitHub Actions qué hacer
- Se define en archivos `.yml`

### **Job**

- Es una tarea principal dentro del workflow
- Ejemplo: "build" (construir) y "deploy" (desplegar)

### **Step**

- Es un paso específico dentro de un job
- Ejemplo: "instalar dependencias", "ejecutar migraciones"

### **Action**

- Es una función predefinida que puedes usar
- Ejemplo: `actions/checkout@v4` descarga tu código

### **Secret**

- Es una variable que contiene información sensible
- Se guarda de forma segura en GitHub

### **Artifact**

- Es un archivo que se crea en un job y se usa en otro
- Ejemplo: el ZIP que se crea en "build" y se usa en "deploy"

### **Environment**

- Es el entorno donde se ejecuta tu aplicación
- Ejemplo: desarrollo, producción

### **Deploy**

- Es el proceso de subir tu aplicación a internet
- Ejemplo: subir a Azure, Heroku, etc.

### **Migration**

- Es un cambio en la estructura de la base de datos
- Ejemplo: crear una nueva tabla

### **Static files**

- Son archivos que no cambian (CSS, JS, imágenes)
- Django los sirve desde una carpeta específica

---

## 🎓 Conceptos importantes para aprender

### 1. **CI/CD (Continuous Integration/Continuous Deployment)**

- **CI:** Integración continua - probar código automáticamente
- **CD:** Despliegue continuo - subir a producción automáticamente

### 2. **Infrastructure as Code**

- Definir tu infraestructura (servidores, configuraciones) en código
- En lugar de configurar manualmente, lo defines en archivos

### 3. **Environment Variables**

- Variables que cambian según el entorno
- Ejemplo: URL de base de datos diferente en desarrollo vs producción

### 4. **Secrets Management**

- Manejo seguro de información sensible
- Nunca poner contraseñas directamente en el código

### 5. **Artifact Management**

- Manejo de archivos entre diferentes pasos del workflow
- Ejemplo: pasar el código compilado del build al deploy

---

## 🚀 Próximos pasos para aprender más

1. **Leer la documentación oficial:**

   - [GitHub Actions Documentation](https://docs.github.com/en/actions)
   - [Azure Web Apps Documentation](https://docs.microsoft.com/en-us/azure/app-service/)

2. **Experimentar:**

   - Crear workflows simples
   - Probar diferentes acciones
   - Entender los logs de GitHub Actions

3. **Conceptos avanzados:**

   - Testing automático
   - Linting y formateo de código
   - Coverage de código
   - Security scanning

4. **Herramientas relacionadas:**
   - Docker para contenedores
   - Kubernetes para orquestación
   - Terraform para infraestructura

---

## 💡 Consejos para principiantes

1. **Empieza simple:** No intentes hacer todo de una vez
2. **Lee los logs:** Los errores te enseñan mucho
3. **Experimenta:** Prueba cambios pequeños y ve qué pasa
4. **Documenta:** Escribe notas de lo que aprendes
5. **Pregunta:** La comunidad de GitHub es muy útil

---

## 🎯 Resumen de lo que aprendiste

✅ **Qué es GitHub Actions y por qué es útil**
✅ **Cómo crear un workflow básico**
✅ **Cómo configurar secrets y variables de entorno**
✅ **Cómo desplegar una aplicación Django a Azure**
✅ **Cómo solucionar problemas comunes**
✅ **Terminología básica de CI/CD**

¡Felicidades! Ahora tienes una base sólida para entender y trabajar con GitHub Actions. 🎉

---

_Esta guía fue creada para ayudarte a entender el proceso completo. Si tienes dudas, no dudes en preguntar. ¡El aprendizaje es un proceso continuo!_
