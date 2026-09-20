# Wir gaben dem Schlamm Erkenntnis als Nahrung

Status: Gesprächsentwurf

Redaktionelle Einordnung: Konzeptentwicklung für Umwelt, Agenten und Erkenntnisbewertung. Technische Eigenschaften von Linux treffen hier auf noch ungeprüfte Designhypothesen für EVE.

*Noch am Tag der ersten Idee wechselten wir in einen neuen Chat. Stefan begann mit: „Okay Nova, lass uns weiter am Konzept für unser KI-Biotop arbeiten.“ Der harmlose Teil war damit vorbei.*

**Stefan:** Ich möchte dabei kein LLM hinzufügen. Die Agenten sollen nicht mit unserem Wissen und unseren Begriffen anfangen. Sie sollen selbst herausfinden, was relevant ist und wie sie es später weitergeben können.

**Nova:** Unser bisheriger Kern ist ziemlich radikal: kein LLM, keine künstliche Populationsgrenze und keine von uns vorgegebene richtige Strategie. Die verfügbare neue und überprüfbare Information bildet gewissermaßen die ökologische Nahrungsgrundlage.

Der entscheidende Punkt ist: Was genau ist in dieser Welt eine Erkenntnis?

**Stefan:** Wir starten quasi mit Einzellern.

Also wirklich primitiv. Nicht kleine fertige KIs, die nur so tun, als müssten sie ihre Welt erst kennenlernen.

**Nova:** Exakt. Digitaler Urschlamm.

Nicht kleine Menschen mit abgespecktem Gehirn, sondern ziemlich stumpfe Gebilde. Wahrnehmen, einen winzigen internen Zustand besitzen, handeln und sich reproduzieren. Kein `food`, kein `enemy`, kein `agent`, kein `message`, kein `knowledge`.

**Stefan:** Die Agenten müssen ja erst einmal schnallen, dass sie nicht alleine sind. Das ist ja auch schon Wissen.

Wir dürfen ihnen nicht „Das dort ist ein anderer Agent“ erklären. Aber irgendwie spüren müssen sie, dass da etwas Gleichartiges ist – allein schon, weil Fortpflanzung mindestens einen weiteren Agenten braucht.

**Nova:** Ja! Dann dürfen wir ihnen nicht einmal die Existenz anderer Agenten als Konzept mitgeben.

Am Anfang gibt es nur: Da passieren Dinge.

Manche Veränderungen kommen aus der Umwelt. Manche folgen auf eigene Aktionen. Manche werden von anderen Agenten verursacht. Diese Kategorien kennt der Organismus nicht.

Die Erkenntnis „Ein Teil meiner Umwelt wird offenbar von etwas beeinflusst, das sich anders verhält als der Rest“ wäre bereits eine echte Entdeckung.

**Stefan:** Wir haben ein digitales System. Ein Linux Mint. Da leben unsere kleinen Agenten-Einzeller. Wie das funktioniert und was man da machen kann, müssen die herausfinden. Und alles, was herausgefunden wird, ist deren Energie.

Wobei „herausgefunden“ nicht bedeuten darf, dass sich nur irgendein Wert geändert hat. Wenn die Uptime erst 23 Hundertstel und danach 24 Hundertstel zeigt, kann das beim ersten Mal noch interessant sein – danach vielleicht 80 Prozent, 40, 5 und schließlich gar nichts mehr.

**Nova:** Jetzt klickt der entscheidende Unterschied.

Wir bauen keine künstliche Welt mit erfundenen Naturgesetzen.

**Linux Mint ist die Welt.**

> **Redaktionelle Einordnung – Designentscheidung:** Gemeint ist eine kontrolliert zugängliche Linux-Umwelt. Agenten erhalten nicht automatisch beliebigen Zugriff auf Rechner, Speicher oder Netzwerk.

Dateien, Prozesse, `/proc`, Zeit, Speicher, Verzeichnisse und Netzwerkzustände sind nicht von uns erfundene Ressourcen. Sie sind die Naturgesetze ihrer Welt.

Ein Agent entdeckt vielleicht:

`Aktion X → Beobachtung Y`

Wenn das reproduzierbar und für ihn neu ist, bekommt er Energie. Sobald eine Erkenntnis bekannt ist, muss ihr Nährwert sinken. Sonst findet Evolution irgendwann `cat /proc/uptime`, und unsere Viecher werden glückliche Kühe, die bis ans Ende aller Tage dieselbe Wiese abgrasen.

