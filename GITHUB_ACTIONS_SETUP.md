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
- **Crea el archivo .env en Azure** (¡Importante!)

## Errores Comunes y Soluciones:

### ❌ Error: "no such table: orders_order"

**Solución:** El archivo .env ahora se crea en Azure también. Verifica que:

1. El secret `ENV_DATABASE_URL` esté configurado correctamente
2. La URL de PostgreSQL sea válida
3. Las migraciones se ejecuten en Azure

### ❌ Error: "DATABASE_URL is None"

**Solución:** El archivo .env se crea en el job de deploy también

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

## Debugging:

Si sigues teniendo problemas, puedes verificar:

- Los logs de Azure en el portal
- Los logs de GitHub Actions
- Que el secret `ENV_DATABASE_URL` esté configurado correctamente
