# 3Cat per a Kodi

Complement de vídeo **no oficial** per a [Kodi 20 (Nexus) i Kodi 21 (Omega)](https://kodi.tv/) que obre els continguts de [3Cat](https://www.3cat.cat) (l'antiga TV3 / CCMA).

No està afiliat a la CCMA ni a 3Cat. Els drets dels programes, les imatges i les marques són dels seus propietaris. El complement només consulta les API JSON públiques que ja fa servir el web i reprodueix les adreces HLS, DASH o MP4 que aquestes API retornen en clar. No esquiva el DRM ni les restriccions geogràfiques.

Codi i baixades: <https://github.com/ferranpruneda/plugin.video.new3cat>

## Què fa

Des del menú de complements de vídeo, 3Cat mostra aquestes entrades:

| Entrada | Què hi trobes |
| --- | --- |
| Directes | TV3, 3CatInfo (3/24), SX3, 33, Esport3, TV3CAT i els canals temàtics que publica 3Cat. La sinopsi mostra el programa en antena quan l'API el facilita, amb imatge de paisatge o pòster. |
| Infantil | Racó dels petits, amb dibuixos acolorits. El SX3 en directe, els programes del canal i franges per edat. |
| Novetats | Els vídeos nous del frontal del web. Es poden reproduir directament. |
| El més vist | Les files de rànquing de vídeo del web (sèries, pel·lícules, documentals, SX3, esports, cuines…). Les files d'àudio i de pòdcast no es mostren. |
| Categories | Les seccions del web: sèries, pel·lícules, documentals, SX3, actualitat, esports, cultura, música, cuines, campus i entreteniment. Cada secció obre les files editorials (novetats, col·leccions, destacats). |
| Catàleg | Tots els programes, o filtrats per lletra (A-Z i #). |
| Continua mirant | El que has vist en aquest aparell, per reprendre-ho, i programes semblants. |
| Cerca | Primer escrius el text; després tries programes o vídeos. |
| Cerca per veu | Obre el teclat de Kodi perquè hi puguis dictar el nom d'un programa. |

Dins d'un programa hi ha les temporades i, a dins, els capítols. Si només hi ha una temporada, s'obre directament la llista de capítols. Les pel·lícules i la resta de vídeos solts es reprodueixen sense passar per temporades.

Les llistes fan servir el tipus de contingut de Kodi (`tvshows`, `seasons`, `episodes`, `movies`) perquè les vistes de pòster, fanart, paisatge i logotip de la pell funcionin. Quan l'API envia les dades, també s'omplen la sinopsi, la durada, la data d'emissió, la temporada, el capítol i la classificació per edats.

## Vista per defecte

A Kodi 20 (Nexus) i Kodi 21 (Omega), `addons/skin.estuary/xml/MyVideoNav.xml` declara les mateixes vistes: `50,51,52,53,54,55,500,501,502`. El mur amb informació és el control 54 (`View_54_InfoWall.xml`) i la llista ampla és el control 55 (`View_55_WideList.xml`). El mur és el 500 i el pòster el 51. El pòster només el mostra Estuary en sèries, pel·lícules i temporades; si es tria en una altra llista, el complement passa al mur.

Cada tipus de pàgina té la seva vista. Amb **Força la vista d'Estuary** activat (és el valor per defecte), després de construir la llista es crida `Container.SetViewMode` amb el número d'aquell tipus, també en tornar enrere. Les llistes no es guarden a la cau de directoris de Kodi: si es guardessin, enrere no tornaria a executar el complement i la pell es quedaria la vista de la pantalla anterior. Els menús i els programes són tots dos `tvshows`, així que Estuary no els pot recordar per separat. Si es desactiva l'opció, una vista canviada des del menú lateral es desa per a aquell tipus de pantalla (menús, vídeos o programes) i es torna a aplicar; el valor per defecte no la tapa. Si la pell no és Estuary, no es força cap vista. Cada element rep pòster, miniatura i icona, encara que l'API només hagi enviat una imatge.

| Pàgina | Vista per defecte |
| --- | --- |
| Menú principal, Infantil, Per edats, categories, lletres A-Z, l'índex d'El més vist i qualsevol pàgina de carpetes (les files d'una secció o del SX3) | Mur amb informació (54). El contingut de la llista és `tvshows`, perquè així Estuary dibuixa el pòster a 290×415 i un pòster 2:3 no queda dins la fitxa apaïsada de 316×218 que fa servir amb `videos`. Cada entrada té títol i descripció. |
| Directes, capítols, clips, novetats, cerca de vídeos, cerca per veu quan hi ha vídeos, Continua mirant | Llista ampla (55). |
| Programes (sèries), temporades, cerca de programes, Et pot agradar, i una fila que només conté programes | Mur (500). Es pot canviar a pòster. |

Les temporades es queden amb la vista de programes: no són un menú de seccions ni una llista de fitxers reproduïbles. Una cerca per veu que només troba programes fa servir la vista de programes; si barreja programes i vídeos, fa servir la llista ampla.

Als menús, si 3Cat ja envia una entradeta (com a les categories del web), es mostra aquella. Si no n'hi ha, o només repeteix el títol, el complement escriu una frase curta en català. Amb «La de Kodi» aquesta frase surt en castellà o en anglès. Cap entrada d'aquests menús queda sense sinopsi.

## Cerca per veu

Kodi no ofereix un micròfon als complements en Python. **Cerca per veu** obre el quadre de text de Kodi. Si el teclat o el comandament poden dictar, el text parlat entra en aquest quadre i el complement el busca.

| Aparell | Com funciona |
| --- | --- |
| Android, Android TV i Google TV | El teclat (Gboard o el de la televisió) té un micròfon. Al comandament, el botó de veu també escriu dins del quadre si el sistema ho permet. |
| Windows | Obre el teclat de Kodi. La dictada del sistema (Win+H) hi pot escriure si està activa. |
| macOS | Igual, amb la dictada del sistema. |
| Linux i la majoria de LibreELEC | No hi ha micròfon. L'entrada serveix igual per escriure. |

La cerca tolera accents i errors petits: «com si fos air» o «comsi fos ahir» s'acosten a «Com si fos ahir». També es prova el text sense accents. Si algú obre el complement amb `?action=voice&q=...`, es fa la cerca sense tornar a demanar el text.

## Continua mirant

Quan mires un vídeo, el complement apunta en aquest aparell el títol, el programa, la imatge i el minut on t'has quedat. Ho fa un servei que s'engega amb Kodi i només llegeix el reproductor. El fitxer és `history.json` dins la carpeta de dades del complement. No surt del dispositiu.

**Continua mirant** ensenya aquesta llista. Si queda prou vídeo, Kodi pot oferir reprendre. **Et pot agradar** busca altres programes de la mateixa temàtica a l'API de 3Cat; si no n'hi ha, fa servir el títol del darrer programa. Pots desactivar el registre o esborrar-lo a la configuració.

## Infantil

La secció **Infantil** és el racó dels petits, separat de la resta del catàleg. Les carpetes tenen dibuixos aprovats (icona, pòster 2:3, fons i bàner). El menú d'Infantil, el de Per edats i els destacats s'obren en mur amb informació; els programes de dins segueixen la vista de programes i conserven el pòster de 3Cat. El logotip oficial del SX3 només es fa servir com a marca petita (`clearlogo`).

## Imatges

Els menús, les categories, les lletres i la cerca fan servir pòsters 2:3 propis (`resources/media/`). No hi ha versions apaïsades ni icones separades per a aquestes seccions: la fitxa és el pòster i el fons de la secció és el fanart. La categoria SX3 reutilitza el pòster d'Infantil. Una categoria desconeguda fa servir el pòster genèric.

Els programes, els capítols, les novetats i els resultats de cerca continuen amb les caràtules de 3Cat. Si un element no en porta cap, el complement hi posa `resources/media/common/poster-fallback.png` i, de fons, `fanart.jpg`.

A **Directes**, TV3, 3CatInfo, SX3, 33, Esport3 i TV3CAT mostren la imatge del programa en antena i conserven el logotip oficial. Els canals temàtics tenen un pòster propi (Verdi Clàssics, Anime, Joc de cartes, Doraemon, Plats bruts, Vinagre(ta) i les càmeres del temps). Un canal temàtic nou fa servir el pòster genèric. Les lletres del catàleg, de la «#» a la Z, tenen cadascuna el seu pòster. L'especificació completa és a `docs/specs.md`.

- **SX3 en directe:** el canal infantil.
- **Programes del SX3:** tot el que l'API marca amb el canal `PUC_S3`.
- **Per edats:** el codi ètic `CE_IN` (Infantil) i, dins del SX3, `CE_TP` (tots els públics), `CE_07` (a partir de 7 anys) i `CE_10` (a partir de 10 anys).
- **Destacats del SX3:** les files del web infantil.

3Cat publica l'edat a `codis_etics` (`CE_IN`, `CE_TP`, `CE_07`, `CE_10`, `CE_12`, `CE_13`, `CE_16`, `CE_18`) i, als vídeos, també a `targets` (`PUT_INF`, `PUT_TOTS`, `PUT_ADULT`). Es pot filtrar amb `programestv?codi_etic=CE_IN`. El «+7» de tot el catàleg no és una secció infantil: inclou documentals i programes generals amb edat mínima 7. Per això les franges de 7 i 10 anys només agafen programes del canal SX3.

Els menús, els avisos i la pantalla de configuració surten **en català** encara que Kodi estigui en castellà o en anglès. A **Llengua dels menús** pots triar «La de Kodi» perquè els menús i els avisos segueixin l'idioma de Kodi (català, castellà o anglès; qualsevol altra llengua es queda en català). Els títols i les sinopsis dels programes arriben en català perquè així els publica l'API.

## Requisits

- **Kodi 20 o Kodi 21** en qualsevol plataforma (escriptori, Android, LibreELEC…). El complement demana `xbmc.python` 3.0.0, que és el de Python 3 d'aquestes versions.
- **Connexió a Internet.**
- **inputstream.adaptive**, del repositori oficial de Kodi, de la mateixa generació que el teu Kodi. No és obligatori per instal·lar el complement, però sí que és el reproductor adequat:
  - Amb ell, els directes HLS i el vídeo a la carta DASH (fins a 1080p, si 3Cat el publica) canvien de qualitat sols.
  - Sense ell, els MP4 progressius es continuen veient, i l'HLS es prova amb el descodificador intern de Kodi. El DASH sense MP4 de reserva no es pot obrir i el complement t'ho diu.

Per instal·lar inputstream.adaptive: **Complements → Instal·la des del repositori → Complements de vídeo de Kodi → InputStream Adaptive → Instal·la**.

Orígens desconeguts: Kodi només accepta un zip de fora del repositori si els tens activats. A la pell Estuary: **Configuració (engranatge) → Sistema → Complements → Orígens desconeguts**. Confirma l'avís.

## On baixar el zip

El fitxer es diu `plugin.video.new3cat-1.0.3.zip`. A l'arrel del zip hi ha d'haver la carpeta `plugin.video.new3cat/`. No el tornis a comprimir pel teu compte.

1. **GitHub Releases (la via recomanada).** Quan es puja una etiqueta `vX.Y.Z` (per exemple `v1.0.3`), la GitHub Action publica una release amb el zip adjunt: <https://github.com/ferranpruneda/plugin.video.new3cat/releases>. Baixa el zip d'aquesta pàgina, no el «Source code» que genera GitHub (aquell no és un complement instal·lable).
2. **Artefacte de la GitHub Action**, útil abans de la primera etiqueta o per provar un commit concret. Obre la pestanya [Actions](https://github.com/ferranpruneda/plugin.video.new3cat/actions), entra a l'execució verda del commit i baixa l'artefacte `plugin.video.new3cat`. GitHub el guarda 90 dies. L'artefacte és un zip que *conté* el zip del complement: obre'l i instal·la el `plugin.video.new3cat-*.zip` de dins.
3. **Construir-lo tu**, si tens el codi. Mira [Construir el zip i executar les proves](#construir-el-zip-i-executar-les-proves).

## Instal·lar des d'un zip (Kodi 20 i 21)

1. Copia el zip al dispositiu on corre Kodi (un USB, la carpeta de baixades o una carpeta compartida).
2. Activa **Orígens desconeguts**, com s'explica a Requisits, si encara no ho has fet.
3. Ves a **Configuració → Complements → Instal·la des d'un fitxer zip**.
4. Localitza `plugin.video.new3cat-1.0.3.zip` i accepta'l.
5. Quan Kodi digui que s'ha instal·lat, obre **Complements → Complements de vídeo → 3Cat**.

A LibreELEC i a la majoria d'Android el camí dels menús és el mateix. Si el navegador de fitxers no veu el zip, copia'l a l'emmagatzematge que Kodi ja mostra (per exemple `Android/data/org.xbmc.kodi/files/` o una font SMB que hagis afegit).

## Actualitzar

1. Baixa el zip de la release nova (la versió de `addon.xml` ha de ser més alta que la que tens instal·lada).
2. Torna a fer **Instal·la des d'un fitxer zip** i tria el zip nou. Kodi substitueix el complement.
3. Si Kodi diu que el complement ja està instal·lat i la versió no ha pujat, desinstal·la'l primer: **Complements → Complements de vídeo → 3Cat → Informació → Desinstal·la**. Les opcions es desen a `addon_data` i es mantenen. Després instal·la el zip.

No cal esborrar la carpeta de dades per una actualització normal.

## Opcions

**Complements → Complements de vídeo → 3Cat → Configura.**

| Opció | Per defecte | Què fa |
| --- | --- | --- |
| Llengua dels menús | Català | Menús i avisos en català, passi el que passi amb l'idioma de Kodi. «La de Kodi» els passa al català, al castellà o a l'anglès de la interfície. La pantalla de configuració es llegeix sempre en català. |
| Qualitat de reproducció | Automàtica | Automàtica: DASH si hi ha inputstream.adaptive, si no el MP4 més alt, i HLS als directes. DASH força el manifest adaptatiu (amb MP4 de reserva si no hi ha inputstream). MP4 demana el fitxer progressiu, que és el més compatible. |
| Elements per pàgina | 24 (entre 8 i 60) | Quants programes, capítols o resultats de cerca s'ensenyen abans de «Pàgina següent». |
| Memòria cau de l'API (minuts) | 30 (entre 1 i 240) | Quant de temps es reutilitzen les llistes del catàleg. Els directes i les adreces de vídeo tenen una caducitat més curta, fixa al codi. |
| Ordre dels capítols | Del primer capítol | Del primer al darrer, o a l'inrevés. |
| Avisa si un vídeo pot estar limitat geogràficament | Activat | Mostra un avís quan l'adreça triada no és la del teu territori (per exemple TV3 des de fora d'Espanya). |
| Mostra els canals temàtics en directe | Activat | Afegeix a Directes els canals ràpids (anime, cinema, etc.) que 3Cat publica a part dels sis canals principals. |
| Desa el que miro en aquest dispositiu | Activat | Guarda en local el punt on has deixat cada vídeo. No s'envia enlloc. |
| Esborra l'historial d'aquest dispositiu | — | Esborra aquesta llista. No es pot desfer. |
| Força la vista d'Estuary | Activat | A la pell Estuary (Kodi 20 i 21) aplica la vista de cada tipus de pàgina. En altres pells no es força cap número. |
| Menús i categories | Mur amb informació | Vista 54. També es pot triar mur (500), pòster (51, només on Estuary el permet) o llista ampla (55). |
| Vídeos i directes | Llista ampla | Vista 55, per a directes, capítols, clips, novetats i Continua mirant. El pòster, en aquestes llistes, passa al mur. |
| Programes | Mur | Vista 500, per a sèries, temporades, cerca de programes i Et pot agradar. El pòster (51) aquí sí que el mostra Estuary. |

## Geolocalització i DRM

3Cat decideix l'adreça segons el territori que declara `https://dinamics.ccma.cat/geo.json` (`CATALUNYA`, `ESPANYA` o `TOTS`).

- Si hi ha una variant del teu territori, es fa servir aquesta.
- Si la teva variant és mundial (`TOTS`), no es mostra l'avís encara que tu siguis a Catalunya: aquella adreça es pot veure des de qualsevol lloc.
- Si des de fora només hi ha variant de Catalunya o d'Espanya, el complement igualment prova la més ampla i avisa. El servidor de 3Cat pot respondre `403 geofence:blocked`. Això no és un error del complement.
- Quines cadenes tenen variant mundial canvia sense avís. En una comprovació amb `geo` = `TOTS`, TV3 oferia una adreça mundial (el senyal internacional), i SX3, 33, 3CatInfo i TV3CAT també. Esport3 només oferia Catalunya i Espanya. Una pel·lícula pot estar limitada encara que un capítol antic no ho estigui: depèn de cada fitxer.

El DRM no es tracta. Si l'única adreça que retorna l'API sembla Widevine, PlayReady o un manifest protegit, el complement mostra «Aquest vídeo està protegit amb DRM i no es pot reproduir» i no demana cap llicència.

Els pòdcasts, la ràdio i la secció EVA no surten al menú. EVA no tenia frontal públic amb contingut quan es va escriure el complement. Entreteniment es llista pel filtre de temàtica de l'API, no per les files editorials del web. L'API de programa sovint només anuncia la temporada en emissió; el complement també comprova `PUTEMP_1`, `PUTEMP_2`, etc., i ho desa a la memòria cau.

## Resolució de problemes

| Símptoma | Què provar |
| --- | --- |
| El vídeo no s'obre o es queda negre | Instal·la inputstream.adaptive. A la configuració, prova **MP4 (màxima compatibilitat)**. |
| Avís de geoblocatge i tot seguit error de reproducció | El contingut no s'emet al teu país. Prova 3CatInfo o TV3CAT, que sovint tenen senyal internacional. No es pot desbloquejar des del complement. |
| Missatge de DRM | 3Cat no ofereix una còpia en clar. No hi ha res a configurar. |
| «No s'ha pogut connectar amb 3Cat» | Revisa la xarxa. Torna-ho a provar al cap d'una estona: les API de vegades responen 5xx. |
| Llistes buides o antigues | Puja o baixa els minuts de memòria cau, o esborra la cau (més avall). |
| Kodi diu que el zip no és un complement | Has baixat el codi font de GitHub o l'artefacte sencer. Cal instal·lar el zip que conté la carpeta `plugin.video.new3cat/`. |
| La cerca no troba res | Prova l'altra opció (programes o vídeos). La cerca de programes no inclou notícies. |

La cau és a la carpeta de dades del complement:

| Sistema | Carpeta |
| --- | --- |
| Linux | `~/.kodi/userdata/addon_data/plugin.video.new3cat/` |
| Windows | `%APPDATA%\Kodi\userdata\addon_data\plugin.video.new3cat\` |
| macOS | `~/Library/Application Support/Kodi/userdata/addon_data/plugin.video.new3cat/` |
| Android | `Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data/plugin.video.new3cat/` |
| LibreELEC / CoreELEC | `/storage/.kodi/userdata/addon_data/plugin.video.new3cat/` |

Esborra els fitxers `.json` d'aquesta carpeta amb Kodi tancat si una llista s'ha quedat encallada. No cal desinstal·lar el complement.

### Registres de Kodi

1. **Configuració → Sistema → Registre → Activa el registre de depuració.**
2. Reprodueix el que falla, o obre la secció que queda buida.
3. Tanca el registre de depuració si no el vols deixar encès: els fitxers creixen de pressa.
4. Obre `kodi.log` i cerca `plugin.video.new3cat`. Les línies d'error de l'API queden amb aquest prefix.

| Sistema | Fitxer |
| --- | --- |
| Linux | `~/.kodi/temp/kodi.log` |
| Windows | `%APPDATA%\Kodi\kodi.log` |
| macOS | `~/Library/Logs/kodi.log` |
| Android | `Android/data/org.xbmc.kodi/files/.kodi/temp/kodi.log` |
| LibreELEC / CoreELEC | `/storage/.kodi/temp/kodi.log` (també pel compartit Samba `Logfiles`) |

A **Configuració → Sistema → Registre → Mostra el registre d'esdeveniments** pots llegir el final del log sense sortir de Kodi. Per enviar-lo, copia el fitxer; no cal enganxar-lo sencer si abans en filtres les línies `plugin.video.new3cat`.

## Estructura del projecte

```
addon.xml                 manifest de Kodi (versió, resum, llicència, codi font)
addon.py                  punt d'entrada
service.py                segueix el reproductor i desa el minut en local
icon.png / fanart.jpg     imatges del complement
resources/media/         pòsters i fons (menús, categories, lletres, directe temàtic, Infantil)
docs/                    especificació de l'art (no s'instal·la amb el zip)
CHANGELOG.md              històric de versions
README.md                 aquesta guia
LICENSE.txt               GPL-2.0-or-later
resources/settings.xml    opcions
resources/language/       català (ca_es), castellà (es_es), anglès (en_gb)
resources/lib/api.py      client HTTP de les API de 3Cat i memòria cau
resources/lib/parsing.py  imatges, durades i elecció d'adreça (sense Kodi ni xarxa)
resources/lib/cache.py    cau en memòria o en fitxers JSON
resources/lib/router.py   menús de Kodi i reproducció
resources/lib/history.py  historial local de reproducció
resources/lib/matching.py cerca tolerant a accents i errors de dictat
scripts/build-zip.sh      genera el zip instal·lable
tests/                    proves unitàries i proves contra l'API pública
.github/workflows/ci.yml  proves, artefacte i release
```

`parsing.py` i `api.py` no importen Kodi, així les proves es poden executar amb Python 3 normal.

## Construir el zip i executar les proves

Cal Python 3.9 o superior (el de Kodi 20/21 en té prou; per les proves, 3.11 va bé), `bash`, `tar` i `zip`. No cal instal·lar Kodi.

```bash
python3 -m unittest tests.test_parsing tests.test_api tests.test_strings tests.test_matching tests.test_history tests.test_views -v
python3 -m unittest tests.test_live -v
bash scripts/build-zip.sh
```

- `tests.test_parsing`, `tests.test_api`, `tests.test_strings`, `tests.test_matching`, `tests.test_history` i `tests.test_views` no necessiten xarxa.
- `tests.test_live` crida les API públiques de 3Cat. Comprova que les llistes tenen elements i que una adreça HLS o MP4 respon. Un 403 de geoblocatge en TV3, vist des de fora d'Espanya, és el resultat esperat i el test el té en compte.
- El zip queda a `dist/plugin.video.new3cat-1.0.3.zip`. El número surt de `version` a `addon.xml`. La carpeta `dist/` no es puja al git.

La GitHub Action fa el mateix a cada push i a cada pull request: executa les proves unitàries i puja el zip com a artefacte. Les proves en viu es deixen per executar-les en local, perquè depenen de la xarxa i del país del servidor de GitHub.

### Publicar una versió

1. Actualitza `version` a `addon.xml` i afegeix l'entrada a `CHANGELOG.md`.
2. Fes el commit i el merge.
3. Crea l'etiqueta amb el mateix número i una `v` al davant, i puja-la:

```bash
git tag v1.0.3
git push origin v1.0.3
```

4. La GitHub Action construeix el zip i crea (o actualitza) la [release](https://github.com/ferranpruneda/plugin.video.new3cat/releases) amb el zip adjunt. Fa servir el `GITHUB_TOKEN` del repositori; no cal cap secret addicional. L'etiqueta ha de dir-se `v` seguit de la versió, per exemple `v1.0.3`.

## Llicència

GPL-2.0-or-later. El text és a [LICENSE.txt](LICENSE.txt).
