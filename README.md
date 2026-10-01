# Deutsch für Hasna

German from A1 to B2, with every word translated into **both English and Arabic**, and a switch at the top to move between them.

**Live site:** deployed on Vercel
**Offline:** the whole thing is one HTML file with no external requests, and a service worker caches it after the first visit

## What's in it

| | |
|---|---|
| 1,169 entries | words, phrases, collocations and grammar rules |
| 2,087 Anki cards | in the downloadable `.apkg`, 13 subdecks |
| A1 → B2 | with a level filter |
| 2 languages | English and Arabic, switchable, Arabic rendered right-to-left |

Seven sections: a searchable word list, a flashcard trainer with a spaced queue, 77 grammar cards explained in both languages, a pronunciation guide written specifically for an Arabic speaker, a day-by-day study plan, a directory of free video resources, and setup instructions.

Each entry carries the article and plural for nouns, the principal parts for verbs, a real example sentence, and translations of both the word and the sentence.

## Files

```
index.html                 the whole app, no build step, no dependencies
Deutsch-fuer-Hasna.apkg    the Anki deck, offered as a download
manifest.webmanifest       installs to a phone home screen
sw.js                      offline cache
vercel.json                headers and clean URLs
```

## Running it

Open `index.html`. That is all — there is no build and nothing to install.

To deploy: push to the connected GitHub repo and Vercel rebuilds it, or run `vercel --prod`.

## Notes

The vocabulary was written by hand rather than scraped, so the work vocabulary covers visas, job applications and software, and the B2 layer covers the things that actually separate B1 from B2: verbs with their fixed prepositions, two-part connectors, the passive, Konjunktiv II and relative clauses.

Audio uses the browser's own speech synthesis. Microsoft Edge gives the best free German voices (Katja, Conrad) with no install.
