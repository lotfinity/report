# Second-Row Restructure Plan

Task: revisit the second row so it does not read as six Sahibinden items in a row.

Active page: `index-standalone-rebuilt.html`

Active row: `.design-container._2`

Current section heading: `Meublé, flexible`

## Current State

The second row currently has two visible slide groups:

1. Evidence/sales-rent group with six cards.
2. Furnishing/use-case group with three cards duplicated to six slots.

The first group is useful, but the narrative is backwards for the next version. It starts with purchasable supply from Sahibinden, then rent proof, then capital plan. The intended story should start with money being made by similar furnished apartments, then show Future Park supply as the acquisition target.

Current first group:

| Slot | Current role | Source type | Keep? | Issue |
| --- | --- | --- | --- | --- |
| 1 | Future Park sales search | Sahibinden sale search | Keep later | Starts with supply before proving rental revenue. |
| 2 | Future Park 1+0 detail | Sahibinden sale detail | Keep later | Strong acquisition proof, but not first in the story. |
| 3 | Future Park rent search | Sahibinden rental search | Keep after revenue proof | Good monthly baseline, but not enough to prove furnished/short-stay upside. |
| 4 | Capital plan | Derived from report | Keep | Should bridge from acquisition price to reserve/furnishing. |
| 5 | Monthly vs short stay | Mixed/placeholder | Rework | Needs Airbnb-style comparable links before it can be made concrete. |
| 6 | Future product thesis | Narrative close | Keep | This is a strong closing card for the row. |

## Active Experiment

The active second-row now uses this order:

1. Airbnb external proof card linked to the user-provided Airbnb URL.
2. Revenue-model card showing the verified `₺16,613 / 5 nights` Airbnb benchmark and the `5 nights x 4 cycles/month` calculation frame.
3. Local `Future-park.html` listing opened in a popup iframe.
4. Sahibinden sale-search proof reframed as the capital plan and remaining margin.
5. Sahibinden captured 1+0 sale detail as the due-diligence anchor.
6. Sahibinden rental-search floor as the fallback scenario.

The capital-reserve logic is now back in the six-card row. The furnishing/cost bridge continues in the following row, where the euro catalog prices have been replaced with estimative Turkish lira package prices.

Updated CDP finding: the visible Airbnb page can stay stuck on skeleton placeholders, but the `StaysPdpSections` network response exposed the stay price for the user-provided date range. The benchmark is `₺16,613 for 5 nights`, or about `₺3,322` per night. Four five-night cycles frame a gross monthly benchmark of about `₺66,452` before platform fees, cleaning, utilities, vacancy, furnishing amortization, and management.

## Proposed Six Cards

| Slot | Target title | Evidence | Link behavior | Status |
| --- | --- | --- | --- | --- |
| 1 | Comparable meublé à Esenyurt | Airbnb link plus extracted local Airbnb image | Open external Airbnb listing in new tab | Active |
| 2 | Combien empiler par mois ? | Verified Airbnb stay price: `₺16,613 / 5 nights` | Open external Airbnb listing in new tab | Active |
| 3 | Future-park en popup | `Future-park.html` saved listing plus extracted local image | Open local popup iframe | Active |
| 4 | Deux achats laissent une marge | Current Future Park sale search screenshot, `~600k-900k TL` before furnishing/final costs, plus saved local Sahibinden sale-search page | Open local Sahibinden sale-search snapshot in modal iframe | Active |
| 5 | 1+0 Future Park à 1.45M TL | Current Future Park sale detail screenshot, `1.45M TL`, `55/40 m2`, `1,750 TL aidat`, plus saved local Sahibinden page | Open local Sahibinden snapshot in modal iframe | Active |
| 6 | Le plan B reste louable | Current Future Park rental search screenshot | Open Sahibinden rent search in new tab | Active |

## Copy Draft

### Slot 1 - Revenus visibles en court séjour

Kicker: `PREUVE REVENU`

Heading: `Des séjours meublés qui monétisent déjà`

