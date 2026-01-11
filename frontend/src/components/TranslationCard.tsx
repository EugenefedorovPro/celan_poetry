import type { VerseTranslationType } from "../api/verse";

type TranslationCardProps = {
  translations: VerseTranslationType[];
};

export function TranslationCard({ translations }: TranslationCardProps) {
  if (translations.length === 0) {
    return <div className="text-muted">No translations available.</div>;
  }

  return (
    <div className="container mt-3">
      {translations.map((t) => (
        <div key={t.id} className="card mb-3 shadow-sm">
          <div className="card-body">
            {/* Language */}
            <h6 className="card-subtitle mb-2 text-muted">
              {t.lang_display}
              {t.year && <span className="ms-2">({t.year})</span>}
            </h6>

            {/* Title */}
            {t.title && <h5 className="card-title">{t.title}</h5>}

            {/* Text */}
            <p className="card-text" style={{ whiteSpace: "pre-line" }}>
              {t.text}
            </p>

            {/* Meta */}
            {(t.translator || t.source) && (
              <div className="text-muted small">
                {[t.translator, t.source].filter(Boolean).join(" • ")}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
