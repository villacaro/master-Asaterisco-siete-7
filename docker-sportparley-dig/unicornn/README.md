# Unicornn.com En producción

**Contenedores desplegados**

|Contenedor       |Descripción                                      |dominio                        |Puertos   |
|-----------------|-------------------------------------------------|-------------------------------|----------|
|flower           |Servicio de monitor en tiempo real de celery     |https://flower.unicornn.com/   |          |
|nodejs           |Servicio de socket.io                            |http://api.unicornn.com:8080/  |8080      |
|panel            |Servicio de Administrativo                       |https://admin.unicornn.com/    |          |
|rabbit           |Servicio de la cola de tareas en celery          |https://rabbit.unicornn.com/   |          |
|webapp           |Servicio principal de apuestas en linea          |https://www.unicornn.com/      |          |
|ws               |Servicio web (scale=2) API princiapal            |https://api.unicornn.com/      |          |
|crontab          |Servicio de ejecución para tareas programadas    |                               |          |
|worker           |Servicio de ejecución para tareas  (scale=2)     |                               |          |
|redis            |Servicio de caché                                |                               |          |
|nginx            |Servicio de despliegue                           |                               |80, 443   |

**Archivo ENV**

Debe existir un archivo llamado: env.unicornn fuera del repositorio, hay un archivo de ejemplo, env.example.unicornn en el directorio principal, guiarse por ese.

**Acceso a db**

La base de datos es lo único que se está usando fuera de docker, debes tener instalada en el sistema principal, y en el archivo env, colocas la ip de la interfaz de docker, tener en cuenta que debes agregar una regla a tu archivo pg_hba de postgres para darle acceso desde los contenedores de docker.