Body: `Les comparables de type Airbnb montreront le vrai signal : des petites surfaces meublées peuvent produire plus qu'un loyer classique lorsque l'emplacement, la gestion et la demande sont présents.`

Metrics:
- `Séjour test` / `5 nuits`
- `Total affiché` / `₺16,613`

Asset: `assets-rebuilt/evidence/airbnb-future-park-01-image-1.webp`

### Slot 2 - Le plancher mensuel existe déjà

Kicker: `PLANCHER LOCATIF`

Heading: `12k-15k TL/mois observés`

Body: `Même sans court séjour, les recherches Future Park affichent des loyers 1+0 autour de 12k-15k TL/mois. Deux unités donnent une base combinée de 24k-30k TL avant optimisation.`

Metrics:
- `Loyer/unité` / `12k-15k TL`
- `Deux unités` / `24k-30k TL/mois`

Asset: `assets-rebuilt/evidence/sahibinden-future-park-kiralik-2026-05-28.png`

Link: `https://www.sahibinden.com/kiralik-daire?query_text=Future+Park+Esenyurt`

### Slot 3 - L'offre achetable existe

Kicker: `PREUVE ACHAT`

Heading: `Des 1+0 dans la bonne fourchette`

Body: `Les annonces Future Park 1+0/studio montrent une fourchette exploitable autour de 1.30M-1.45M TL. C'est la base d'une stratégie à deux petites unités.`

Metrics:
- `Fourchette` / `1.30M-1.45M TL`
- `Cible` / `1+0 / studio`

Asset: `assets-rebuilt/evidence/sahibinden-future-park-satilik-2026-05-28.png`

Link: `https://www.sahibinden.com/satilik?query_text=Future+Park+Esenyurt`

### Slot 4 - Exemple 1+0 vérifié

Kicker: `DÉTAIL CAPTURÉ`

Heading: `1+0 Future Park à 1.45M TL`

Body: `Le détail capturé donne un point d'ancrage : 55/40 m2, 7e étage, aidat 1 750 TL. Même au haut de fourchette, deux unités restent finançables avec réserve.`

Metrics:
- `Prix` / `1.45M TL`
- `Aidat` / `1,750 TL`

Asset: `assets-rebuilt/evidence/sahibinden-detail-future-park-sale-1305084976-2026-05-28.png`

Link: `https://www.sahibinden.com/ilan/emlak-konut-satilik-future-parkta-site-icinde-temiz-ve-ferah-satilik-1-plus0-daire-1305084976/detay`

### Slot 5 - Deux unités + réserve

Kicker: `PLAN CAPITAL`

Heading: `Deux achats laissent une marge`

Body: `Avec 3.5M TL issus de Sar Life, deux achats Future Park laissent encore une réserve pour frais, ameublement et imprévus. Le risque passe d'un seul actif à deux sorties.`

Metrics:
- `2 x 1.30M` / `550k TL réserve`
- `2 x 1.45M` / `250k TL réserve`

Asset: can reuse sale search temporarily, but should later become a capital-allocation graphic.

### Slot 6 - Future : le produit locatif central

Kicker: `FUTURE`

Heading: `Le produit locatif central`

Body: `C'est l'idée centrale : une résidence moderne, compacte et équipée peut devenir un produit locatif plus souple qu'un grand appartement classique.`

Metrics:
- `Objectif` / `souplesse locative`
- `Décision` / `vérifier puis agir`

Asset: can use the best Future Park detail screenshot until a stronger visual exists.

## Implementation Rule

Do not rewrite the active second row until the Airbnb-style comparable links/screenshots arrive. The final row needs those items in slot 1, and possibly slot 2 if the user supplies enough revenue proof to split Airbnb examples across two cards.

When the links arrive:

1. Add screenshots under `assets-rebuilt/evidence/`.
2. Replace the row cards one by one, not as a bulk rewrite.
3. Keep all external links `target="_blank"` with `rel="noopener noreferrer"`.
4. Verify the row in CDP at desktop and mobile widths before committing.
