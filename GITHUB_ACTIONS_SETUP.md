# Configuración Simple de GitHub Actions

## Solo necesitas configurar 1 secret:

### `ENV_DATABASE_URL`

Tu URL de conexión a la base de datos PostgreSQL en la nube.

**Formato:**

```
postgresql://username:password@host:port/database_name
```

## Cómo configurar:

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. "New repository secret"
4. Nombre: `ENV_DATABASE_URL`
5. Valor: Tu URL de PostgreSQL

## ¿Qué hace el workflow?

- Se ejecuta cuando haces push a `main`
- Instala las dependencias
- Ejecuta las migraciones
- Despliega a Azure

## Errores Comunes y Soluciones:

### ❌ Error: "No module named 'psycopg2'"

**Solución:** Ya está incluido en requirements.txt

### ❌ Error: "DATABASE_URL not found"

**Solución:** Verifica que el secret `ENV_DATABASE_URL` esté configurado

### ❌ Error: "Connection refused" en base de datos

**Solución:** Verifica que la URL de PostgreSQL sea correcta

### ❌ Error: "Static files not found"

**Solución:** El workflow ya ejecuta `collectstatic`

### ❌ Error: "App not found" en Azure

**Solución:** Verifica que el nombre de la app sea `backen-django-aco-rl`

## Listo! 🚀

Una vez configurado el secret, cada vez que hagas push a main se desplegará automáticamente.

## Verificar que funciona:

1. Haz push a main
2. Ve a Actions en GitHub para ver el progreso
3. Si todo está bien, tu app estará en: `https://backen-django-aco-rl-fgagduasagdbejh8.northcentralus-01.azurewebsites.net`
