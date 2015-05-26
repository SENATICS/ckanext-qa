ckanext-qa
=================

**Status:** En uso (datos.gov.py)

**CKAN Version:** 1.7.1+

Esta librería extiende ckanext-qa a modo de agregarle soporte para internacionalización del lenguaje.

**Requerimientos:** tener previamente instalada la extensión ckanext-archiver y la extensión opendatagovpy. Para el entorno de producción es necesario tener levantado celeryd con supervisor.

* Guía de instalación de ckanext-archiver: https://github.com/ckan/ckanext-archiver
* Guía de instalación de ckanext-opendatagovpy: https://github.com/SENATICS/ckanext-opendatagovpy

Instalación QA
--------------

1. Activar el entorno virtual
  
  ```
  $ . /usr/lib/ckan/default/bin/activate
  ```
2. Ir al directorio de extensiones
  
  ```
$ cd ckan/lib/default/src
```
3. Clonar el repositorio
 
  ```
$ git clone <repositorio-senatics-ckanext-qa>
```
4. Ingresar al directorio de la extensión e instalarla con pip

  ```
$ pip install -e ./
```
5. Agregar la extensión a la lista de plugins del catálogo en el archivo de configuración (development.ini/production.ini)

  ```
ckan.plugins = qa
```

Uso QA
------

1. Para actualizar los datasets a partir de la extensión se deberá levantar el servidor celeryd desde el directorio de ckan con el siguiente comando paster:

  ```
$ paster celeryd -c <path to CKAN config>
```
2. Luego se debe ejecutar el siguiente comando paster

  ```
$ paster qa update [dataset] -c <path to CKAN config>

  ```
donde **[dataset]** es el id del dataset actualizado, si se omite se actualizaran todos los datasets,
y ** path to CKAN config ** es la ubicación del archivo de configuración de CKAN.

  **Importante:** la actualización de la extensión qa siempre debe realizarse después de la actualización del archiver.

  * Para conocer las demás funcionalidades del comando paster para la extensión archiver ejecutar

  ```
$ paster qa --help
```

  * Para verificar ir a la página de aseguramiento de calidad en: http://localhost:9000/qa

  Al finalizar la instalación de esta extensión se tendrá una página /qa con información importante respecto a la calidad de los recursos y conjuntos de datos. También se
podrá observar la categorización de los recursos en sus respectivas páginas. Sin embargo, no se tendrá la categorización a nivel de datasets ni soporte para varios idiomas.

  Para completar la instalación es necesario contar con la extensión **ckanext-opendatagovpy** que agrega tres características adicionales a qa: soporte para iternacionalización (inglés y español), categorización a nivel de datasets y facets.

1. Ingresar al directorio de la extensión opendatagovpy y ejecutar el comando de internacionalización

  ```
$ paster translations merge -l es -c /home/rparra/ckan/etc/default/development.ini
```
2. Después de actualizar archiver y qa respectivamente, para que los cambios puedan ser visibles completamente en el catálogo de datos, se debe re indexar el índice.
Para re indexar el índice ir al directorio de CKAN y ejecutar el siguiente comando:

  ```
$ paster search-index rebuild --config=/etc/ckan/default/development.ini
```
3. Reiniciar el servidor con el comando paster

  ```
$ paster serve /etc/ckan/default/development.ini
```

Automatización QA
-----------------

**Observación:** Primero debe asegurarse de tener configurado el servidor celeryd con supervisor (como se explica en la extensión archiver).

1. Tener levantado el servidor celeryd con supervisor.
2. Agregar al cron el comando paster que realiza las actualizaciones automáticamente cada cierto período de tiempo. Para esto, ingresar al crontab de la siguiente manera:

  ```
sudo crontab -e -u ckan
```
**Observación:** la llamada a este proceso se realiza con el mismo usuario con el que se configuro el archivo celeryd-supervisor.conf (ckan en el ejemplo)

3. Agregar la siguiente línea al crontab:

  ```
# m  h  dom mon dow   command
*/30 *  *   *   *     <path to PASTER command> --plugin=ckanext-qa qa update --config=<path to CKAN config>
```

  donde **path to PASTER command** es la ubicación del comando paster dentro del entorno virtual,
y **path to CKAN config** es la ubicación del archivo de configuración de CKAN.

  **Observación:** tener en cuenta que la actualización de la extensión qa debe realizarse una vez que se haya realizado la actualización de la extensión archiver.

4. Adicionalmente agregar el comando paster para re indexar el catálogo luego de los procesos anteriores

  ```
# m  h  dom mon dow   command
*/30 *  *   *   *     <path to PASTER command> --plugin=ckan search-index rebuild --config=<path to CKAN config>
```

  donde **path to PASTER command** es la ubicación del comando paster dentro del entorno virtual,
y **path to CKAN config** es la ubicación del archivo de configuración de CKAN.

* Para más detalles acerca de la extensión qa ir a: https://github.com/ckan/ckanext-qa
