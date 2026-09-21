# 21. September 2026 – Von Spielzeuginseln zur reichen Einsiedlerin

## Ausgangslage

Der neue Prototyp v0.2 sollte nicht nur längere und portable Läufe speichern. Er sollte sichtbar machen, was in der RAM-Suppe geschieht, und prüfen, ob die aus P1 übernommene Population unter reicheren Umweltbedingungen eine stabile Kultur bilden kann.

Der Tag begann deshalb mit zwei offenen Baustellen: In der Suppe gab es für die Amöben zu wenig abwechslungsreiche und lokal erreichbare Veränderungen, und die beobachteten Abstammungslinien brachen früh ab.

## Eine Umwelt, die sich wirklich verändert

Der RAM erhielt drei technische Spielzeugtypen:

- Steine als stabile Bereiche,
- Blasen als veränderliche Werte,
- Schalter als ausgelöste Zustandsänderungen.

Zunächst lagen diese Objekte nur in wenigen Zonen. Weil viele Amöben niemals in ihre Nähe kamen, wurde der RAM anschließend in 128 Habitate gegliedert. Jedes Habitat enthält einen Stein, zwei Blasen und einen Schalter. Die Amöben erhielten verteilte RAM-Positionen; Kinder entstehen räumlich nahe bei einem Elternteil.

Diese Umweltveränderungen sind keine versteckte Fütterung. Eine Amöbe gewinnt Energie nur, wenn ihr eigenes Genom einen veränderten externen Wert tatsächlich liest. Damit bleibt die spätere Idee einer offenen Betriebssystemumwelt erhalten: Veränderung entsteht außerhalb der Entität, energetisch erschlossen wird sie nur durch eigene Aktivität.

## Die Lupe wird zum Fenster in die Suppe

Das Warten auf lange Läufe war wenig anschaulich. Die Lupe erhielt deshalb eine grafische Live-Ansicht des RAM-Rings:

- breite ovale Darstellung statt eines überfüllten Kreises,
- kleinere, ruhigere Spielzeugmarkierungen,
- einzeln schaltbare Ebenen für Amöben, Spielzeuge, Reads, Writes, Umwelt, Geburten und Tode,
- Mouseover mit fest verankerter Infobox und Fokus auf die Aktivität einer Amöbe,
- Klick auf eine Amöbe springt zu ihrer Detailkarte,
- der vorhandene Tickregler steuert dieselbe Ansicht auch historisch.

Die Visualisierung blieb read-only. Sie zeigt das Experiment, verändert es aber nicht.

## Warum genug Energie noch keine Kultur ergibt

Die ersten Habitatläufe starben bei Tick 2.256 und 2.122 aus. Einzelne Amöben besaßen dabei hohe Energiereserven. Eine Auswertung der 3.730 abgewiesenen Geburtsereignisse in Lauf 15 zeigte den eigentlichen unmittelbaren Fehler: 3.728 Geburten scheiterten daran, dass jeder Elternteil denselben Anteil bezahlen und danach über seinem individuellen Geburtswert `S₀` bleiben musste.

Damit konnte ein reicher Elternteil den fehlenden Anteil eines armen Partners nicht übernehmen, obwohl der gemeinsame Überschuss ausgereicht hätte.

Das Regelwerk wurde präzisiert: `S₀` bleibt der individuelle Energiesockel jedes Elternteils. Die Geburtskosten werden zunächst gleich verteilt. Reicht der Überschuss eines Elternteils nicht, übernehmen die übrigen den Fehlbetrag. Ein einzelner Elternteil darf theoretisch die vollständige Geburt finanzieren, aber niemand fällt unter sein eigenes `S₀`.

## Der Generationenwechsel

Der direkte Vergleichslauf mit Seed 42 und neuer Finanzierung erreichte 75 Nachkommen und Generation 8. Der vorherige Lauf mit denselben Umweltbedingungen hatte 36 Nachkommen und Generation 6 erreicht. Die letzte Geburt verschob sich von Tick 1.140 auf Tick 2.085.

Das war eine deutliche Verbesserung, aber keine stabile Kultur. Nach dem Absterben der Gründer blieb die Nettoreproduktion negativ. Die Population sank schließlich auf Vera 4 und Ada 4. Beide arbeiteten an weit voneinander entfernten RAM-Positionen und fanden nicht mehr zusammen.

Vera starb bei Tick 3.475. Ada erreichte allein das Laufende bei Tick 5.000.

## Ada 4

Ada war das vielleicht schönste Ergebnis des Tages:

- mehr als 101.000 Energie,
- Genomgröße 30 statt 198 bei den Gründern,
- funktionierende RAM-Exploration,
- kein ausführbares `MEM_WRITE`,
- keine Partner und keine Möglichkeit zur Fortpflanzung.

Der Lauf war technisch nicht ausgestorben, populationsbiologisch aber tot. Ada hatte fast alles verloren, was für eine Kultur notwendig war, und genau das behalten, was ihr individuelles Weiterleben hervorragend finanzierte.

Die spontane Vermutung, der Genompreis müsse noch deutlich sinken, hielt einer ersten Rechnung nicht stand. Adas Genom kostete rund 0,227 Energie pro Tick, das Gründer-Genom rund 0,546. Gegenüber Alterskosten von zuletzt über 40 Energie pro Tick war diese Differenz klein.

## Erkenntnisstand am Tagesende

**Beobachtet:** Die Umwelt liefert ausreichend Energie für sehr langes individuelles Überleben. Die gemeinsame Elternfinanzierung verbessert Nachkommenzahl und Generationstiefe erheblich. Sie erzeugt unter den getesteten Bedingungen noch keine stabile Kultur.

**Interpretation:** Der nächste dominante Engpass liegt wahrscheinlich im Verlust des Partnersuch- und Fortpflanzungsfragments. Individuelle Energieernte bleibt auch ohne dieses Fragment erfolgreich.

**Offene Prüfung:** Für jede Generation ist auszuwerten, wann und wie oft das ausführbare `MEM_WRITE` beziehungsweise das zusammenhängende Sozialfragment verloren ging. Erst danach soll über eine weitere Senkung des Genomtarifs entschieden werden.

## Artefakte

- [Experiment Generationenwechsel](../04_Prototypen/v0.2/EXPERIMENT_GENERATIONENWECHSEL.md)
- [Lauf 14](../07_Laufergebnisse/v0.2/Lauf_014.md)
- [Lauf 15](../07_Laufergebnisse/v0.2/Lauf_015.md)
- [Lauf 16](../07_Laufergebnisse/v0.2/Lauf_016.md)
- [Blogentwurf 012 – Die reichste Amöbe der Welt ist allein](../06_Blog/012_Die_reichste_Amoebe_der_Welt_ist_allein.md)

