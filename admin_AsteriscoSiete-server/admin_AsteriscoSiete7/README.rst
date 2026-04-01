admin_asterisco7
================

Panel administrativo de Asterisco Siete (*7)

Uso de Django 1.8 suspendido, funciona bien, pero es bastante lento
al ejecutar migraciones, algo tiene en ese modulo, y mejor no me arriesgo :(

Instrucciones de uso
====================

#. Descargar la base de datos mas actualizada del servidor
#. Crear la db local y hacer el restore de la db descargada
#. Crear entorno virtual para python 3 >> virtualenv -p /usr/bin/python3 nombre_entorno_virtual
#. Para trabajar en nuestro entorno virtual >> source nombre_entorno_virtual/bin/activate
#. Instalar todas las dependendias necesarias para el proyecto >> pip install -r requerimientos.txt
#. Añadir la db creada en el settings.py
#. Aplicar todos los cambios >> python manage.py migrate
#. Ejecutar el proyecto >> python manage.py runserver_plus
#. Se aplico una manera automatica de generar los permisos, para poder tener acceso a todos los url de manera limpia sin aplicar permiso por permiso, acceda al administrador de django busque su usuario (el del panel de Asterisco Siete) y procesa a colocarlo como super usuario.


Notas importantes
=================

#. Prohibidos los filtro a los pks de los modelos con la convercion a entero int(), por el momento la mayoria son númericos pero con el tiempo se implementaran pks como los de las sessiones en la mayoria de las tablas para alargar su vida util. usar formularios con tipos enteros por el momento o usar un "{0}".format(pk)

#. Hacer los filtros de manera adecuada, por ejemplo Equipos.objects.filter( deporte_id = pk_deporte ), NOT Equipos.objects.filter( deporte__pk = pk_deporte ) xq eso creara un join mas, lo cual no es optimo, esto aplicado a todo tipo de filtros, tener en cuenta.

#. En los Js tambien se imprimen los url de la manera {% url "my_ulr" %}, ya que se aplica una manera muy estricta de la permisologia y no pueden quedar cabos sueltos, internamente django si no detecta permiso a ese link devuelve un texto #404-page-not-found" que no lleva a ningun lugar, los enlaces tambien deben tener su url definida de esa manera, ya que al posees ese url en JS se ponen invisibles, los urls de los listar genericos deben llevar su url completa para que django sepa hacer esa validacion.

#. Para el lanzamiento en servidores usar el collectstatic, asi los archivos estaticos se mantendran en una sola ubicacion sin tener 2 enlaces con ngix

#. Cada ves que se este en proceso de migracion de una app y halla codigo que se deba eliminar pero que aun no es conveniente añadir una nota con un warnig para recordarlo luego

#. Las migraciones de las apps se ejecutan con >> python manage.py makemigrations nom_app, :) asi nada mas, sea inicial o no, ya no es necesario preocuparnos por las secuencias numericas tampoco.

#. Para hacer migraciones de datas, los MALOTES, se deben ejecutas usando django_extensions, muy util, ya hay un primer ejemplo, los archivos se añaden en el modulo scritps.

#. La libreria para impresiones en PDF pisa, obligatoriamente a sido actualizada a xhtml2pdf; por lo tanto usaremos esa, pero a dicha libreria le faltan ajustes para python 3 y django 1.7. me tome a la tarea de migrar dicho proyecto ya que lo necesitamos, al instalarla, descargar desde https://github.com/eabg/xhtml2pdf y reemplazar la carpeta xhtml2pdf, o en caso contrario si tambien quieren contribuir los invito, clonen el repositorio y y hagan un enlace simbolico parecido a este: sudo ln -s /home/edwar/github/xhtml2pdf/xhtml2pdf/ /home/edwar/django-efectivo/python3/lib/python3.4/site-packages/xhtml2pdf/

#. El archivo del entorno virtual ubicado en /python3/lib/python3.4/site-packages/crequest/middleware.py debe actualizarse

Att:
Asterisco Siete (*7)
