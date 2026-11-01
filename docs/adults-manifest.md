# plugin.video.new3cat: art d'adults i general (estil de paisatges terrosos)

Generat l'1 de novembre de 2026 a partir de `specs.md` / `specs.csv`, aplicant les decisions d'en Ferran. Les rutes de l'especificació `resources/media/<secció>/…` s'han desat com a `/workspace/new3cat-art-new/<secció>/…`, com ja es feia amb `kids/`.

**Fets:** 82 fitxers (46 NOU + 36 OPCIONAL) · **No fets:** 95 files (inclou 22 FET i 3 REUTILITZA).

Comprovació amb Pillow: tots els fitxers tenen la mida exacta de l'especificació. Pòsters: 480×720, PNG RGB opac. Fons: 1920×1080, JPEG RGB de qualitat 90.

Decisions aplicades: 1) pòster 2:3, sense versions 16:9; 2) els canals en directe es queden amb la imatge del programa; 3) es mantenen els logos oficials; 4) A–Z: una base i 27 lletres compostes amb Pillow (tipografia Oswald SemiBold); 5) un pòster per a cada canal temàtic, més el genèric de reserva; 6) EVA amb imatges pròpies; 7) sense icones d'adults.

Fulls de contactes: `contact-sheet-adults.png` (35 pòsters + 20 fons) i `contact-sheet-letters.png` (base + 27 lletres).

## Fitxers fets

