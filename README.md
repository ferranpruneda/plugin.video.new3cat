# 3Cat per a Kodi

Complement de vídeo **no oficial** per a [3Cat](https://www.3cat.cat) (l'antiga TV3 / CCMA). Permet veure els canals en directe i el catàleg a la carta des de Kodi 20 o Kodi 21.

No està afiliat a la CCMA ni a 3Cat. Els drets dels continguts són dels seus propietaris.

## Què hi ha

- **Directes:** TV3, 3CatInfo (3/24), SX3, 33, Esport3, TV3CAT i els canals temàtics que publica 3Cat (amb el programa que s'està emetent, si l'API el facilita).
- **Catàleg:** categories del web (sèries, pel·lícules, documentals, SX3, actualitat, esports, cultura, música, cuines…), amb pòsters, fanart, sinopsi, durada i data.
- **Programes:** temporades i capítols. Si el programa només té una temporada, s'obre directament la llista de capítols.
- **Novetats** i **El més vist**, a partir de les mateixes llistes que fa servir el web.
- **Cerca** de programes i de vídeos.
- **Catàleg A-Z.**

La reproducció fa servir les adreces HLS, DASH o MP4 que ja publica l'API pública. Si un vídeo està protegit amb DRM, el complement ho diu i no el reprodueix. No s'intenta saltar cap protecció.

## Instal·lació (fitxer zip)

1. Descarrega `plugin.video.new3cat-1.0.0.zip` (l'artefacte de la GitHub Action, o genera'l tu amb l'script de sota).
2. A Kodi: **Complements → Instal·la des d'un fitxer zip** i tria el zip.
3. El zip ha de contenir la carpeta `plugin.video.new3cat/` a l'arrel. No el recomprimis a mà sense aquesta carpeta.
4. Recomanat: instal·la també **inputstream.adaptive** des del repositori oficial de Kodi. Cal per al DASH i millora l'HLS adaptatiu. Sense ell, els vídeos que tinguin MP4 progressiu es continuen reproduint, i l'HLS es prova amb el reproductor intern.

Idioma de la interfície: català, castellà i anglès. El català és l'idioma per defecte del complement; Kodi fa servir l'idioma que tinguis configurat si n'hi ha traducció.

## Com s'usa

- **Directes:** entra a la carpeta i tria un canal. La sinopsi mostra què s'està emetent.
- **Categories:** cada secció obre les files del web (novetats, col·leccions, el més vist d'aquella secció…). Un programa obre les temporades; un capítol o una pel·lícula es reprodueix.
- **Cerca:** escriu el text i tria si vols programes o vídeos.
- **Opcions del complement:** qualitat (automàtica, DASH o MP4), mida de pàgina, memòria cau, ordre dels capítols, avís de geoblocatge i canals temàtics.

## Limitacions

- Part dels directes (sobretot **TV3** i **SX3**) només es poden veure des de Catalunya o Espanya. Des de fora, 3CatInfo, 33, Esport3 i TV3CAT solen respondre; si el teu punt de xarxa no hi té dret, Kodi rep un error del servidor i el complement avisa que pot ser una restricció geogràfica.
- El DRM no es reprodueix.
- Els pòdcasts i la ràdio no s'inclouen: és un complement de vídeo.
- La secció **EVA** no surt al menú perquè, en el moment de fer el complement, el frontal públic d'aquesta secció tornava buit. **Entreteniment** es llista pel filtre de temàtica de l'API.
- L'API de programa sovint només anuncia la temporada en emissió. El complement comprova també les temporades anteriors (`PUTEMP_1`, `PUTEMP_2`…).

## Generar el zip

Des de l'arrel del repositori:

```bash
bash scripts/build-zip.sh
```

El fitxer queda a `dist/plugin.video.new3cat-1.0.0.zip`.

## Proves

Els tests no necessiten Kodi. N'hi ha d'unitat (sense xarxa) i de comprovació contra l'API pública:

```bash
python -m unittest discover -s tests -v
```

Cal connexió a Internet per als tests de `tests/test_live.py`.
