import { useMemo, useState } from "react";
import type { WordTranslationType, WordType, Lang } from "../api/verse";
import { Search } from "./Search"; // adjust path if needed
import { Filter, type FreqFilterValue } from "./Filter";
import { Sort, type SortValue } from "./Sort";

type UiLang = Lang; // "en" | "ru" | "uk"

const LANG_LABEL: Record<UiLang, string> = {
  en: "English",
  ru: "Russian",
  uk: "Ukrainian",
};

type ThesaurusCardProps = {
  translations: WordTranslationType[];
  words: WordType[];
};

export function ThesaurusCard({ translations, words }: ThesaurusCardProps) {
  const [lang, setLang] = useState<UiLang>("en");
  const [query, setQuery] = useState("");
  const [freq, setFreq] = useState<FreqFilterValue>({});
  const [sort, setSort] = useState<SortValue>({ key: "freq", dir: "desc" });

  const wordByLemma = useMemo(() => {
    const map = new Map<string, WordType>();
    for (const w of words) map.set(w.lemma, w);
    return map;
  }, [words]);

  const items = useMemo(() => {
    const q = query.trim().toLowerCase();

    // 1) language
    let arr = translations.filter((t) => t.lang === lang);

    // 2) search
    if (q) {
      arr = arr.filter((t) => {
        const lemma = (t.lemma ?? "").toLowerCase();
        const trans = (t.trans ?? "").toLowerCase();
        return lemma.includes(q) || trans.includes(q);
      });
    }

    // 3) freq filter
    if (freq.min !== undefined || freq.max !== undefined) {
      arr = arr.filter((t) => {
        const f = wordByLemma.get(t.lemma)?.freq ?? 0;
        if (freq.min !== undefined && f < freq.min) return false;
        if (freq.max !== undefined && f > freq.max) return false;
        return true;
      });
    }

    // 4) sort
    const dirMul = sort.dir === "asc" ? 1 : -1;

    const freqOf = (t: WordTranslationType) =>
      wordByLemma.get(t.lemma)?.freq ?? 0;
    const lemmaOf = (t: WordTranslationType) => t.lemma ?? "";
    const transOf = (t: WordTranslationType) => t.trans ?? "";

    const cmpStr = (a: string, b: string) => a.localeCompare(b);

    return [...arr].sort((a, b) => {
      if (sort.key === "freq") {
        const fa = freqOf(a);
        const fb = freqOf(b);
        if (fa !== fb) return (fa - fb) * dirMul;
        return cmpStr(lemmaOf(a), lemmaOf(b));
      }
      if (sort.key === "lemma") {
        const c = cmpStr(lemmaOf(a), lemmaOf(b));
        if (c !== 0) return c * dirMul;
        return cmpStr(transOf(a), transOf(b)) * dirMul;
      }
      // translation
      const c = cmpStr(transOf(a), transOf(b));
      if (c !== 0) return c * dirMul;
      return cmpStr(lemmaOf(a), lemmaOf(b)) * dirMul;
    });
  }, [translations, lang, query, freq, sort, wordByLemma]);

  if (translations.length === 0) {
    return <div className="text-muted">No thesaurus entries available.</div>;
  }

  return (
    <div className="container mt-3">
      {/* Language tabs */}
      <div className="mb-3 d-flex align-items-center gap-2 flex-wrap">
        <div className="btn-group" role="group">
          {(["en", "ru", "uk"] as const).map((code) => (
            <button
              key={code}
              type="button"
              className={`btn btn-sm ${
                lang === code ? "btn-primary" : "btn-outline-primary"
              }`}
              onClick={() => setLang(code)}
            >
              {LANG_LABEL[code]}
            </button>
          ))}
        </div>

        <span className="text-muted small ms-auto">{items.length} items</span>
      </div>

      {/* Search / Filter / Sort */}
      <Search
        value={query}
        onChange={setQuery}
        placeholder={`Search in ${LANG_LABEL[lang]}…`}
      />

      <Filter value={freq} onChange={setFreq} />

      <Sort value={sort} onChange={setSort} />

      {/* List */}
      {items.length === 0 ? (
        <div className="text-muted">No matches.</div>
      ) : (
        <div className="list-group">
          {items.map((t) => {
            const word = wordByLemma.get(t.lemma);

            return (
              <div key={t.id} className="list-group-item">
                <div className="d-flex justify-content-between align-items-center">
                  <div className="fw-semibold text-primary">{t.lemma}</div>

                  {word && (
                    <div className="text-muted small">
                      freq: {word.freq}
                      {word.neologism ? " • neologism" : ""}
                    </div>
                  )}
                </div>

                <div className="mt-1">
                  {t.trans || <span className="text-muted">(empty)</span>}
                </div>

              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
