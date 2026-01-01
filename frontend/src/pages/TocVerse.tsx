import { useState, useEffect } from "react";
import {useParams} from "react-router-dom";
import { tocVerseApi } from "../api/tocVerse";
import type { TocVerseInterface } from "../api/tocVerse";
import {Link} from "react-router-dom";


export const TocVerse = () => {
  const {collectionId} = useParams<{collectionId: string}>();

  const [data, setData] = useState<TocVerseInterface[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");



  useEffect(() => {
    if (!collectionId) return;

    tocVerseApi(Number(collectionId))
      .then((toc) => setData(toc))
      .catch((e) => {
        console.log("Failed to load toc of vers");
        setError(e);
      })
      .finally(() => setLoading(false));
  }, [collectionId]);

  if (loading) {
    return <span>Loading</span>;
  }
  if (error) {
    return <span>{error}</span>;
  }

  return (
    <div className="container mt-4">
      <div className="card shadow-sm">
        <div className="card-body">
          <h5 className="card-title mb-3">
            Table of Contents
          </h5>

          <ul className="list-group list-group-flush">
            {data.map((item) => (
              <li
                key={item.id}
                className="list-group-item px-0"
              >
                {item.title}
                <Link to={`/verse/${item.id}`}>
                  Open verse
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
