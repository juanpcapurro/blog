#############################
Finalmente, tengo comentarios
#############################
:slug: tengo-comentarios-v1
:date: 2023-08-01
:summary: inventados completamente acá for fun & profit
:tags: programming
:author: capu
:featured_image:

La idea
=======
Antes de que ocurriera el merge de ethereum dije 'uh para cuando Ethereum deje
de tener Proof Of Work, MI BLOG VA A TENER'.
En ese momento estaba vibeando en Viedma, en un café esperando que pase el
viento para irme en bici a otro lado.

La idea es choreada del nakamoto consensus:

- Cuando posteas un comentario, tenés que serializar los datos del mismo
  (contenido, nombre, email de respuesta) de una forma estandar.
- En el chorizo serializado ese metés también un numerito falopa 'nonce', que
  tiene la unica función de ser variado sin tener que modificar el contenido en
  si.
- Calculás hashes de lo serializado anteriormente, y vas probando nonces hasta
  que el hash tenga, no se, los dos primeros bytes en 0. O alguna condicion
  arbitraria así. Para tener los dos primeros bytes en 0, como la funcion de
  hash no es predecible, no te queda otra que hacer algun numero de intentos
  entre 1 y 2^16
- Mandás el comentario serializado con el nonce que encontraste
- Mi servidor computa una vez el hash, si el resultado le da con dos ceros
  adelante, todo piola y el comentario se guarda. Si no da, el comentario se
  descarta y te devuelve un error HTTP 400

Luego la vida sucedió y recientemente recordé mi idea. No solo descubrí que el
approach que quiero lograr ya existe desde los 90 y se llama `hashcash
<http://www.hashcash.org/>`_, sino que `His Royal Hashness
<https://blog.lopp.net/protect-contact-forms-from-spam-with-proof-of-work/>`_ lo
tiene implementado para su pagina de contacto hace dos años.

La implementación (hasta ahora)
===============================
Me gasté en hacer el form de contacto bonito que pueden ver acá abajo, la 
logica y maquetado para mostrar los comentarios que ya están, y pasé todos los
caños para que se hablen entre si. Más un placeholder para el PoW de verdad, que
haré a continuación. Pero quería ir tirandole algo al mundo real, por tener las
metodologias ágiles brandeadas en la materia gris nomas. Y para ver que tan
gedes son mis amigos y los robots de la internet.

La infra
--------
Si bien laburé de sysadmin tecnicamente un rato, nunca me puse a aprender
ninguna cosa de 'infrastructure as code' o parecido. Mis objetivos para
administrar esto son:

- No meter herramientas innecesariamente complejas. Entender todo el stack que
  uso en consecuencia.
- Sin embargo, meter deployments reproducibles. No quiero que configurar el
  ambiente en el que está productiva la cosa sea lo suficiente un evento como
  para ameritar levantar un shell interactivo, y despues olvidarme como mierda
  lo hice.
  
Decidí usar un dockerfile, sin docker-compose ni nada parecido arriba, y mandar
las imagenes a mano por ssh. Es la definicion de mal proceso, porque tengo que
correr un total de 5 comandos, 3 de ellos por ssh, y están guardados en un
README que me voy a olvidar de actualizar. Pero no tengo que correr ``pip`` a
mano en el server ni preocuparme por tener versiones sutilmente distintas de las
cosas en produccion que desarrollando. No es como si mi webserver de 12 lineas
vaya a tener tantas sutilezas igual.

Estuvo bueno refrescar docker. Si le prestan atencion `al pr
<https://github.com/juanpcapurro/blog/pull/5>`_, está separado en dos
dockerfiles, uno que va a la internet y se trae el software, y otro que hace
configuracion especifica del proyecto. Recuerdo que hice eso así para poder
rebuildear el deployment y codear esto en el `tren patagónico
<https://trenpatagonicosa.com.ar/>`_ cuando lo tomé.

Agradezco comentarios en como habrían hecho ustedes para deployar de manera
prolija una cosa simple y chiquita como esta. Me tengo que meter en guix? nixos?
ansible?

Gracias por leer! Dejense un comentario. Porfis. Necesito QA.
