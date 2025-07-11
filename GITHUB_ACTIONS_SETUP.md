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

## Listo! 🚀

Una vez configurado el secret, cada vez que hagas push a main se desplegará automáticamente.
