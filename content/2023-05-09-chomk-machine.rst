#######################################################
Hackeando completamente mi cuadro tope inferior de gama
#######################################################
:date: 2023-05-09
:summary: No me gusta la geometría del fad nottingham y alta paja hacerme un instagram para comprar
          otro tipo de cuadro
:tags: cycling, meatspace-hacking
:author: capu
:featured_image: /chomk-machine/photo_2023-05-08_19-52-45.jpg

...Hacía falta todo esto?
=========================
Sí. En mi ultimo viaje, desde playas doradas hasta Trelew, estuve corto de neumáticos. O sea, pude
viajar bien y llegué, pero en Punta Pórfido sentí que en cualquier momento iba a cortar una sidewall
al carajo, y no quiero quedarme a pata en ese tipo de lugares. Y en el ripio entre Madryn y Trelew
hubiera apreciado flotar algo más sobre las piedritas.

Seguir usando las mismas llantas estaba afuera de la pregunta, dado que el FAD Lord que empezó
siendo la chill machine se banca en teoría 622x32 como máximo, y con los schwalbe g-one de 35mm ya
estaba jugado, ejemplo, no pudiendo usar todo el dropout.

Iba a tener que hacer una conversión.

Conversión? cómo
================
Una conversión puede referirse a dos cosas:

- Armar una bici piñon fijo a partir de una rutera con dropouts horizontales (o Advanced Hackery)
- Cambiar el tamaño de llanta de un juego de ruedas para poder meter neumáticos más gorditos
  (convirtiendo de un rodado más chico a uno más grande) o para tener menos masa rotativa y ruedas
  más livianas (la gente a veces hace esto cuando convierte mountain bikes de los 90 a *gravel
  bikes*)

Yo voy a poner llantas mas chicas para poner neumáticos más gorditos.

Consideré armar ruedas 559 (26", para los que aman la ambigüedad) para darle un hogar a unas wtb
weirwolf 2.1 que vengo acarreando desde 2019, pero juzgué que iba a ser dificil seguir consiguiendo
neumáticos buenos en el futuro, y no está bueno perder distancia al piso cuando la transmisión es
piñón fijo. Además que ni idea si se consiguen llantas para tubeless en esa medida.

Entonces, fui por 584 (27.5" / 650B )

.. image:: {static}/chomk-machine/photo_2023-05-08_19-53-24.jpg

Lo mas chico tubeless-compatible que encontré fueron unas maxxis beaver en 50mm (2 freedom thumbs).

La rueda, con esas cubiertas, me debería quedar de un radio apenas mas chico que con los neumaticos
actuales:

.. code::

    (current_rim_diameter/2)+current_tire_size
    (622/2)+35
    346

    (next_rim_diameter/2)+next_tire_size
    (584/2)+50
    342

\... entonces debería andar, imaginé. No me puse a ver en detalle cómo iba a ir de ancho, dado que
no tenia una forma facil de estimar dónde iba a tener qué ancho la cubierta, entonces medio que me
la jugué.

.. image:: {static}/chomk-machine/photo_2023-05-08_19-52-25.jpg
    :alt: la rueda trasera puesta en la bici rozando las seatstays, de lejos

oops.

.. image:: {static}/chomk-machine/photo_2023-05-08_19-52-22.jpg
    :alt: la rueda trasera puesta en el cuadro sin modificar, closeup

Resulta que ni siquiera poniendola lo mas lejos posible en el forkend llega a girar sin tocar.

El plan
=======
Lo que hice fue:

- diseñar un jig para separar las 'stays usando toda la ventaja mecánica que pueda conseguir
- cortar los puentes entre las seatstays y las chainstays
- separar las 'stays
- re-alinear el cuadro
- soldar puentes nuevos (aproveché a ponerle agarres de verdad para un rack)

El jig
------
Diseñé piezas en 3d con agujeros para que pasen varillas roscadas y un lugar para que apoye todo un
lado de los distintos caños. Las chainstays son de 16-17mm y las seatstays de 12-13mm.

No confié en que el plástico se banque la fuerza de las tuercas, entonces corté tambien unas
planchuelas para que distribuyan la fuerza sobre el plástico y no busquen doblarlo.

Lo que quise maximizar fue:

- No deformar localmente el caño (colapsarlo, kinkearlo), por eso el plástico que lo agarra en un
  área considerable
- No tener que deformar el caño en otro lugar para darle forma donde quiero. Consideré otros
  approaches con una crowbar y un poco de paracord pero tenía pinta de terminar mal.

.. image:: {static}/chomk-machine/blender.png
    :alt: un screnshot (en blender) de la pieza impresa en 3d para el jig

.. image:: {static}/chomk-machine/IMG_20230502_143443_167.jpg
    :alt: el jig antes de separar las seatstays

Es como una prensa de matambre inside-out.

.. image:: {static}/chomk-machine/IMG_20230502_144108_412.jpg
    :alt: el jig habiendo separado un poco las seatstays

.. image:: {static}/chomk-machine/IMG_20230502_150301_685.jpg
    :alt: jig separando las chainstays, visto desde arriba

Con esa separación, pude meter la rueda ✨

.. video:: {static}/chomk-machine/video_2023-05-09_13-23-35.mp4

Alineación
----------

Ya en este punto, le pegué una alineada siguiendo `la guia de Dios Sheldon
<https://www.sheldonbrown.com/frame-spacing.html>`_

.. image:: {static}/chomk-machine/photo_2023-05-08_19-52-58.jpg
    :alt: alineando el cuadro full low tech

Soldación
---------

Y me puse a agregarle los puentes:

.. image:: {static}/chomk-machine/photo_2023-05-08_19-52-45.jpg
    :alt: capu soldando

Resulta que hice super beefy el chainstay bridge y me quitó espacio para el plato, entonces lo tuve
que amolar casi enteramente de un lado, y encima después de eso aplicarle coerción `como la vez
pasada <{filename}/chainstay-coercion.rst>`_ para que pueda pasar con lo que moví la chainstay hacia
afuera. Tuve a mi hábil recomendador ayudándome:

.. image:: {static}/chomk-machine/photo_2023-05-08_19-53-09.jpg
    :alt: tebo aplicando coerción a las chainstays

\... y parece que pasa.

.. image:: {static}/chomk-machine/photo_2023-05-08_19-53-05.jpg
    :alt: clearance con el platopalanca, visto desde las chainstays

Qué queda
=========

En 1-2 semanas imagino que voy a poder tener otro update, pero la bici no está terminada. Le falta:

- Terminar de armar la rueda delantera y ver que no haya problemas de espacio ahí tampoco
- Agregarle un punto de soldadura en el seatstay bridge para que el anclaje de rack quede más sólido
- Alinearla de nuevo.
- Pintarla (tuve por primera vez en la vida una preferencia estética y la voy a intentar implementar)
- Ensamblarla
- Agregarle una montura de disco a la horquilla -- esto probablemente lo postergue dado que no
  necesito la redundancia de frenado si no tengo un rack trasero ni una relación muy larga
- Pasar de freno v-brake a disco

Y seguro algo me olvido. Capaz flasho y le agrego monturas para más botellas o algo así.

Nos vemos la semana que viene. Probablemente con algo más del cyberespacio.
