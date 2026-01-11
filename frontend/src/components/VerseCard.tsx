import type { VerseType } from "../api/verse";

type VerseCardProps = {
  data: VerseType;
};

export function VerseCard({ data }: VerseCardProps) {
  return (
    <div className="container mt-4">
      <div className="card shadow-sm">
        <div className="card-body">
          {/* Title */}
          <h5 className="card-title mb-3">{data.title}</h5>

          {/* Collection */}
          <h6 className="card-subtitle text-muted mb-2">
            {data.collection_name}
          </h6>

          {/* Years */}
          <div className="mb-3 text-muted small">
            {data.year_writing !== 0 && <div>Written: {data.year_writing}</div>}
            {data.year_publication !== 0 && (
              <div>Published: {data.year_publication}</div>
            )}
          </div>

          {/* Text */}
          <p className="card-text" style={{ whiteSpace: "pre-line" }}>
            {data.text}
          </p>
        </div>
      </div>
    </div>
  );
}
