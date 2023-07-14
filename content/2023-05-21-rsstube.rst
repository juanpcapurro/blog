########################################################
Un shellazo para hacer un podcast de un canal de youtube
########################################################
:date: 2023-05-21
:summary: something something Gordo Diferido
:tags: programming, fringe political views
:author: capu
:featured_image:

El problema
===========
Resulta que sigo el `stream de farfan <https://www.youtube.com/channel/UCwqNoD7cnB43zae2Y5TEanw>`_
pero soy más del formato de podcast, y suelo querer escuchar ese tipo de cosas en situaciones donde
tener la compu o una conexion a internet fiable es medio unwieldy. Entonces quiero poder consumirlo
como un podcast, en un cliente estandar (yo uso `antennapod <https://antennapod.org/>`_)

La solución
===========

- un directorio en mi server para exponer las cosas
- un `shellazo <https://github.com/juanpcapurro/dotfiles/blob/master/.scripts/makefeed>`_ que baja
  los archivos y genera un feed rss con eso
- literalmente nada mas (le falta tener imagenes, reportar la duracion de los episodios, un par de
  memitos así)

El resultado
============

http://static.capu.tech/other/farfan/feed.xml -- ahora puedo ser gordo diferido offline
softwareliberado  y ustedes tambien

lo que quiero mostrar es lo facil que es implementar la funcionalidad que querés cuando las
herramientas y estándares que hay por debajo son simples. Por fuera de estar rojoempastillado como
usuario, yo no tenia ninguna experiencia trabajando con rss ...ni mucho con xml for that matter, y
pude lograr la UX que quería en 2-3hs de intentar cosas.

En el proceso se me piantó un lagrimón al leer `lo que se imaginaban que iba a ser la web en el 2001
<https://www.rssboard.org/rss-enclosures-use-case>`_ , y lo facil de lograr que es comparado a la
maraña de servicios que te hacen correr sus clientes privativos con los que vivimos ahora.

Eso es todo por ahora, tengo un asado basado al que llegar todo mojado.
