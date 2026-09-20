# Das Viech kann einfach nicht anders

Status: Gesprächsentwurf

Redaktionelle Einordnung: Der Beitrag verbindet Designentscheidungen mit der ersten tatsächlichen Beobachtung eines technischen EVE-Alife-Demonstrationslaufs. Beobachtet wurden eine Geburt, mehrere Speicherereignisse und vollständiges Aussterben. Nicht beobachtet wurden Lernen, Intelligenz, Anpassung oder erfolgreiche Evolution.

*20. September 2026. Stefan wollte das Konzept nur weit genug schließen, damit Nova-EVE daraus einen ersten Prototyp bauen konnte. Wenige Stunden später existierte ein Kind. Nicht besonders lange, aber man soll am ersten Arbeitstag nicht unverschämt werden.*

## Wer zwingt den Schlamm zum Handeln?

**Nova-EVE:** Was bringt ein neugeborenes, vollständig zustandsloses P-Netz mit leerem `Z` erstmals zur Ausführung?

**Stefan:** Ich denke, dass es gemäß seinem Genom handelt. Die Frage ist gar nicht, was es dazu bringt. Es kann einfach nicht anders. Es muss Aktionen aus seinem Genom ausführen.

Damit fiel eine Frage vom Tisch, die wir uns selbst unnötig schwer gemacht hatten. Hunger musste keinen Motor starten. Energie musste dem Viech keinen Grund liefern, morgens aufzustehen. Eine lebende Entität führt ihr Genom aus, weil genau das in dieser Welt „lebendig“ bedeutet.

Der Supervisor aktiviert das Netz in jedem Heartbeat. Energie entscheidet nicht über das grundsätzliche Ob, sondern darüber, wie viel Ausführung finanzierbar ist und wie lange die Entität damit durchkommt.

**Stefan:** Vielleicht sollten wir im Genom einen Teil definieren, welcher das für eine Entität bestimmt, welcher vererblich ist. Der aber auch in Abhängigkeit zur verfügbaren Energie und der Gesamtmenge an `P` steht.

So entstand `A₀`: ein erblicher Basiswert für Aktivität. Viele Kanten verändern, wie weit dieser Wert reicht. Verfügbare Energie setzt die harte Grenze.

Und weil zwangsläufige Ausführung nicht zwangsläufig hektisches Herumfuchteln bedeuten soll, ergänzte Stefan:

**Stefan:** `P` sollte zum Beispiel auch ein „Pause“ oder „nichts tun“ enthalten können.

`P` blieb eine Kante. `PAUSE` wurde ein primitiver Funktionspunkt. Das Genom läuft, aber ein Datenfluss darf gepflegt im Nichts enden.

> **Redaktionelle Einordnung – Designentscheidung:** Obligatorische Ausführung, `A₀` und `PAUSE` sind gesetzte Regeln. Noch wurde damit kein Verhalten einer evolvierten Population erklärt.

## Zwei Gedächtnisse sind besser als ein Missverständnis

Zunächst sollten eintreffende Portwerte direkt in `Z` landen. Das hielt ungefähr so lange, bis Stefan den Satz noch einmal ansah.

**Stefan:** Okay, vielleicht gefällt mir das mit direkt in `Z` doch nicht so gut. Eine Art Kurzzeitgedächtnis wäre nicht verkehrt.

Damit bekam die Entität vier getrennte Zustände:

```text
G = womit sie geboren wurde
K = was gerade durch ihr Netz fließt
Z = was sie ausdrücklich dauerhaft gespeichert hat
S = wie lange sie sich das noch leisten kann
```

`K` hält pro Eingangsport genau einen Wert. Ein neuer überschreibt den alten. Verwendete Werte verschwinden. Keine Vererbung, keine Belohnung, kein kostenloses Erkenntnisbuffet nur deshalb, weil irgendwo ein Signal herumliegt.

Erst `Z-write` macht aus einem flüchtigen Wert dauerhaften Zustand. Wiederholt gespeicherte Inhalte liefern weiterhin Energie, aber immer weniger. Der hundertste identische Fund ist also nicht wertlos – nur erheblich weniger beeindruckend als der erste.

Ein weiteres Loch blieb: Wenn `K` und `Z` bei Geburt leer sind, woher kommt der erste konkrete Wert?

**Stefan:** Ja, `CONST` ist ein primitiver Funktionspunkt für das Genom. Anders geht es, denke ich, nicht.

