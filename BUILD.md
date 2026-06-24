# BUILD.md — Een nieuwe hardloop-app maken (bartlopen Run Coach)

Dit is het recept om snel een persoonlijke hardloop-app voor een nieuwe loper te
maken vanuit deze template. Taal: **Nederlands**. Signatuurwoord: **"strijder"**
(altijd houden). Coach: **Coach Bart · @bartlopen**.

Bestaande voorbeelden:
- Dave — 10K — https://bartdevries43-arch.github.io/bartlopen-runcoach/ (afstand-gebaseerd)
- Marinke — halve ±2:15 — https://bartdevries43-arch.github.io/bartlopen-marinke/ (afstand-gebaseerd)
- Sietse — halve 1:45 — https://bartdevries43-arch.github.io/bartlopen-sietse/ (**tijd-gebaseerd**, blessurevrij)

---

## 1. Intake — vraag dit aan de loper
1. **Naam** (en evt. of de voornaam genoeg is).
2. **Doel + wedstrijd**: afstand/tijd, naam van de wedstrijd, **datum**.
3. **Huidig niveau**: comfortabel tempo (en in de hitte), huidige max afstand, km/week.
4. **Trainingsdagen** per week + welke dagen (bijv. ma/do/za).
5. **Sturing**: afstand-gebaseerd (km) of **tijd-gebaseerd** (minuten, bij blessure-opbouw)?
6. **Blessures / aandachtspunten** (bepaalt opbouwtempo en evt. knie-/signaalkaarten).
7. **In welke week zitten ze nu?** (zet de startdatum hierop af.)
8. Eventuele **tussenwedstrijden** (bijv. een 10K onderweg).

Staat alles al in een schema-document? Lees dat uit en neem het 1-op-1 over.

## 2. Stappen
1. **Kopieer de template** naar een nieuwe map / nieuwe repo.
2. **CONFIG** (boven in `app.js`):
   - `appName` (bijv. "Op naar 10K" / "Op naar 21,1K"), `runner`, `goal`.
   - `startDate` = **de maandag van week 1** (maand is 0-based: 5 = juni). Reken terug
     vanuit "in welke week zitten ze nu", zodat het label **"Nu"** op de juiste week valt.
     Check: `currentWeek()` = `floor((vandaag - startDate)/7 dagen) + 1`.
   - `storeKey` = **uniek** per loper (anders delen ze voortgang!).
   - `athleteWord` / `catchphrase`: "strijder" laten staan.
3. **ZONES**: vul de tempo's in op basis van hun niveau. Tip: hergebruik de sleutel
   `"doel"` voor het wedstrijd-/doeltempo, dan werken alle bestaande kleuren in
   `styles.css` zonder aanpassing. (Dave: doel ≈ 5:30; Marinke: ≈ 6:24; Sietse: HM-gevoel.)
4. **PLAN**: vervang met hun schema. Per week: `week`, `dates`, `phase`, optionele vlaggen
   `recovery: true` / `taper: true` / `race: true`, en `sessions: [...]`.
   - Dagen via helpers, bijv. `const ma = ...`, `const don = ...`, `const za = ...`
     (let op: `do` is een gereserveerd woord in JS → gebruik `don`).
   - **Afstand-gebaseerd**: sessie heeft `km: 10`. **Tijd-gebaseerd**: `min: 45`
     (en `renderChart`, `nextup-meta`, `session-meta`, `detail-kind` gebruiken dan `s.min`;
     zie bartlopen-sietse als referentie).
   - `TOTAL_WEEKS` bovenin gelijkzetten aan het aantal weken (bepaalt de cap van `currentWeek`
     en de raceweek-check). De finish-badge checkt `s.week === TOTAL_WEEKS && s.day === "za"`.
5. **COACH**: per zone **6–8** gevarieerde regels (worden willekeurig getoond). Geef de loper
   een eigen toon (Dave explosief, Marinke rustig-sterk, Sietse beheerst/blessurevrij). "strijder"
   in een deel van de regels, niet allemaal — natuurlijker.
6. **DONE**: lijst met ~6 willekeurige "gedaan"-meldingen; racemelding apart.
7. **WHY / INFO / BADGES**: stem af op doel en niveau (bijv. lange-loper-badge op een passende
   afstand/tijd; bij blessure een knie-signaalkaart zoals bij Sietse).
8. **og-image**: draai `python3 generate_og.py` (pas titel/naam/doel aan) → `og-image.png`.
   Zet de Open Graph-tags in `index.html` met de juiste URL (voor nette WhatsApp/Insta-preview).
9. **sw.js**: geef `CACHE` een unieke naam (bijv. `runcoach-<naam>-v1`). **Bij elke latere
   wijziging dit ophogen**, anders halen telefoons (PWA) de update niet op.
10. **index.html / manifest.json**: titel, `apple-mobile-web-app-title`, beschrijving aanpassen.

## 3. Publiceren (GitHub Pages)
- Elke loper krijgt een **eigen PUBLIEKE repo** (`bartlopen-<naam>`). GitHub Pages werkt niet
  op privé-repo's met een gratis plan.
- `gh repo create bartlopen-<naam> --public` → bestanden in de **root** committen → pushen.
- Pages aanzetten: `gh api -X POST repos/<owner>/bartlopen-<naam>/pages -f 'source[branch]=main' -f 'source[path]=/'`.
- Zet ook `homepage` van de repo op de Pages-URL en geef de repo een leuke `description`.
- Verifieer live (HTTP 200) en stuur de loper de link + een kort deelbericht.

## 4. Datamodel (kort)
- `CONFIG` — branding + startdatum + storeKey.
- `ZONES[]` — `{key, name, pace, info}`; `zoneByKey` mapt erop. Sleutels bepalen kleuren in CSS.
- `PLAN[]` — weken met `sessions[]`; sessie: `{day, dayLabel, kind, zone, km|min, title, goal, blocks[]}`.
- `COACH{zone:[...]}`, `WHY{zone:"..."}`, `INFO[]`, `BADGES[]` (elk met `test(stats)`).
- `computeStats()` levert o.a. `done, km, maxDist, maxTime, bestPace, streak, fullWeeks, raceDone`.
- Voortgang staat in `localStorage[storeKey]`; export/import-knoppen zitten in de footer.

## 5. Valkuilen (al opgelost in deze template — houden!)
- **Tijd invullen op mobiel**: het tijdveld staat op een cijfertoetsenbord (geen `:`-toets).
  `autoTime()` voegt de dubbele punt automatisch in (`5200` → `52:00`, `21500` → `2:15:00`).
- **Oranje toast-balletje**: `.toast` mag NIET in de `prefers-reduced-motion`-regel staan
  (die forceert `opacity:1`, waardoor de lege toast permanent zichtbaar wordt).
- **PWA-cache**: na een update moet de app één keer gesloten/heropend worden; daarom de
  `CACHE`-versie ophogen bij elke wijziging.
- **`do`** is een JS-keyword → donderdag-helper `don` noemen.
- **storeKey** uniek houden per loper.
