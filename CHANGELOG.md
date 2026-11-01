# Canvis

El format segueix [Keep a Changelog](https://keepachangelog.com/). Les versions del complement són les de `addon.xml`. Una etiqueta `vX.Y.Z` al repositori publica el zip d'aquella versió a GitHub Releases.

## [1.0.3] - 2026-11-01

- Els menús i les pàgines de carpetes s'obren en mur amb informació (vista 54 d'Estuary, la mateixa a Kodi 20 i 21): menú principal, Infantil, Per edats, categories, lletres A-Z, l'índex d'El més vist i les files d'una secció. Aquestes llistes es marquen com a sèries (`tvshows`). Al mur amb informació d'Estuary 20 i 21, `videos` dibuixa el pòster dins una fitxa apaïsada de 316×218; `tvshows` el mostra a 290×415, sense encaixar un pòster vertical en aquella fitxa.
- Cada entrada d'aquestes pàgines té títol i descripció. Si 3Cat no en dóna, n'hi ha una d'escrita en català, amb traducció al castellà i a l'anglès.
- Directes, capítols, clips, novetats, cerca de vídeos i Continua mirant s'obren en llista ampla (vista 55).
- Les llistes de programes i les temporades es queden en mur (vista 500). El pòster es pot tornar a triar per a sèries, pel·lícules i temporades.
- L'opció única de vista se substitueix per tres (menús i categories, vídeos i directes, programes), i es manté la de forçar la vista. Qui havia canviat la vista global ho ha de tornar a triar. En altres pells no es força cap número.
- En tornar enrere, la pantalla recupera la vista que tenia. Les llistes no es desen a la memòria de Kodi, perquè si no el complement no es torna a executar i Estuary es queda amb la vista de la pantalla que s'acaba de deixar (els menús i els programes comparteixen el tipus `tvshows`). Si es desactiva «Força la vista», una vista triada a mà per a un tipus de pantalla es recorda i es torna a posar; amb l'opció activada, mana el valor per defecte d'aquell tipus.
- Art propi per a la icona, el fons, Infantil, els menús, les categories (i EVA), les lletres A-Z, la cerca i els set canals temàtics. Les fitxes de menú són pòsters 2:3, sense versions 16:9 ni icones d'adults. Els canals principals segueixen mostrant la imatge del programa en antena i el logotip oficial. Si un programa o un vídeo no porta imatge, es fa servir el pòster de reserva local en lloc de la imatge de 3Cat.

## [1.0.2] - 2026-11-01

- Nova secció **Infantil**: SX3 en directe, programes del canal SX3, franges per edat (codi Infantil, tots els públics, a partir de 7 i de 10 anys) i destacats del web del SX3.
- La secció té dibuixos originals i acolorits (icona, pòster, fanart, bàner i paisatge) pensats per a criatures. El logotip oficial del SX3 només es mostra com a marca petita. Les llistes s'obren com a sèries perquè les pells puguin usar vistes de pòster.
- No s'hi barregen tots els programes «+7» del catàleg general: aquest codi és una edat mínima, no una marca infantil. Les franges de 7 i 10 anys es limiten al canal SX3.
- **Cerca per veu:** obre el teclat de Kodi perquè el micròfon del sistema o del comandament hi pugui dictar. No hi ha API de micròfon per als complements. La cerca tolera accents i errors petits.
- **Continua mirant:** historial i punt de represa només en aquest dispositiu, amb programes semblants segons la temàtica. Es pot desactivar i esborrar.
- Les llistes s'obren en mur (vista 500 d'Estuary) per defecte. Es pot triar pòster o mur amb informació, o desactivar-ho. En altres pells no es força la vista.

## [1.0.1] - 2026-11-01

- Els menús, els avisos i les etiquetes de configuració es mostren en català encara que la interfície de Kodi sigui en un altre idioma.
- Nova opció «Llengua dels menús»: Català (per defecte) o la llengua de Kodi (català, castellà o anglès).
- Els noms de les categories conegudes es forcen en català, i les peticions a l'API demanen `Accept-Language: ca`.

## [1.0.0] - 2026-10-31

Primera versió instal·lable.

- Directes de TV3, 3CatInfo (3/24), SX3, 33, Esport3, TV3CAT i canals temàtics, amb el programa en antena quan l'API l'indica.
- Catàleg a la carta per categories del web, temporades i capítols, amb pòsters, fanart, sinopsi, durada i data.
- Novetats, el més vist, cerca de programes i de vídeos, i índex A-Z.
- Reproducció HLS, DASH o MP4 en clar. Avís si el flux pot estar limitat a Catalunya o Espanya. Els vídeos amb DRM no es reprodueixen.
- Interfície en català, castellà i anglès.
- Memòria cau de les crides a l'API i script per generar el zip.
