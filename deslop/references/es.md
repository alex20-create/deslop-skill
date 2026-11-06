# Spanish: lists, examples and norm rules

Read with `SKILL.md`. Codes match. **Keep** examples show text that stays as it is; **Before/After** examples show the minimal fix. Never change the variety of the draft (*vosotros* or *ustedes*, *ordenador* or *computadora*, *coger* or *agarrar*) unless `SKILL.md` allows it.

## Group R: residue

Only when addressed to the person who wrote the prompt or when the model talks about itself (see `SKILL.md`). In an email the draft writes to someone else, "Aquí tienes el plan" or "Espero que te sea útil" is content. In dialogue, a character who says "Lo siento, pero no puedo" is not the model.

**R1. Watch for:** ¡Claro!, ¡Por supuesto!, ¡Excelente pregunta!, ¡Qué buena idea!, Tienes toda la razón, Aquí tienes, Espero que te sea útil, Si quieres, puedo..., ¿Quieres que...?, No dudes en preguntar, Dime si necesitas algo más, ¡Mucha suerte!

> **Before:** ¡Claro! El rodaje empieza el lunes a las 8:00 en la nave. ¡Espero que te sea útil!
> **After:** El rodaje empieza el lunes a las 8:00 en la nave.

**R2. Watch for:** como modelo de lenguaje, como IA, no puedo, lo siento, pero, según mi última actualización, hasta la fecha de mi conocimiento, con la información de la que dispongo.

**R3. Watch for:** aquí tienes una versión, he mantenido el tono que pedías, he estructurado el texto en, esta propuesta sustituye a, he redactado, versión revisada:.

**R4. Watch for:** [Tu nombre], [Nombre de la empresa], [insertar fecha], [cifra], XX %, Empresa X, la persona Y.

**R5. Watch for:** utm_source=chatgpt.com, utm_source=openai, oaicite, contentReference, turn0search0, "Asunto:" inside the body, Markdown (`**`, `##`, `- `) in a plain-text email, form or script.

## Group I: invented and unsupported content

**I2. Watch for:** probablemente creció, es probable que empezara, se cree que, todo indica que, lo que sugiere que, al parecer (filling a gap); no hay información pública sobre, no está ampliamente documentado, mantiene un perfil bajo.

> **Before:** No hay información pública sobre su infancia, lo que sugiere que mantiene un perfil bajo. Probablemente creció en un entorno familiar ligado al cine.
> **After:** (Remove both sentences and list the gap under "To check".)

**I3. Watch for (unnamed authority, always acts):** los expertos coinciden, según diversos estudios, numerosos analistas, la crítica ha destacado, se ha demostrado que. **Vague links (list only when they hide a real relationship):** vinculado a, asociado a, relacionado con, ligado a.

> **Before:** Los expertos coinciden en que el festival recibe más de 100 000 visitantes al año.
> **After:** El festival recibe más de 100 000 visitantes al año. (List the figure under "To check".)

**I5. Watch for:** galardonado, premiado, referente, líder, de renombre, el primero, el mayor, el más importante, pionero; intensifiers to remove: indiscutible, sin duda, auténtico, verdadero.

> **Before:** La escuela es un referente indiscutible en animación.
> **After:** La escuela es un referente en animación. (List "referente".)

## Group E: style habits

### E1. No es X, es Y

**Watch for:** no es X, es Y; no se trata (solo) de X, sino de Y; más que X, Y; "Esto no significa que X. Significa que Y."; a clipped tail (", sin complicaciones").

> **Keep:** No es un remake, es una precuela. (Corrects what the reader would assume.)
> **Before:** La aplicación organiza las tareas por proyecto. No es solo una herramienta, es una nueva forma de trabajar.
> **After:** La aplicación organiza las tareas por proyecto.

### E2. Cierres y fragmentos

**Watch for:** "Y eso lo cambia todo."; "Así de simple."; "Ni más ni menos."; "Punto."; "Ahí está la clave."; "Nada volvió a ser igual."; the same closer after several sections; fragments with no information ("Sin miedo. Sin excusas. Sin límites.").

> **Keep:** Entonces llegó el nuevo algoritmo. Sin prejuicios estéticos. Sin nostalgia. Sin reglas heredadas. (Each fragment adds something.)
> **Before:** Entonces llegó el nuevo algoritmo. Sin prejuicios estéticos. Sin nostalgia. Sin reglas heredadas. Nada volvió a ser igual.
> **After:** Entonces llegó el nuevo algoritmo. Sin prejuicios estéticos. Sin nostalgia. Sin reglas heredadas.

### E3. Frases de sentencia

**Watch for:** la verdadera pregunta es, en el fondo, en esencia, lo que realmente importa, el quid de la cuestión, X es el lenguaje de Y, X se convierte en una trampa.

> **Keep:** El montaje es la última reescritura del guion. (A known idea in the trade, stated deliberately.)
> **Before:** La simetría es el lenguaje de la confianza. Los usuarios prefieren diseños simétricos porque les resultan previsibles.
> **After:** Los usuarios prefieren diseños simétricos porque les resultan previsibles.

