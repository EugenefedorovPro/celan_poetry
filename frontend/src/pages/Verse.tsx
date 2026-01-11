import { useState, useEffect } from "react";
import type { VerseType } from "../api/verse.ts";
import { verseApi } from "../api/verse.ts";
import { useParams } from "react-router-dom";
import { VerseCard } from "../components/VerseCard"; // <-- adjust path if needed
import { TranslationCard } from "../components/TranslationCard";
import { ThesaurusCard } from "../components/ThesaurusCard";

type Tab = "verse" | "translation" | "thesaurus";

export const Verse = () => {
  const { verseId } = useParams<{ verseId: string }>();

  const [data, setData] = useState<VerseType | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");
  const [tab, setTab] = useState<Tab>("verse");

  useEffect(() => {
    if (!verseId) return;
    verseApi(Number(verseId))
      .then((verse) => setData(verse))
      .catch((e) => {
        console.log(`Failed to fetch verse with error: ${e}`);
        setError(e);
      })
      .finally(() => setLoading(false));
  }, [verseId]);

  if (loading) {
    return <span>Loading</span>;
  }
  if (error) {
    return <span>{error}</span>;
  }

  if (!data) return <span>Not found</span>;

  return (
    <div className="container mt-4">
      {/* Tabs header */}
      <ul className="nav nav-tabs">
        <li className="nav-item">
          <button
            type="button"
            className={`nav-link ${tab === "verse" ? "active" : ""}`}
            onClick={() => setTab("verse")}
          >
            Verse
          </button>
        </li>

        <li className="nav-item">
          <button
            type="button"
            className={`nav-link ${tab === "translation" ? "active" : ""}`}
            onClick={() => setTab("translation")}
          >
            Translation
          </button>
        </li>

        <li className="nav-item">
          <button
            type="button"
            className={`nav-link ${tab === "thesaurus" ? "active" : ""}`}
            onClick={() => setTab("thesaurus")}
          >
            Thesaurus
          </button>
        </li>
      </ul>

      {/* Tabs content */}
      <div className="border border-top-0 p-3">
        {tab === "verse" && <VerseCard data={data} />}
        {tab === "translation" && (
          <TranslationCard translations={data.verse_translations} />
        )}
        {tab === "thesaurus" && (
          <ThesaurusCard
            words={data.words}
            translations={data.word_translations}
          />
        )}
      </div>
    </div>
  );
};