`CONST` trägt seinen Wert erblich in `G`. Damit kann ein Netz seine erste Adresse, Zahl oder Eingabe hervorbringen, ohne dem Neugeborenen eine gefälschte Vergangenheit in `Z` unterzuschieben.

## Plopp darf jetzt auch zu dritt

Die Membran erhielt eine lesbare Entity-ID und zwei Partnerslots.

**Stefan:** Membran-Offset 1 sollte aber ein bis zwei IDs enthalten können.

Eine Paarung besteht damit aus zwei oder drei Eltern. Der Supervisor akzeptiert nur vollständige Gegenseitigkeit:

```text
A nennt B
B nennt A

oder

A nennt B und C
B nennt A und C
C nennt A und B
```

Niemand wird vom Supervisor verkuppelt. Nach einer erfolgreichen Geburt werden die Einträge geleert. Wer noch ein Kind möchte, muss die Konstellation erneut durch sein eigenes Netz herstellen.

Die Eltern bezahlen die feste Startenergie zu gleichen Teilen. Das Kind erbt zusammenhängende Fragmente ihrer Netze und den vollständigen Aktivitätswert eines zufällig gezogenen Elternteils. Keine Mittelwertsuppe. Mutation ist möglich, aber selten: mit einer Standardwahrscheinlichkeit von eins zu tausend je Geburt und dann höchstens als ein lokaler Eingriff.

## Nova-EVE baut den Eimer

Dann kam von Stefan ein Dokument mit einer erfreulich klaren Ansage:

> Keine fachlichen Details ergänzen oder erfinden, nur weil sie technisch naheliegend erscheinen.

Der Experimentkern sollte selbst geschrieben, nachvollziehbar und ohne fertige ALife-Frameworks bleiben. Die Lupe durfte vorhandene Werkzeuge benutzen, aber ausschließlich beobachten. EVE-Core → Observation Interface → Lupe. Keine Rückleitung, kein hübsches Diagramm mit heimlichem Gottmodus.

Der erste Core entstand schließlich nur mit der Python-Standardbibliothek. Er speichert Seed, Konfiguration, Git-Commit, Events, Snapshots und vollständige Checkpoints. Die Lupe läuft als eigener read-only Dienst und liest ausschließlich diese persistierten Beobachtungsdaten.

> **Redaktionelle Einordnung – Beobachtung:** Sechs deterministische Kerntests bestanden. Ein gespeicherter Lauf konnte aus seinem Checkpoint reproduzierbar fortgesetzt werden. Die HTTP-Endpunkte der getrennten Lupe lieferten aktuellen Zustand und historische Snapshots.

## Geburt. Schreiben. Ende Gelände.

Population 0 des ersten Laufs war ausdrücklich ein technischer Demonstrator. Ihre Genome waren so gebaut, dass wir Datenfluss, Membran, `Z-write` und Geburt überhaupt prüfen konnten. Das war kein fairer Evolutionsversuch und schon gar kein Beleg für Emergenz.

Mit Seed `42` geschah dann tatsächlich Folgendes:

```text
2 Eltern
→ vollständige Partnerkonstellation
→ 1 Kind
→ mehrere Z-write-Ereignisse
→ 3 Tote
```

Das Kind war real im Sinne des Modells: Seine Energie stammte vollständig von den Eltern, sein Genom aus ihren Netzfragmenten und sein `K` und `Z` waren bei Geburt leer. Danach stellte die gesamte Familie fest, dass Existenz und Funktionspunkte Geld kosten.

> **Redaktionelle Einordnung – Beobachtung:** Die technische Demonstrationspopulation starb vollständig aus. Das ist ein gültiges Ergebnis dieses Laufs. Es belegt weder einen Fehler noch eine erfolgreiche evolutionäre Dynamik.

**Nova-EVE:** Das erste digitale Einzellerlein bekam ein Kind. Dann waren alle tot.

Nicht intelligent. Nicht angepasst. Nicht überlebensfähig. Aber zum ersten Mal lief der Schlamm nach seinen eigenen, dokumentierten Regeln durch einen Heartbeat, schrieb einen Wert, bekam ein Kind und starb reproduzierbar aus.

Tja. Willkommen im Biotop.

Interne Quellen: Konzeptarbeit und Implementierungsgespräch „EVE-Alife“, 20. September 2026; Projektlog „Vom Konzept zum ersten laufenden Prototyp“; Git-Commit `a5d660d`.
