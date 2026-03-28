# Dev - contenedores para desarrollo local

Para desarrolo local se instancian los siguientes contendores:

```
panel1
ws1

worker

flower
nginx
redis
```

El panel1 y ws1 corren directamente el .bash, no ejecutan supervisor, esto con la finalidad de usar el siguiente comando
```

El contenedor `worker` contiene supervisor con los 7 workers usados

// para ver todos los log
$ docker-compose logs

// si se quiere ver los logs solo del panel por ejemplo, hacerlo de esta forma:
$ docker-compose logs panel1
```
Esto es solo en dev, ya que aveces se usa un print y no es viable estar revisando los archivos log que genera supervisor.

* Puertos usados

Dependiendo de la ip generada por docker o docker-machine, debe configurarse el siguiente archivo:
```
$ sudo nano /etc/hosts
```
Y agregar lo siguiente (cambiar la ip 127.0.0.1 por la de docker-machine en caso de qe lo uses):
```
127.0.0.1       dev.panel
127.0.0.1       dev.ws
127.0.0.1       dev.flower
127.0.0.1       dev.rabbit
```

Para acceder a los proyectos basta con entrar desde el navegador por los siguientes dominios:
```
panel: dev.panel
ws: dev.ws
flower: dev.flower
```
* Archivo ENV

Debe existir un archivo llamado: env que se ignora por git, esto con la finalidad de que cada desarrollador tenga configuraciones independientes, hay un archivo de ejemplo, env.example en el directorio principal, guierse por ese.

* Acceso a db

La base de datos es lo unico que se esta usando fuera de docker, debes tenerla instalada en tu sistema principal, y en el archivo env, colocas la ip que te proporciona tu router, tener en cuenta que debes agregar una regla a tu archivo pg_hba de postgres para darle acceso desde los contenedores de docker.

Con el tiempo solo localmente postgres tambien puede servirse en un contenedor.

* Acceso a flower:
user: dev
password: dev123