# First-Row Image Assessment

Task: assess whether the current first-row images match the injected French text content in the `Pourquoi Future Park ?` row.

Scope checked:
- Active page: `index-standalone-rebuilt.html`
- Row container: `.design-container._1`
- Structure: two `.slide-1-grid` groups, six cards each, twelve content cards total.
- Method: static DOM extraction plus direct inspection of representative assets in `assets-rebuilt/`.

No HTML or visual replacements were made in this pass.

## Summary

The row now has strong text, but most visuals are still recycled Webflow/template assets. The repeated visuals are visually polished, but they often communicate "architecture/product demo" rather than the new investment thesis: flexible stay, medical guests, small-unit yield, operator advantage, due diligence, and direct demand.

The clearest problem is repetition. The same visual is reused for different ideas:
- `Frame 2131330325.png` appears on slides 1 and 4.
- `placeholder.png` appears on slides 2, 5, 8, and 11.
- `1.png` appears on slides 3 and 6.
- The apartment stack appears on slides 7 and 10.
- The amenity/site map appears on slides 9 and 12.

This makes the row feel coherent as a design system, but not yet coherent as an argument.

## Slide Audit

| Slide | Current heading | Current visual | Relevance | Issue | Recommended replacement direction |
| --- | --- | --- | --- | --- | --- |
| 1 | Conçu pour le séjour flexible | `Frame 2131330325.png`, single Future Park line-art building | Partial | It identifies the building, but not the flexible-stay use case, medical guests, companions, or temporary residents. | Keep Future Park as anchor, but add a furnished-stay / hotel-residence layer: small unit, luggage, monthly stay, patient companion cues. |
| 2 | Prix décoté, usage réel | `placeholder.png` linked to `video2.html` | Replace | Generic logo/video placeholder does not explain discount, damaged reputation, or real rental demand. | Pricing-opportunity visual: discounted purchase price vs usable monthly demand, with a sober investment dashboard feel. |
| 3 | Rendement des petites surfaces | `1.png`, full Future Park 3D complex render | Partial | It shows the project well, but not the economic point of studios/1+0 producing stronger cash flow than one large unit. | Small-unit yield comparison: two compact units vs one larger flat, capital split, monthly rent arrows, TL cash-flow emphasis. |
| 4 | Compatible séjour médical | `Frame 2131330325.png`, repeated from slide 1 | Replace | The same building render does not show medical recovery, privacy, kitchen, companion, or extended stay. | Private recovery apartment concept: compact furnished room, kitchenette, quiet stay, companion, clinic/hospital transfer cue. |
| 5 | Avantage propriétaire-opérateur | `placeholder.png` linked to `video2.html` | Replace | Placeholder does not show clinical experience, local network, or direct guest acquisition. | Operator workflow visual: clinic network, guest pipeline, local operations, owner/operator control points. |
| 6 | Services à forte valeur | `1.png`, repeated full-complex render | Replace | The complex render does not show transfers, taxi, delivery, translation, local support, or tourist packages. | Service-stack visual: transfers, taxi, grocery delivery, translation, local assistant, trip package icons around the guest. |
| 7 | Maîtrise locale | stacked apartment PNGs | Partial | It suggests real estate, but not Istanbul presence, local rules, administration, guests, or rental structure. | Local execution visual: Istanbul admin checklist, residence desk, guest management, contracts, aidat/rules cues. |
| 8 | Option de revalorisation | `placeholder.png` linked to `video3.html` | Replace | Placeholder does not show hotel/commercial relaunch or perception change. | Revaluation scenario: dormant commercial/hotel layer becoming active, perception shift, value uplift arrow. |
| 9 | Le downside reste viable | amenity/site map stack | Partial | The site map suggests livability and amenities, but not downside/base-case rental viability. | Base-case rental visual: monthly furnished lease, conservative cash-flow floor, occupied unit without full project revival. |
| 10 | À vérifier avant achat | stacked apartment PNGs, repeated from slide 7 | Replace | Repeated tower images do not communicate due diligence: tapu, habitable block, aidat, rules, guest access, net yield. | Due-diligence checklist visual with Turkish property documents and clear pass/fail checks. |
| 11 | Demande non dépendante d’Airbnb | `placeholder.png` linked to `video3.html` | Replace | Placeholder does not communicate direct clinical/monthly demand or reduced platform dependence. | Direct-demand channel map: clinic/referral/monthly furnished stays before Airbnb-style platforms. |
| 12 | Un actif à opérer | amenity/site map stack, repeated from slide 9 | Partial | Amenities help, but the text is about active operation: housing, service, support, targeted marketing. | Active-asset operations loop: listing, guest support, services, reviews/referrals, marketing, repeat demand. |

## Replacement Priority

1. Replace slides 2, 5, 8, and 11 first because the video placeholders are the weakest semantic match.
2. Replace slides 4, 6, and 10 next because duplicated visuals actively conflict with distinct messages.
3. Rework slides 3, 7, 9, and 12 after that; they are usable placeholders but should become more specific.
4. Slide 1 can remain the visual anchor for the project if it is enhanced or paired with a stronger flexible-stay image.

## Asset Notes

Representative inspected files:
- `assets-rebuilt/3b03b71f05_685312d28646ac27e1e57f46_Frame 2131330325.png` - 1252 x 1188, Future Park single-building line-art.
- `assets-rebuilt/1.png` - 1254 x 1254, full Future Park 3D complex render.
- `assets-rebuilt/placeholder.png` - 850 x 476, Future Park logo/video placeholder.
- `assets-rebuilt/4f32581370_6851b5afa8312a49891754de_Group 989.png` - 312 x 550, stacked tower image.
- `assets-rebuilt/933f3d11c7_6851c347b8e04f765a40c947_Property 1_1.webp` - 1221 x 1919, dark site/amenity map.

Recommended generation/replacement specs:
- For building/complex cards: keep near-square assets around 1250 x 1250 or 1252 x 1188 so current CSS crops predictably.
- For video-placeholder cards: use 16:9 or near 850 x 476 until the card wrapper is redesigned.
- For tall stack/map cards: keep tall transparent or tall dark assets so the current layered CSS does not collapse.

## Verification

This task is a content/asset relevance audit only. CDP screenshot verification is still required after actual image replacement, because fit, crop, and horizontal scroll behavior can only be trusted in the browser.