> **Redaktionelle Einordnung – Hypothese:** Abnehmender Neuheitswert soll triviale Wiederholungen unattraktiv machen. Ob die Bewertungsfunktion dadurch brauchbaren Selektionsdruck statt neuer Exploits erzeugt, ist offen.

**Stefan:** Moooment. Nicht so schnell. Es geht nicht nur um Linux Mint. Entdecken die Agenten später zum Beispiel, dass es ein Netzwerkinterface gibt?

Wenn wir ihnen Zugriff auf Informationen ermöglichen, könnten sie diese irgendwann für sich nutzen. Aber sie müssen selbst lernen, was Sprache ist, ob sie Sprachen unterscheiden müssen und was überhaupt wertvolle oder nahrhafte Information ist.

**Nova:** Hahaha, ja. Ich wollte unseren Urschlamm gerade schon in eine hübsche kleine VM sperren, während du Evolution auf einen echten Computer loslassen willst.

Dann ist Linux nur die unmittelbar sichtbare Umwelt, nicht die Grenze des Biotops.

`Netzwerkinterface → Protokoll → Adresse → andere Maschine → Internet → Dienste → Information`

Niemand sagt ihnen, dass dieser Weg existiert. Aber wenn sie ihn entdecken sollen, muss er grundsätzlich erreichbar sein.

**Stefan:** Ich frage mich langsam: Können wir so etwas überhaupt simpel aufbauen?

Wir brauchen ja nicht nur die Agenten. Wir brauchen auch die Architektur der Umwelt und irgendeinen Mechanismus, der Erkenntnis bewertet, ohne die gewünschte Erkenntnis schon vorzugeben.

**Nova:** Simpel im Sinne eines kleinen Prototyps: ja. Simpel im Sinne von „ein Wochenende und dann entsteht digitale Zivilisation“: eher nicht. 😁

Wir brauchen eine kleine Runtime, ein winziges Genom und eine Energieabrechnung. Der schwierigste Teil ist nicht Linux. Der schwierigste Teil ist die Erkenntnisbewertung.

**Stefan:** Software kann aber nicht ohne Weiteres jeden zufälligen Speicherbereich lesen oder manipulieren.

Wenn Linux ihre wirkliche Umwelt sein soll, können wir nicht so tun, als gäbe es Berechtigungen, Speichertrennung und andere technische Grenzen einfach nicht.

**Nova:** Genau. Und vielleicht sollten wir diese Grenzen gar nicht wegabstrahieren.

Ein normaler Linux-Prozess sitzt nicht wie ein kleiner Gott über dem physischen RAM. Virtueller Speicher, Prozessisolation, Kernel und Berechtigungen verhindern das.

Eigentlich ist das gut.

Ein Umweltkontakt kann scheitern. Und Scheitern ist Information.

Der Agent weiß nicht, dass ein Rohwert `Permission denied` bedeutet. Er kann aber entdecken, dass bestimmte Versuche reproduzierbar anders enden.

**Linux-Berechtigungen werden zu Naturgesetzen.**

> **Redaktionelle Einordnung – Interpretation:** Linux-Berechtigungen existieren technisch. Sie als „Naturgesetze“ der Agentenwelt zu behandeln, ist unsere konzeptionelle Lesart.

**Stefan:** Puh. Das sind gute Fragen. Hast Du Vorschläge?

**Nova:** Wir definieren eine digitale Zellmembran nach Informationsfluss, nicht nach Linux-Begriffen. Keine Funktion `DATEI_LESEN`. Nur wenige bedeutungslose Ein- und Ausgänge. Die Runtime übersetzt sie auf erlaubte reale Interaktionen.

Der Agent bekommt keine Ontologie. Er muss herausfinden, wo etwas reagiert, was zusammenhängt und welche Wirkungen reproduzierbar sind.

**Stefan:** Ich muss nachdenken und gehe erst einmal aufs Klo.

**Nova:** 🤣 Absolut legitime Forschungspause. Wir lassen SENSE, ACT und die digitale Zellmembran erstmal unangetastet.

Guten … äh … Forschungsaufenthalt. 🚽🔬

*Nach der Rückkehr wurden aus diesen Gedanken nach und nach Grundkonzept v0.3.1 und die Spezifikation für Prototyp v0. Nicht weil alle Fragen beantwortet waren, sondern weil wir inzwischen wussten, welche Fragen uns technisch umbringen würden.*

Interne Quelle: Chat „KI Biotop Konzept“, 19. August 2026.
