# Docker - SportParley

Descripcion general, para instalar y usar los contenedores de manera sencilla.

Para información de puertos usados y demas configuraciones personalizadas en los servidores revisar cada carpeta, por ejemplo para desarrollo local deben usar la carpeta dev 


# Instalacion

Instalar todo con las instrucciones de los websites oficiales; para docker tener cuidado y agregar el usuario anfitrion al grupo de docker y asi usarlo sin sudo.

* Leer la [documentacion oficial de docker](https://docs.docker.com/)

* Requerimientos de Docker
```
docker 1.8.1
docker-compose 1.4.0
```

Instalar docker 1.7.1
[install linux](https://docs.docker.com/installation/ubuntulinux/)
[install mac](https://docs.docker.com/installation/mac/)

Instalar docker-compose 1.3.3
[install](https://docs.docker.com/compose/install/)


# Opcional
```
virtualbox 4.3
docker-machine 0.4.0-rc1
```

* virtualbox y docker-machine son solo para uso local, es como el servidor en nuestras maquinas, en los servidores no hace falta.

Install virtualbox 4.3
```
$ sudo apt-get install virtualbox
```

Instalar docker-machine 0.4.0-rc1
	[install](https://docs.docker.com/machine/)

```
// Nota: en linux usar ya que tiene soporte para la carpeta compartida de virtualbox
$ curl -L https://github.com/docker/machine/releases/download/v0.4.0-rc1/docker-machine_linux-amd64 > /usr/local/bin/docker-machine
```

* Inicializando entorno de trabajo

Solo la primera vez para crear la maquina virtual
``` 
$ docker-machine create --driver virtualbox --virtualbox-memory 1024 --virtualbox-cpu-count 2 sportparley
``` 

Luego basta con ejecutar la maquina virtual
``` 
$ docker-machine start sportparley

// Activamos docker en la maquina virtual
$ eval "$(docker-machine env sportparley)"
```

# Primer uso

* Nos ubicamos en la carpeta correspondiente del repositorio, para desarrollo es dev, y le damos permisos de ejecucion a los archivos bash que ejecutan los proyectos
``` 
$ chmod +x config-supervisor/bash/ws/ws.bash
$ chmod +x config-supervisor/bash/panel/panel.bash
```

```
// Construimos las imagenes
// Tener paciencia con cantv :( para intalar todos los requerimientos
$ docker-compose build 

// Levantamos todas las imagenes en modo demonio (-d), la primera vez hara un pull
// Tener paciencia con cantv :(
$ docker-compose up -d 
```

Ya luego al inicial la pc, activamos la maquina virtual o la iniciamos y los contendores se iniciaran solos

# Uso comun o utilidades

* Como ejecutar los comandos, ejemplo un migrate, con docker-compose se inicia un contenedor temporal, explico los parametros.
--rm: elimina el contenedor apenas finaliza el comando
--no-deps: evita levantar contenedores de los cuales dependa
```
$ docker-compose run --rm --no-deps [app-name] python manage.py [command]
```

* Otra forma es abrir un shell de un contenedor en ejecucion y procesar los comandos allí (esto se debe hacer asi en produccion, ya que hay un balanceador de carga en nginx, primero se sube todo a panel1 por ejemplo y luego a panel2, las migraciones o reload menu solo se ejecutan una vez)
```
$ docker ps # Solo para buscar id contenedor
$ docker exec -it id bash
```

* Una vez dentro del contenedor del panel o el ws (es la manera correcta de reiniciar el panel o ws en el supervisor, NO EJECUTAR SERVICE SUPERVISOR)
```
$ supervisorctl stop panel
$ supervisorctl start panel
```
O un restart 
```
$ supervisorctl restart ws
```
O en su defecto para mas rapidez, si no hay que hacer un reload menu, ni nada que amerite entrar en el contenedor puede reiniciarse el contenedor de de la siguiente forma:
```
$ docker exec -it id supervisorctl restart panel
```

Docker usa como volumenes los repositorios, por eso no se deden reiniciar los contenedores


* Para ejecutar sentencias dentro de un contenedor sin entrar en el
```
$ docker exec -it id supervisorctl status
```

# Notas importantes
Los proyectos corren con variables de entorno, eso quiere decir que para hacer un reload menu por ejemplo no debemos editar el settings, eso se hace modificando la variabel de entorno directamente y luego colocandola en su valor original.

Ejemplo:

```
// CONTAINER ID
// panel1 4bd7961d35f5

$ docker exec -it 4bd7961d35f5 bash

# env | grep PANEL_ADD_MENU
PANEL_ADD_MENU=False

# export PANEL_ADD_MENU=True
# env | grep PANEL_ADD_MENU
PANEL_ADD_MENU=True

# python manage.py runscript reload_menu
Recargando informacion del menu
Menu actualizado con exito....

// Dejamos la variable como estaba
# export PANEL_ADD_MENU=False
# env | grep PANEL_ADD_MENU
PANEL_ADD_MENU=False
```

O de forma simplificada:
```
export PANEL_ADD_MENU=True && python manage.py runscript reload_menu && export PANEL_ADD_MENU=False
```

Es la forma correcta de hacer un reload_menu, y para ejecutar algun script en produccion


# Como escalar

```
docker-compose scale panel=2
docker-compose up -d --force-recreate
```

# Entonacion basica de nginx:

El parametro worker_processes, debe ser igual al resultado de:
```
cat /proc/cpuinfo | grep processor | wc -l
```

El parametro worker_connections, deber ser igual al resultado de:
```
ulimit -n
```

# Generacion de certificado ssl:

Generar key RSA de 2048 bits
```
openssl genrsa -des3 -out nginx.key 2048
```
Clave usada
```
miprimeraRSA :) con otra cosa: 4&E%4DS!^dV#Ka9hcg^f
```

Generar certificado (LLenar los datos solicitados)
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx.key -out nginx.crt
```

Enviar archivo por la consola:
```
scp 201510210205_admin_parley.backup lzambrano@192.168.1.126:~/
```

Capturas en tcpdump:
```
sudo tcpdump -A -i docker0 tcp and host 172.17.42.1 and port 80 > data-gzip-disabe.txt
```

Instalar para poder generar el modelo relacional en grafico:
```
apt-get install graphviz graphviz-dev pkg-config
(venv)$ pip install pygraphviz
```

Solucionar problemas al iniciar docker:
```
sudo rm -r /var/lib/docker/network
```