import { useState, useEffect } from "react";
import type { VerseInterface } from "../api/verse.ts";
import { verseApi } from "../api/verse.ts";
import { useParams } from "react-router-dom";

export const Verse = () => {
  const { verseId } = useParams<{ verseId: string }>();

  const [data, setData] = useState<VerseInterface>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

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

  return (
    <>
      {data && (
        <div className="container mt-4">
          <div className="card shadow-sm">
            <div className="card-body">
              {/* Collection */}
              <h6 className="card-subtitle text-muted mb-2">
                {data.collection}
              </h6>

              {/* Title */}
              <h5 className="card-title mb-3">{data.title}</h5>

              {/* Text */}
              <p className="card-text" style={{ whiteSpace: "pre-line" }}>
                {data.text}
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
