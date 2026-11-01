# Canvis

El format segueix [Keep a Changelog](https://keepachangelog.com/). Les versions del complement són les de `addon.xml`. Una etiqueta `vX.Y.Z` al repositori publica el zip d'aquella versió a GitHub Releases.

## [1.0.2] - 2026-11-01

- Nova secció **Infantil**: SX3 en directe, programes del canal SX3, franges per edat (codi Infantil, tots els públics, a partir de 7 i de 10 anys) i destacats del web del SX3.
- La secció té dibuixos originals i acolorits (icona, pòster, fanart, bàner i paisatge) pensats per a criatures. El logotip oficial del SX3 només es mostra com a marca petita. Les llistes s'obren com a sèries perquè les pells puguin usar vistes de pòster.
- No s'hi barregen tots els programes «+7» del catàleg general: aquest codi és una edat mínima, no una marca infantil. Les franges de 7 i 10 anys es limiten al canal SX3.
- **Cerca per veu:** obre el teclat de Kodi perquè el micròfon del sistema o del comandament hi pugui dictar. No hi ha API de micròfon per als complements. La cerca tolera accents i errors petits.
- **Continua mirant:** historial i punt de represa només en aquest dispositiu, amb programes semblants segons la temàtica. Es pot desactivar i esborrar.

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