| Fila CSV | Estat | Fitxer | Mida | Format/mode | Què representa | Contingut de l'especificació |
|---|---|---|---|---|---|---|
| 34 | NOU | menu/poster-live.png | 480×720 | PNG RGB | Entrada «Directes» del menú principal; el fanart també és el fons de la secció | Paisatge de turons amb una antena al cim que emet ones concèntriques. |
| 35 | NOU | menu/fanart-live.jpg | 1920×1080 | JPEG RGB | Entrada «Directes» del menú principal; el fanart també és el fons de la secció | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 38 | NOU | menu/poster-latest.png | 480×720 | PNG RGB | Entrada «Novetats» del menú principal; el fanart també és el fons de la secció | Albada sobre un camp llaurat amb un brot acabat de néixer en primer pla. |
| 39 | NOU | menu/fanart-latest.jpg | 1920×1080 | JPEG RGB | Entrada «Novetats» del menú principal; el fanart també és el fons de la secció | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 42 | NOU | menu/poster-rankings.png | 480×720 | PNG RGB | Entrada «El més vist» del menú principal; el fanart també és el fons de la secció | Tres turons d'alçades diferents com un podi, amb un estendard al més alt. |
| 43 | NOU | menu/fanart-rankings.jpg | 1920×1080 | JPEG RGB | Entrada «El més vist» del menú principal; el fanart també és el fons de la secció | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 46 | NOU | menu/poster-categories.png | 480×720 | PNG RGB | Entrada «Categories» del menú principal; el fanart també és el fons de la secció | Terrasses de conreu en franges de colors terrosos diferents, una per temàtica. |
| 47 | NOU | menu/fanart-categories.jpg | 1920×1080 | JPEG RGB | Entrada «Categories» del menú principal; el fanart també és el fons de la secció | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 50 | NOU | menu/poster-letters.png | 480×720 | PNG RGB | Entrada «Catàleg (A-Z i Tots els programes)» del menú principal; el fanart també és el fons de la secció | Camí que travessa la plana marcat amb fites de pedra en fila. |
| 51 | NOU | menu/fanart-letters.jpg | 1920×1080 | JPEG RGB | Entrada «Catàleg (A-Z i Tots els programes)» del menú principal; el fanart també és el fons de la secció | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 54 | NOU | menu/poster-continue.png | 480×720 | PNG RGB | Entrada «Continua mirant» del menú principal; el fanart també és el fons de la secció | Camí que es perd cap a l'horitzó amb un banc a mig recorregut i unes petjades. |
| 55 | NOU | menu/fanart-continue.jpg | 1920×1080 | JPEG RGB | Entrada «Continua mirant» del menú principal; el fanart també és el fons de la secció | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 58 | NOU | menu/poster-search.png | 480×720 | PNG RGB | Entrada «Cerca» del menú principal; el fanart també és el fons de la secció | Una lupa gegant sobre el paisatge que magnifica un arbre solitari. |
| 59 | NOU | menu/fanart-search.jpg | 1920×1080 | JPEG RGB | Entrada «Cerca» del menú principal; el fanart també és el fons de la secció | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 62 | NOU | menu/poster-voice.png | 480×720 | PNG RGB | Entrada «Cerca per veu» del menú principal; el fanart també és el fons de la secció | Vall entre dues muntanyes amb ones d'eco que reboten d'una a l'altra. |
| 63 | NOU | menu/fanart-voice.jpg | 1920×1080 | JPEG RGB | Entrada «Cerca per veu» del menú principal; el fanart també és el fons de la secció | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 76 | NOU | live/poster-fast-generic.png | 480×720 | PNG RGB | Canals temàtics (FAST) sense art propi | Petita cabana amb una antena i diverses finestres il·luminades de colors diferents. |
| 78 | OPCIONAL | live/poster-fast-tem1.png | 480×720 | PNG RGB | Canal temàtic 3Cat Verdi Clàssics | Cadira de director de cinema sola en un prat. |
| 79 | OPCIONAL | live/poster-fast-tem2.png | 480×720 | PNG RGB | Canal temàtic 3Cat Anime | Turó amb un cirerer i un gran sol vermell. |
| 80 | OPCIONAL | live/poster-fast-pucfc2.png | 480×720 | PNG RGB | Canal temàtic 3Cat Joc de cartes | Taula parada a l'aire lliure amb una carta de menú. |
| 81 | OPCIONAL | live/poster-fast-pucfc3.png | 480×720 | PNG RGB | Canal temàtic 3Cat Doraemon | Porta oberta enmig d'un camp que dona a un altre paisatge. |
| 82 | OPCIONAL | live/poster-fast-pucfc1.png | 480×720 | PNG RGB | Canal temàtic 3Cat Plats bruts | Finestra d'un pis amb una pila de plats a l'ampit. |
| 83 | OPCIONAL | live/poster-fast-pucfc4.png | 480×720 | PNG RGB | Canal temàtic 3Cat Vinagre(ta) | Ampolla de vinagre sobre un mur de pedra seca. |
| 84 | OPCIONAL | live/poster-fast-beauties.png | 480×720 | PNG RGB | Canal temàtic 3Cat: càmeres del temps | Càmera web sobre un turó amb núvols i un arc de Sant Martí. |
| 86 | NOU | categories/poster-actualitat.png | 480×720 | PNG RGB | Categoria «Actualitat» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Ciutat amb una torre de rellotge a primera hora del matí. |
| 87 | NOU | categories/fanart-actualitat.jpg | 1920×1080 | JPEG RGB | Categoria «Actualitat» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 90 | NOU | categories/poster-esports.png | 480×720 | PNG RGB | Categoria «Esports» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Una pilota que fa de sol post sobre un camp de joc entre turons. |
| 91 | NOU | categories/fanart-esports.jpg | 1920×1080 | JPEG RGB | Categoria «Esports» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 94 | NOU | categories/poster-campus.png | 480×720 | PNG RGB | Categoria «Campus» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Un arbre gran amb un llibre obert als peus. |
| 95 | NOU | categories/fanart-campus.jpg | 1920×1080 | JPEG RGB | Categoria «Campus» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 98 | NOU | categories/poster-cultura.png | 480×720 | PNG RGB | Categoria «Cultura i divulgació» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Una columna clàssica trencada al costat d'un telescopi. |
| 99 | NOU | categories/fanart-cultura.jpg | 1920×1080 | JPEG RGB | Categoria «Cultura i divulgació» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 102 | NOU | categories/poster-pellicules.png | 480×720 | PNG RGB | Categoria «Pel·lícules» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Carretera que es corba com una tira de cinema cap a un sol-projector. |
| 103 | NOU | categories/fanart-pellicules.jpg | 1920×1080 | JPEG RGB | Categoria «Pel·lícules» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 106 | NOU | categories/poster-documentals-i-reportatges.png | 480×720 | PNG RGB | Categoria «Documentals» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Uns prismàtics sobre la barana d'un mirador amb un ocell volant. |
| 107 | NOU | categories/fanart-documentals-i-reportatges.jpg | 1920×1080 | JPEG RGB | Categoria «Documentals» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 110 | NOU | categories/poster-musica.png | 480×720 | PNG RGB | Categoria «Música» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Turons ondulats com un pentagrama amb ocells fent de notes. |
| 111 | NOU | categories/fanart-musica.jpg | 1920×1080 | JPEG RGB | Categoria «Música» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 114 | NOU | categories/poster-entreteniment.png | 480×720 | PNG RGB | Categoria «Entreteniment» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Un globus aerostàtic sobre la vall. |
| 115 | NOU | categories/fanart-entreteniment.jpg | 1920×1080 | JPEG RGB | Categoria «Entreteniment» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 118 | NOU | categories/poster-series.png | 480×720 | PNG RGB | Categoria «Sèries» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Rengle de cases amb finestres il·luminades una darrere l'altra (capítols). |
| 119 | NOU | categories/fanart-series.jpg | 1920×1080 | JPEG RGB | Categoria «Sèries» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 122 | NOU | categories/poster-cuines.png | 480×720 | PNG RGB | Categoria «Cuines» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Hort amb una olla fumejant en primer pla. |
| 123 | NOU | categories/fanart-cuines.jpg | 1920×1080 | JPEG RGB | Categoria «Cuines» (fitxa i fons de la pàgina de la categoria; també les seves files i la fila de rànquing equivalent) | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 127 | NOU | categories/poster-generic.png | 480×720 | PNG RGB | Categoria nova o desconeguda que 3Cat afegeixi | Paisatge base de l'estil, sense cap detall identificatiu. |
| 128 | NOU | categories/fanart-generic.jpg | 1920×1080 | JPEG RGB | Categoria nova o desconeguda que 3Cat afegeixi | Versió ampla i molt simplificada de l'escena, sense text i sense detalls petits (es veu molt enfosquida). |
| 130 | OPCIONAL | categories/poster-eva.png | 480×720 | PNG RGB | EVA (fila de rànquing; futura categoria) | Turó amb un mòbil plantat com si fos un rètol, cel de tarda. |
| 131 | OPCIONAL | categories/fanart-eva.jpg | 1920×1080 | JPEG RGB | EVA (fila de rànquing; futura categoria) | Turó amb un mòbil plantat com si fos un rètol, cel de tarda. |
| 134 | NOU | letters/poster-all.png | 480×720 | PNG RGB | «Tots els programes» | Biblioteca a l'aire lliure: prestatges de pedra plens de llibres en un prat. |
| 136 | NOU | letters/poster-letter.png | 480×720 | PNG RGB | Base comuna per a «#» i les lletres A–Z | Fita de pedra en un camí, amb la cara frontal llisa i buida (el nom de la lletra surt com a títol de la fitxa). |
| 137 | OPCIONAL | letters/poster-letter-hash.png | 480×720 | PNG RGB | Lletra «#» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 138 | OPCIONAL | letters/poster-letter-a.png | 480×720 | PNG RGB | Lletra «A» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 139 | OPCIONAL | letters/poster-letter-b.png | 480×720 | PNG RGB | Lletra «B» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 140 | OPCIONAL | letters/poster-letter-c.png | 480×720 | PNG RGB | Lletra «C» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 141 | OPCIONAL | letters/poster-letter-d.png | 480×720 | PNG RGB | Lletra «D» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 142 | OPCIONAL | letters/poster-letter-e.png | 480×720 | PNG RGB | Lletra «E» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 143 | OPCIONAL | letters/poster-letter-f.png | 480×720 | PNG RGB | Lletra «F» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 144 | OPCIONAL | letters/poster-letter-g.png | 480×720 | PNG RGB | Lletra «G» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 145 | OPCIONAL | letters/poster-letter-h.png | 480×720 | PNG RGB | Lletra «H» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 146 | OPCIONAL | letters/poster-letter-i.png | 480×720 | PNG RGB | Lletra «I» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 147 | OPCIONAL | letters/poster-letter-j.png | 480×720 | PNG RGB | Lletra «J» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 148 | OPCIONAL | letters/poster-letter-k.png | 480×720 | PNG RGB | Lletra «K» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 149 | OPCIONAL | letters/poster-letter-l.png | 480×720 | PNG RGB | Lletra «L» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 150 | OPCIONAL | letters/poster-letter-m.png | 480×720 | PNG RGB | Lletra «M» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 151 | OPCIONAL | letters/poster-letter-n.png | 480×720 | PNG RGB | Lletra «N» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 152 | OPCIONAL | letters/poster-letter-o.png | 480×720 | PNG RGB | Lletra «O» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 153 | OPCIONAL | letters/poster-letter-p.png | 480×720 | PNG RGB | Lletra «P» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 154 | OPCIONAL | letters/poster-letter-q.png | 480×720 | PNG RGB | Lletra «Q» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 155 | OPCIONAL | letters/poster-letter-r.png | 480×720 | PNG RGB | Lletra «R» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 156 | OPCIONAL | letters/poster-letter-s.png | 480×720 | PNG RGB | Lletra «S» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 157 | OPCIONAL | letters/poster-letter-t.png | 480×720 | PNG RGB | Lletra «T» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 158 | OPCIONAL | letters/poster-letter-u.png | 480×720 | PNG RGB | Lletra «U» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 159 | OPCIONAL | letters/poster-letter-v.png | 480×720 | PNG RGB | Lletra «V» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 160 | OPCIONAL | letters/poster-letter-w.png | 480×720 | PNG RGB | Lletra «W» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 161 | OPCIONAL | letters/poster-letter-x.png | 480×720 | PNG RGB | Lletra «X» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 162 | OPCIONAL | letters/poster-letter-y.png | 480×720 | PNG RGB | Lletra «Y» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 163 | OPCIONAL | letters/poster-letter-z.png | 480×720 | PNG RGB | Lletra «Z» | La base comuna amb la lletra gravada a la fita (es pot generar per script a partir de la base i una tipografia). |
| 165 | NOU | search/poster-programmes.png | 480×720 | PNG RGB | «Cerca de programes» (després d'escriure el text) | La lupa sobre un rengle de cases (programes). |
| 168 | NOU | search/poster-videos.png | 480×720 | PNG RGB | «Cerca de vídeos» | La lupa sobre un quadre-pantalla plantat al camp. |
| 171 | NOU | menu/poster-similar.png | 480×720 | PNG RGB | «Et pot agradar» (al final de Continua mirant) | Camí que es bifurca, amb una flor destacada a la branca nova. |
| 174 | NOU | common/poster-next-page.png | 480×720 | PNG RGB | «Pàgina següent (n/m)» a totes les llistes paginades | Camí que gira a la dreta amb una fita amb fletxa. |
| 176 | NOU | common/poster-fallback.png | 480×720 | PNG RGB | Reserva quan un programa o vídeo de 3Cat no porta imatge | Paisatge neutre amb un marc de quadre buit al mig. |

## Files de l'especificació no fetes

| Fila CSV | Estat | Fitxer | Motiu |
|---|---|---|---|
| 2 | FET | icon.png | FET: ja existent (no s'ha tocat) |
| 3 | FET | fanart.jpg | FET: ja existent (no s'ha tocat) |
| 4 | FET | kids/fanart.png | FET: ja existent (no s'ha tocat) |
| 5 | FET | kids/banner.png | FET: ja existent (no s'ha tocat) |
| 6 | FET | kids/icon-home.png | FET: ja existent (no s'ha tocat) |
| 7 | FET | kids/poster-home.png | FET: ja existent (no s'ha tocat) |
| 8 | FET | kids/icon-live.png | FET: ja existent (no s'ha tocat) |
| 9 | FET | kids/poster-live.png | FET: ja existent (no s'ha tocat) |
| 10 | FET | kids/icon-programmes.png | FET: ja existent (no s'ha tocat) |
| 11 | FET | kids/poster-programmes.png | FET: ja existent (no s'ha tocat) |
| 12 | FET | kids/icon-ages.png | FET: ja existent (no s'ha tocat) |
| 13 | FET | kids/poster-ages.png | FET: ja existent (no s'ha tocat) |
| 14 | FET | kids/icon-highlights.png | FET: ja existent (no s'ha tocat) |
| 15 | FET | kids/poster-highlights.png | FET: ja existent (no s'ha tocat) |
| 16 | FET | kids/icon-petits.png | FET: ja existent (no s'ha tocat) |
| 17 | FET | kids/poster-petits.png | FET: ja existent (no s'ha tocat) |
| 18 | FET | kids/icon-tots.png | FET: ja existent (no s'ha tocat) |
| 19 | FET | kids/poster-tots.png | FET: ja existent (no s'ha tocat) |
| 20 | FET | kids/icon-age7.png | FET: ja existent (no s'ha tocat) |
| 21 | FET | kids/poster-age7.png | FET: ja existent (no s'ha tocat) |
| 22 | FET | kids/icon-age10.png | FET: ja existent (no s'ha tocat) |
| 23 | FET | kids/poster-age10.png | FET: ja existent (no s'ha tocat) |
| 24 | OPCIONAL | kids/landscape-home.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 25 | OPCIONAL | kids/landscape-live.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 26 | OPCIONAL | kids/landscape-programmes.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 27 | OPCIONAL | kids/landscape-ages.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 28 | OPCIONAL | kids/landscape-highlights.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 29 | OPCIONAL | kids/landscape-petits.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 30 | OPCIONAL | kids/landscape-tots.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 31 | OPCIONAL | kids/landscape-age7.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 32 | OPCIONAL | kids/landscape-age10.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 33 | NOU | menu/icon-live.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 36 | OPCIONAL | menu/landscape-live.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 37 | NOU | menu/icon-latest.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 40 | OPCIONAL | menu/landscape-latest.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 41 | NOU | menu/icon-rankings.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 44 | OPCIONAL | menu/landscape-rankings.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 45 | NOU | menu/icon-categories.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 48 | OPCIONAL | menu/landscape-categories.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 49 | NOU | menu/icon-letters.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 52 | OPCIONAL | menu/landscape-letters.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 53 | NOU | menu/icon-continue.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 56 | OPCIONAL | menu/landscape-continue.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 57 | NOU | menu/icon-search.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 60 | OPCIONAL | menu/landscape-search.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 61 | NOU | menu/icon-voice.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 64 | OPCIONAL | menu/landscape-voice.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 65 | NOU | live/poster-tv3.png | Decisió 2: canals en directe només amb la imatge del programa |
| 66 | OPCIONAL | live/landscape-tv3.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 67 | NOU | live/poster-324.png | Decisió 2: canals en directe només amb la imatge del programa |
| 68 | OPCIONAL | live/landscape-324.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 69 | NOU | live/poster-33.png | Decisió 2: canals en directe només amb la imatge del programa |
| 70 | OPCIONAL | live/landscape-33.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 71 | NOU | live/poster-esport3.png | Decisió 2: canals en directe només amb la imatge del programa |
| 72 | OPCIONAL | live/landscape-esport3.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 73 | NOU | live/poster-tv3cat.png | Decisió 2: canals en directe només amb la imatge del programa |
| 74 | OPCIONAL | live/landscape-tv3cat.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 75 | REUTILITZA | kids/poster-live.png | REUTILITZA: apunta a una imatge existent |
| 77 | OPCIONAL | live/landscape-fast-generic.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 85 | NOU | categories/icon-actualitat.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 88 | OPCIONAL | categories/landscape-actualitat.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 89 | NOU | categories/icon-esports.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 92 | OPCIONAL | categories/landscape-esports.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 93 | NOU | categories/icon-campus.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 96 | OPCIONAL | categories/landscape-campus.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 97 | NOU | categories/icon-cultura.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 100 | OPCIONAL | categories/landscape-cultura.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 101 | NOU | categories/icon-pellicules.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 104 | OPCIONAL | categories/landscape-pellicules.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 105 | NOU | categories/icon-documentals-i-reportatges.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 108 | OPCIONAL | categories/landscape-documentals-i-reportatges.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 109 | NOU | categories/icon-musica.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 112 | OPCIONAL | categories/landscape-musica.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 113 | NOU | categories/icon-entreteniment.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 116 | OPCIONAL | categories/landscape-entreteniment.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 117 | NOU | categories/icon-series.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 120 | OPCIONAL | categories/landscape-series.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 121 | NOU | categories/icon-cuines.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 124 | OPCIONAL | categories/landscape-cuines.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 125 | REUTILITZA | kids/poster-home.png | REUTILITZA: apunta a una imatge existent |
| 126 | NOU | categories/icon-generic.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 129 | OPCIONAL | categories/landscape-generic.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 132 | REUTILITZA | menu/poster-rankings.png | REUTILITZA: apunta a una imatge existent |
| 133 | NOU | letters/icon-all.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 135 | OPCIONAL | letters/landscape-all.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 164 | NOU | search/icon-programmes.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 166 | OPCIONAL | search/landscape-programmes.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 167 | NOU | search/icon-videos.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 169 | OPCIONAL | search/landscape-videos.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 170 | NOU | menu/icon-similar.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 172 | OPCIONAL | menu/landscape-similar.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 173 | NOU | common/icon-next-page.png | Decisió 7: sense icones d'adults (només pòsters i fons) |
| 175 | OPCIONAL | common/landscape-next-page.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 177 | OPCIONAL | common/landscape-fallback.png | Decisió 1: fitxes en pòster 2:3, sense versions 16:9 |
| 178 | OPCIONAL | common/banner.png | Opcional: vista Bàner 501 no prevista a la 1.0.3 i cap decisió la demana |

## Notes i interpretacions
- **Pel·lícules i Documentals:** per als pòsters s'han fet servir les dues imatges ja aprovades, retallades a 2:3. El pòster de Documentals és la **lupa** aprovada, no els prismàtics que proposa l'especificació. Com que Cerca (`menu/poster-search`, `search/*`) també fa servir una lupa, aquestes imatges es distingeixen pel color del cel i per l'objecte que es veu a dins.
- **`live/poster-fast-generic.png`:** s'ha fet tot i que hi hagi els 7 pòsters temàtics, perquè és la reserva per als canals temàtics nous o canviats, que són dinàmics.
- **`letters/poster-letter.png`:** és la base, una fita de pedra amb la cara en blanc. Les 27 variants (`poster-letter-hash` i `a`–`z`) porten la lletra composta amb Pillow sobre aquesta base, en color rovell i amb un relleu clar per donar l'efecte de gravat.
- **`categories/poster-musica`:** en lloc de turons, el pentagrama són cables elèctrics amb ocells fent de notes, perquè la primera prova va sortir amb notes musicals de veritat.
- **Fons:** s'han generat a 1024×576 i s'han ampliat a 1920×1080 (×1,875) afegint-hi una mica de gra de paper. Com que són formes planes i grans que es veuen al ~22 %, no es nota que siguin tous.
- **Pòsters:** s'han generat a 768×1024 (3:4), retallats a 683×1024 (2:3) amb el detall a la zona central i reduïts a 480×720.
