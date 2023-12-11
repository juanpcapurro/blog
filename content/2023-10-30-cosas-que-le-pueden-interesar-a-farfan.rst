######################################
Cosas que le pueden interesar a farfan
######################################
:date: 2023-10-30
:status: draft
:slug: cosas-que-le-pueden-interesar-a-farfan
:summary: no, no puedo ir a un podcast si no tengo notitas
:tags: programming, cycling
:author: capu
:featured_image:

Farfán tiró que iba a invitar a un 'master jedi de monero', que vendríá a ser
yo. Voy a intentar tirar un poco de data y estar a la altura antes de que nos
distraigamos irreversiblemente hablando de skid patches o algo.

Outline sobre monero
====================

Es una criptomoneda basada en blockchain y UTXOs que hace a la privacidad su
prioridad #1. Es el estado del arte de la privacidad en internet, y lo pueden
usar por menos de diez centavos de dolar por transacción.

Como logra la privacidad
------------------------

En la blockchain:

- stealth addresses: yo no te pago a tu address (el string que me pasas
  diciendome 'che pagame acá') sino a una one-time-address que es un secreto
  compartido entre vos y yo (derivado de mi clave privada y tu clave publica)
  solamente. Vos, para saber si recibiste la transaccion, no te queda otra que
  mirarlas todas.
- ring signatures: Cuando gasto un output, tambien incluyo en la transacción 11
  _decoys_ (señuelos?) que no son mios, junto con una prueba de que estoy
  gastando uno (y solo uno) de ellos. De acá sale que los ataques sobre Monero
  en general son heurísticos, es decir, juegan con encontrar la _probabilidad_
  de que estes gastando X output.
- ringCT: El mecanismo para ofuscar de que cantidad son los outputs usados en
  una transacción. Previamente, monero funcionaba parecido a los billetes: habia
  un par de denominaciones de outputs (0.05, 0.1, 1, 2, 5) y para cada output
  que querias gastar ponias varios decoys de la misma denominacion. Esto es un
  shenanigan matematico para probar que sale la misma cantidad de dinero que
  entra, sin revelar cual es. Y está above my paygrade, perdón.
- Homogeneidad de transacciones: todas las transacciones se ven mas o menos
  igual, de la misma forma que todos los tor browsers se ven mas o menos igual.
  Al no haber mas de una forma de hacer una transaccion, no se filtra
  información de qué wallet usas.

Por fuera de la blockchain:

- La experiencia por defecto de usar monero es bajarte la `monero-gui-wallet
  <https://www.getmonero.org/downloads/>`_ , que baja y verifica todos los
  bloques y levanta un full node. Al tener un full node, tenes plausible
  deniability cuando mandas una transaccion, porque podes estar transmitiendo
  una tuya o forwardeando una de alguien mas.


Alternativas
------------
- ETH: tiene stablecoins, prestamos, rulos, todo. Algunas personas comprometidas
  con triggerearme lo llaman 'the future of banking'. Pero es trivial, para
  actores con nada de conocimiento tecnico, de seguir el sueldo de cada uno de
  ustedes. Están a una avivada de un quilombón.
- ETH con Tornado: Por fuera de las conversaciones con el CBP que les puede
  causar, tienen tambien un monton de bordes filosos con los que pueden pinchar
  su seguridad operacional. Si no tienen su propio nodo, infura ya los tiene
  presos.
- BTC: sweetspot de escalabilidad a futuro, programabilidad/extensibilidad, y
  simpleza. Pero no hace de la privacidad su prioridad #1 y actores con muy poca
  sofisticación pueden trackear transacciones (aunque no es *trivial* como en
  ethereum). Esto se puede hacer mas dificil con `algunas ofuscaciones
  <https://bitcoinmagazine.com/technical/a-comprehensive-bitcoin-coinjoin-guide>`_
  , pero crucialmente la privacidad no está enforzada por defecto.

Limitaciones
------------
Monero en pos de maximizar privacidad hace muchos sacrificios que otros
proyectos no tienen que hacer

- Programabilidad: Nunca miraron en la dirección de turing-completeness de
  Ethereum, e incluso cosas que estan establecidas en Bitcoin son todavía muy
  imprácticas (multisigs) o AFAIK imposibles (LN). Stablecoins, timba,
  prestamos, están fuera de discusión.
- 'ta gordito: En Bitcoin, podes no correr un nodo y que no te caguen
  bastante facil (explicado como Simple Payment Verification en el whitepaper).
  Para obtener todos los beneficios de XMR tenes que tener tu propio nodo
  synceado con la red, cosa que puede tomar 1-2 dias.
- Escalabilidad: A largo plazo, el protocolo va a tener que innovar en como
  hacer que siga siendo usable la red con mas datos pasando por ella. En mi
  compu está tomando 1s indexar cada bloque actual. Y hay un bloque cada 120s.
  Si la red hace un 120x en volumen, tengo que cambiar la compu o quedarme
  afuera. Es importante recordar que ademas de ser una solucion tecnica, monero
  es una construcción social que tuvo network upgrades cada 6 meses y los puede
  volver a tener.


Recursos
========
Ninguno de estos son affiliate links, soy pestañeador profesional:

- https://masteringmonero.com/ -- libro introductorio, por uno de los lead
  contributors
- `Playlist de 'breaking monero'
  <https://invidious.no-logs.com/playlist?list=PLsSYUeVwrHBnAUre2G_LYDsdo-tD0ov-y>`_
  , deep dives tecnicos a un par de temas, `hosteada como podcast
  <https://static.capu.tech/other/breaking-monero/feed.xml>`_ by yours truly
- https://trocador.app/  -- agregador de exchanges sin KYC ni JS, bien esquizo
- https://fixedfloat.com/ -- exchange sin KYC, pero mas 'normal'
- https://kycnot.me/ -- directorio de servicios sin kyc, que aceptan monero

Zona de gordos bicicleta
========================

están `mis bicis <{filename}/pages/mis-bicis.rst>`_ , la `bici de carga
<{filename}/2022-06-12-ladecarga.rst>`_, la `chill machine
<{filename}/2023-05-09-chomk-machine.rst:1>`_ (que ahora está extra gordita,
con neumaticos de 2.1)

Algunos viajecitos
------------------
