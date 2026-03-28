# Galileo - contenedores para producción 

Para acceder usar el usuario:
```
lvillalobos
```

los archivos estan ubicados en la carpeta docker

Los siguientes contenedores son levantados por docker-compose, con el prefijo galileo

```
panel1
panel2
ws1
ws2

worker

flower
nginx
redis
```

Aqui el panel1, panel2, ws1, ws2, corren con supervisor, a su vez nginx implementa un balanceador de carga en ambos contenedores, esto permite tener alta disponibilida al momento de hacer deploy de cambios, para ello dependiendo de lo que ametire el cambio, solo debe reiniciarse el proceso con supervisorctl dentro el contenedor, en la descripcion principal aparece la forma de hacerlo.

Para ver los logs del sistema deben revisarse los archivos dentro de los contenedores

El contenedor `worker` contiene supervisor con los 7 workers usados

* Puertos usados

```
panel: 8090
ws http: 8091
ws https: 8092
flower: 8093
rabbit: 8094
```
* Archivo ENV

Debe existir un archivo llamado: env que se ignora por git, con las configuraciones necesarias para el servidor de galileo.

* Acceso a db

La db esta instalada en el servidor principal, con el tiempo eso buscara instalarse en otro servidor, ya que la db es un pilar vital, lo mismo con los contendores, el balanceador de carga con el tiempo debe existir en servidores distintos para asegurar rendimiento.

* Acceso a flower:
user: galileo
password: galileo123

# Deploy

La forma de hacer deploy sera la siguiente, se podran subir cambios a cualquier hora del dia, puesto que hay un balanceador de carga en nginx y 2 contenedores para el panel y el ws.

. Entrar a la carpeta docker/admin_banklotsports

. Hacer git pull

. Entrar a la carpeta docker/docker-sportparley/galileo

. Hacer `docker ps | grep galileo` para listar solo los contenedores correspondientes

. Entrar al contenedor del panel1 `docker exec -it id_panel1 bash`

. Dentro ejecutar `supervisorctl status` para verificar que este corriendo el panel

. Luego ejecutar `supervisorctl restart panel`

. Hacer lo mismo con el contenedor del panel 2

. Si los cambios son del ws, aplica de la misma forma, para el ws apesar de hay que un balanceador de carga, es recomendable hacer las actalizaciones en horas de baja carga en el servidor

. Si los cambios afectan un worker, se hace `docker-compose restart worker1` por ejemplo, de la misma forma para los demas.

. Redis nunca debe reiniciarse, o en su defecto se debe reiniciar todo de forma global.

. Para subir cambios globales, afecta todo completamente, eso si solo podra subirse por las noches, y se debe ejecutar `docker-compose restart`