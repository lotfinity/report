#!/usr/bin/env python3
with open('index-standalone.html', 'r') as f:
    content = f.read()

# Replace sphere items section
old_sphere_start = '                    <div class="sphere-items-container">'
old_sphere_end = '</div><img   loading="lazy" alt="" class="visual-mobile-img" />'

start_idx = content.find(old_sphere_start)
end_idx = content.find(old_sphere_end, start_idx) + len(old_sphere_end)

if start_idx != -1 and end_idx != -1:
    new_metrics = """                    <div class="hero-metrics-wrap" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5em; padding: 2em 0; max-width: 70em; margin: 0 auto;">
                        <div class="metric-card" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(249,197,24,0.2); border-radius: 0.8em; padding: 1.2em 1em; text-align: center;">
                            <div class="text-42-regular" style="color: #F9C518; line-height: 1.1;">3,5M TL</div>
                            <div class="text-14-regualr-caps" style="color: rgba(255,255,255,0.7); margin-top: 0.3em;">Capital cible \u00e0 red\u00e9ployer</div>
                            <div class="text-12-regular" style="color: rgba(255,255,255,0.35); margin-top: 0.3em;">Offre Sar Life actuelle</div>
                        </div>
                        <div class="metric-card" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(249,197,24,0.2); border-radius: 0.8em; padding: 1.2em 1em; text-align: center;">
                            <div class="text-42-regular" style="color: #F9C518; line-height: 1.1;">9\u201312 %</div>
                            <div class="text-14-regualr-caps" style="color: rgba(255,255,255,0.7); margin-top: 0.3em;">Rendement net mod\u00e9lis\u00e9 par unit\u00e9</div>
                            <div class="text-12-regular" style="color: rgba(255,255,255,0.35); margin-top: 0.3em;">sup\u00e9rieur au rendement estim\u00e9 de Sar Life</div>
                        </div>
                        <div class="metric-card" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(249,197,24,0.2); border-radius: 0.8em; padding: 1.2em 1em; text-align: center;">
                            <div class="text-42-regular" style="color: #F9C518; line-height: 1.1;">24k\u201334k TL</div>
                            <div class="text-14-regualr-caps" style="color: rgba(255,255,255,0.7); margin-top: 0.3em;">Revenu locatif mensuel combin\u00e9</div>
                            <div class="text-12-regular" style="color: rgba(255,255,255,0.35); margin-top: 0.3em;">deux unit\u00e9s Future Park</div>
                        </div>
                        <div class="metric-card" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(249,197,24,0.2); border-radius: 0.8em; padding: 1.2em 1em; text-align: center;">
                            <div class="text-42-regular" style="color: #F9C518; line-height: 1.1;">2 unit\u00e9s</div>
                            <div class="text-14-regualr-caps" style="color: rgba(255,255,255,0.7); margin-top: 0.3em;">Risque locatif diversifi\u00e9</div>
                            <div class="text-12-regular" style="color: rgba(255,255,255,0.35); margin-top: 0.3em;">au lieu d\u2019un seul locataire</div>
                        </div>
                    </div>"""
    content = content[:start_idx] + new_metrics + content[end_idx:]
    print('Sphere items replaced successfully')
else:
    print('ERROR: Could not find sphere items section')

# Replace intro section
old_intro = """    <section id="intro" class="section second">
        <div class="_3in1-container">
            <div class="section linear">
                <div class="w-layout-blockcontainer container _3in1 w-container">
                    <div class="_3d-yellow"></div>
                    <div class="wrapper">
                        <div class="_3-n-1-wrap">
                            <div class="_3d-yellow-wrap">
                                <div text-split="" class="text-52-regular _w-450">3-in-1 Solution for Real Estate <br/>Projects. </div>
                                <div data-w-id="c7cee2f9-4c0b-4756-73c7-375fe8971591" class="text-24-regular _w-435">Maximize the potential of your real estate <br/>projects with our comprehensive tool that <br/>combines Design, Estimate, and Shop \u2014 <br/>all in one place.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>"""

