# Configuración de GitHub Actions para Django con Base de Datos en la Nube

## Variables de Entorno Requeridas

Para que el proyecto funcione correctamente con GitHub Actions, necesitas configurar los siguientes secrets en tu repositorio de GitHub:

### 1. Ir a Settings > Secrets and variables > Actions

En tu repositorio de GitHub, ve a:

- Settings → Secrets and variables → Actions
- Haz clic en "New repository secret"

### 2. Configurar los siguientes secrets:

#### `ENV_DATABASE_URL`

Tu URL de conexión a la base de datos PostgreSQL en la nube.

```
postgresql://username:password@host:port/database_name
```

#### `DJANGO_SECRET_KEY`

Una clave secreta segura para Django (genera una nueva para producción):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### `AZUREAPPSERVICE_CLIENTID_6211FC74B2474734A0FDE3A018F44548`

ID del cliente de Azure (ya configurado)

#### `AZUREAPPSERVICE_TENANTID_B5F54BED6C9A4E36AB479FE78AAFC033`

ID del tenant de Azure (ya configurado)

#### `AZUREAPPSERVICE_SUBSCRIPTIONID_FA0EF95108794082B84508C115D8E047`

ID de la suscripción de Azure (ya configurado)

## Workflows Configurados

### 1. `main_backen-django-aco-rl.yml`

- **Trigger**: Push a `main` branch
- **Funciones**:
  - Ejecuta tests
  - Construye la aplicación
  - Despliega a Azure Web App

### 2. `ci.yml`

- **Trigger**: Pull requests y push a `main`/`develop`
- **Funciones**:
  - Linting y formateo de código
  - Verificaciones de seguridad
  - Tests con coverage
  - Validaciones de calidad de código

## Configuración de Base de Datos

El proyecto está configurado para usar:

- **Producción**: PostgreSQL en la nube (via `DATABASE_URL`)
- **Desarrollo**: SQLite (fallback automático)

## Mejoras Implementadas

### Seguridad

- Variables de entorno para configuración sensible
- Configuración de seguridad para producción
- Verificaciones de seguridad automáticas

### Performance

- Cache de dependencias de pip
- Tests paralelos
- Coverage reporting

### Calidad de Código

- Linting con flake8
- Formateo con black
- Ordenamiento de imports con isort
- Verificaciones de seguridad con bandit y safety

## Comandos Útiles

### Generar nueva SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Verificar configuración local

```bash
python manage.py check --deploy
```

### Ejecutar tests localmente

```bash
python manage.py test --verbosity=2
```

## Troubleshooting

### Error: DATABASE_URL no encontrada

- Verifica que el secret `ENV_DATABASE_URL` esté configurado correctamente
- Asegúrate de que la URL de la base de datos sea válida

### Error: Tests fallan en CI

- Verifica que todas las dependencias estén en `requirements.txt`
- Asegúrate de que los tests no dependan de servicios externos

### Error: Deploy falla

- Verifica que las credenciales de Azure estén correctas
- Asegúrate de que la aplicación web de Azure esté configurada correctamente

## Notas Importantes

1. **Nunca** commits secrets directamente en el código
2. Usa siempre variables de entorno para configuración sensible
3. El proyecto usa `python-dotenv` para cargar variables de entorno
4. Los workflows están configurados para ejecutarse en Ubuntu latest
5. Se usa Python 3.11 para compatibilidad