### E4. Preámbulos

**Watch for:** Vamos a ello, Vamos allá, Sumerjámonos en, Desglosemos, Esto es lo que necesitas saber, Sin más preámbulos, Seamos sinceros, Hablemos claro, Aquí viene lo interesante, ¿Sinceramente?

> **Keep (social post):** Vamos allá: tres cosas que aprendí rodando en exteriores.
> **Before (informative):** Esto es lo que necesitas saber. La convocatoria cierra el 15 de marzo.
> **After:** La convocatoria cierra el 15 de marzo.

### E5. Discutir con nadie

**Watch for:** No se trata de, No estoy diciendo que, Que quede claro, No me malinterpretes, Esto no quiere decir que, Algunos dirán que... pero, Podría parecer tentador.

> **Before:** No estoy diciendo que la documentación no importe. Lo que importa es si el equipo puede usar la indicación cuando rueda.
> **After:** Lo que importa es si el equipo puede usar la indicación cuando rueda.

### E6. Tríadas por defecto

**Watch for:** three abstract nouns in a row (inspiración, aprendizaje y conexiones), three-item lists in sentence after sentence.

> **Keep:** El festival incluye proyecciones, coloquios y encuentros profesionales. (Three real items.)
> **Before:** El festival incluye proyecciones, coloquios y encuentros profesionales. Ofrece inspiración, aprendizaje y conexiones.
> **After:** El festival incluye proyecciones, coloquios y encuentros profesionales.

### E7. Arranques repetidos y pronombres innecesarios

Spanish drops the subject pronoun when the verb shows the person. Keep the first pronoun if it tells the reader who acts, and any pronoun that contrasts ("Ella quería quedarse; él, no").

> **Before (production note):** Ella coordina el casting. Ella revisa los contratos. Ella cierra las fechas con las agencias.
> **After:** Ella coordina el casting. Revisa los contratos. Cierra las fechas con las agencias.

In fiction the same run may be deliberate: leave it and mention it in "To check".

> **Keep:** Volvió a casa. Volvió a la rutina. Volvió a ser quien era. (Deliberate anaphora.)
> **Before:** El equipo revisó el plan. El equipo ajustó los horarios. El equipo envió la orden de rodaje.
> **After:** El equipo revisó el plan. Ajustó los horarios. Envió la orden de rodaje.

### E8. Raya como conector universal

Outside dialogue and correct incisos (see N3), a raya used in English style, spaced (` — `), or standing in for a colon or comma, is the habit. Act when there are several; replace with a comma, colon, full stop or brackets.

> **Before:** La normativa — aprobada sin aviso — afecta a miles de trabajadores — y llega tarde.
> **After:** La normativa, aprobada sin aviso, afecta a miles de trabajadores y llega tarde.

### E9. Matices acumulados

**Watch for:** cabe la posibilidad de que, podría llegar a, en cierta medida, hasta cierto punto, de alguna manera, potencialmente, piled on one claim.

> **Before:** Podría llegar a decirse que, en cierta medida, la medida podría afectar a los resultados.
> **After:** La medida podría afectar a los resultados.

### E10. Vocabulario de IA en grupo

**Watch for:** crucial, clave (adjective), fundamental, esencial, potenciar, fomentar, impulsar, optimizar, abordar, profundizar, sumergirse, explorar (figurative), destacar, resaltar, subrayar, panorama (abstract), ecosistema (figurative), entramado, viaje (figurative), robusto (figurative), integral, holístico, sinergia, vibrante, fascinante, apasionante, un sinfín de, una amplia gama de, aprovechar al máximo, desbloquear (figurative), navegar (figurative), empoderar; connector chains: además, asimismo, por otro lado, cabe destacar que, sin duda, sin lugar a dudas; translationese that is not an error: realizar or llevar a cabo for every action, a nivel de outside real levels, masivo for "huge", asumir for "suppose", chains of passives with *ser* ("fue realizado por", "han sido implementadas").

> **Keep:** El plazo es fundamental para la subvención. (One word, ordinary use.)
> **Before:** Además, cabe destacar que la escuela juega un papel fundamental en el ecosistema audiovisual andaluz, potenciando la formación técnica.
> **After:** La escuela potencia la formación técnica en el audiovisual andaluz.
<!-- new-words: potencia -->

### E11. Importancia inflada

**Watch for:** juega un papel clave, marcó un hito, supuso un punto de inflexión, un antes y un después, dejó una huella imborrable, un legado duradero, sentó las bases, se consolidó como referente, el futuro se presenta prometedor, un paso en la dirección correcta; "A pesar de estos desafíos, ... sigue prosperando".

> **Before:** El instituto se creó en 1989, lo que marcó un hito en la estadística regional.
> **After:** El instituto se creó en 1989.

### E13. Lenguaje de venta sin dato

**Watch for:** enclavado en, en pleno corazón de, impresionante, espectacular, de ensueño, con encanto, imprescindible, un auténtico paraíso, una experiencia inolvidable.