new_intro = """    <section id="intro" class="section second">
        <div class="_3in1-container">
            <div class="section linear">
                <div class="w-layout-blockcontainer container _3in1 w-container">
                    <div class="_3d-yellow"></div>
                    <div class="wrapper">
                        <div class="_3-n-1-wrap">
                            <div class="_3d-yellow-wrap">
                                <div text-split="" class="text-52-regular _w-450">Pourquoi cette strat\u00e9gie gagne</div>
                                <div data-w-id="c7cee2f9-4c0b-4756-73c7-375fe8971591" class="text-24-regular _w-435">Le c\u0153ur de la d\u00e9cision est simple : une grande unit\u00e9 concentre le risque, tandis que deux petites unit\u00e9s cr\u00e9ent plus de flux de tr\u00e9sorerie, plus de flexibilit\u00e9 et une meilleure liquidit\u00e9. Future Park devient la cible prioritaire car son prix d\u2019entr\u00e9e, son format compact et sa demande locative permettent de transformer le m\u00eame capital en rendement plus efficace.</div>
                            </div>
                        </div>
                    </div>
                    <div class="intro-cards-wrap" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5em; margin-top: 2em; max-width: 65em; margin-left: auto; margin-right: auto;">
                        <div class="intro-card" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 0.8em; padding: 1.5em;">
                            <div class="text-16-caps" style="color: #F9C518; margin-bottom: 0.5em;">Plus de cash-flow</div>
                            <div class="text-14-regular" style="color: rgba(255,255,255,0.7);">Une unit\u00e9 Sar Life peut g\u00e9n\u00e9rer environ 18k\u201321k TL par mois. Deux petites unit\u00e9s Future Park peuvent viser ensemble 24k\u201334k TL par mois, selon le prix d\u2019achat, l\u2019\u00e9tat r\u00e9el de l\u2019unit\u00e9 et le loyer obtenu.</div>
                        </div>
                        <div class="intro-card" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 0.8em; padding: 1.5em;">
                            <div class="text-16-caps" style="color: #F9C518; margin-bottom: 0.5em;">Moins de risque locatif</div>
                            <div class="text-14-regular" style="color: rgba(255,255,255,0.7);">Avec une seule unit\u00e9, une vacance coupe tout le revenu. Avec deux unit\u00e9s, le risque est divis\u00e9 : m\u00eame si une unit\u00e9 reste vide temporairement, l\u2019autre peut continuer \u00e0 produire du revenu.</div>
                        </div>
                        <div class="intro-card" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 0.8em; padding: 1.5em;">
                            <div class="text-16-caps" style="color: #F9C518; margin-bottom: 0.5em;">Meilleure flexibilit\u00e9 de sortie</div>
                            <div class="text-14-regular" style="color: rgba(255,255,255,0.7);">Deux petites unit\u00e9s sont plus faciles \u00e0 vendre s\u00e9par\u00e9ment qu\u2019un seul actif plus cher. Cela permet de vendre une unit\u00e9, garder l\u2019autre, ajuster la strat\u00e9gie ou lib\u00e9rer du capital progressivement.</div>
                        </div>
                    </div>
                    <div class="insight-box" style="background: rgba(249,197,24,0.06); border: 1px solid rgba(249,197,24,0.25); border-radius: 0.8em; padding: 1.2em 1.5em; margin-top: 1.5em; max-width: 65em; margin-left: auto; margin-right: auto;">
                        <div class="text-14-regualr-caps" style="color: #F9C518; margin-bottom: 0.3em;">Point cl\u00e9</div>
                        <div class="text-14-regular" style="color: rgba(255,255,255,0.75);">L\u2019in\u00e9ligibilit\u00e9 au cr\u00e9dit n\u2019est pas forc\u00e9ment un obstacle dans ce cas. Pour un acheteur \u00e9tranger au comptant, les annonces que d\u2019autres acheteurs \u00e9vitent peuvent cr\u00e9er une d\u00e9cote exploitable \u2014 \u00e0 condition de v\u00e9rifier le titre, l\u2019\u00e9tat r\u00e9el du bloc, l\u2019aidat, la livraison et la situation juridique avant tout engagement.</div>
                    </div>
                    <div class="mini-conclusion" style="margin-top: 1.5em; text-align: center; max-width: 50em; margin-left: auto; margin-right: auto;">
                        <div class="text-14-regular" style="color: rgba(255,255,255,0.5); font-style: italic;">Le premier objectif n\u2019est donc pas de comparer tous les projets du march\u00e9. Le premier objectif est de valider Future Park comme cible principale, puis de v\u00e9rifier uniquement les alternatives si Future Park \u00e9choue au contr\u00f4le terrain.</div>
                    </div>
                </div>
            </div>
        </div>
    </section>"""

if old_intro in content:
    content = content.replace(old_intro, new_intro)
    print('Intro section replaced successfully')
else:
    print('ERROR: Could not find intro section')

with open('index-standalone.html', 'w') as f:
    f.write(content)

print('Done')