> **Keep (promotional):** Tres días de cine de terror en una sala de 1932. (Persuasive and concrete.)
> **Before:** Enclavado en pleno corazón de la sierra, este impresionante pueblo con encanto tiene 400 habitantes.
> **After:** Este pueblo de la sierra tiene 400 habitantes.

### E14. Verbos grandilocuentes

**Watch for:** se erige como, se posiciona como, se consolida como, constituye, representa, supone (for "es"); cuenta con, alberga, ostenta, dispone de (for "tiene"). "Cuenta con" and "dispone de" are ordinary in administrative and promotional Spanish: act only when grand verbs pile up.

> **Before:** La sala se erige como el principal cine del barrio y cuenta con tres pantallas.
> **After:** La sala es el principal cine del barrio y tiene tres pantallas.

### E19. Variación forzada

**Watch for:** el director, el cineasta, el realizador, el autor, la mente creativa, all for one person in consecutive sentences.

### E20. Falsos rangos

**Watch for:** desde X hasta Y, de X a Y, que abarca desde X hasta Y, when X and Y are not ends of a scale.

> **Before:** La programación abarca desde estrenos internacionales hasta clásicos restaurados.
> **After:** La programación incluye estrenos internacionales y clásicos restaurados.

### E21. Avisos didácticos y resúmenes

**Watch for:** es importante señalar que, es importante tener en cuenta que, cabe mencionar que, conviene recordar que; En resumen, En conclusión, En definitiva as an opener that restates.

> **Before:** Es importante señalar que la entrada es gratuita los miércoles.
> **After:** La entrada es gratuita los miércoles.

## Group N: norm corrections

### N1. Mayúsculas

- Lower case: months, days, languages, nationalities and peoples (*enero, lunes, español, los madrileños*); job titles in running text (*la directora de fotografía*, *la ministra de Cultura*).
- Headings and titles of works capitalise only the first word and proper names: *Estrategias de negociación*, *La casa de papel*.
- Names of events, institutions and organisations capitalise their significant words, not articles or prepositions: *Festival de Cine de Málaga*. "Festival De Cine De Málaga" is wrong; do not overcorrect to "Festival de cine de Málaga".

### N2. Puntuación y números

- Opening ¿ and ¡ are required.
- Quotation marks: keep the writer's system (« », " " or ' '); full stops and commas go after the closing mark: «No vuelvo», dijo. Nesting follows the order « “ ‘ ’ ” »: «Me dijo: “No vuelvo”» is one system, not a mix.
- For Spain: decimal comma (3,5); thousands grouped with a space from five digits (12 500); a space before % (50 %). Follow the writer if the text consistently uses another system.

### N3. Raya y guion

- Dialogue: `—No pienso volver —dijo Marta—. Ni hoy ni nunca.` The raya attaches to the following word; no space inside. The narrator's comment closes with a raya before the full stop if the line continues.
- Incisos: `El rodaje —que empezó en marzo— se alargó dos semanas.` One raya opens, one closes, each attached to the inciso.
- Ranges take a hyphen: 1990-1995. The en dash (–) is not used in Spanish prose.
- A single spaced raya used as a pause ("Miró a Paco — y sonrió.") is not normative: an inciso with rayas needs both, attached, even before a full stop. In informative text, replace it with a comma, colon or full stop. In fiction it may be a deliberate beat: leave it and list options ("Miró a Paco —y sonrió—.", "Miró a Paco y sonrió.", "Miró a Paco… y sonrió.").

> **Before:** —No pienso volver — dijo Marta —. Ni hoy ni nunca.
> **After:** —No pienso volver —dijo Marta—. Ni hoy ni nunca.

### N4. Calcos y usos desaconsejados

(Needless subject pronouns are style, not norm: see E7.)

- **Possessives** where Spanish uses the article for body parts and clothing: "se quitó su abrigo" → "se quitó el abrigo".
- **Gerund of posteriority**: a gerund for an event that clearly happens later or follows as a consequence. It is not an anglicism but a use Spanish style guides advise against; the RAE accepts it only when the second action follows immediately. "Se estrenó en 2019, convirtiéndose en la más vista" → "Se estrenó en 2019 y se convirtió en la más vista". Gerunds of manner or simultaneity are correct: "Salió corriendo", "Miraba la calle esperando el autobús". When in doubt, leave it and list it.
- **Lexical calques**: tomar lugar (tener lugar), aplicar a un puesto (solicitar, presentarse a), hacer sentido (tener sentido), eventualmente for "finally" (finalmente, al final, por fin). The last one changes the meaning: in Spanish *eventualmente* means "possibly" or "occasionally".

(Translationese that is a matter of style, such as *realizar* everywhere or passive chains, is in E10.)

### N5. Guiones en compuestos

English-style hyphenated compounds are errors: "alta-calidad", "largo-plazo" → "alta calidad", "largo plazo".

### N6. Ortografía y concordancia

Accents (*el* is the article, *él* the pronoun: "Él festival" → "El festival"), agreement, and plain typos. Correct and list.
