import { useState, useEffect } from "react";
import { collectionApi } from "../api/collection";
import type { CollectionInterface } from "../api/collection";
import {Link} from "react-router-dom";

const Collection = () => {
  const [data, setData] = useState<CollectionInterface[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    collectionApi()
      .then((collection) => setData(collection))
      .catch((e) => {
        console.error(e);
        setError(`Failed to load collection with the Error: ${e}`);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <span>Loading</span>;
  }
  if (error) {
    return <span>{error}</span>;
  }

  return (
    <div className="container mt-4">
      <div className="row g-3">
        {data.map((item) => (
          <div
            key={item.pk}
            className="col-12 col-md-6 col-lg-4"
          >
            <div className="card h-100 shadow-sm">
              <div className="card-body">
                {/* Title */}
                <h5 className="card-title mb-1">
                  {item.name}
                </h5>

                {/* Genre */}
                <h6 className="card-subtitle text-muted mb-3">
                  {item.genre}
                </h6>

                {/* Meta info */}
                <ul className="list-unstyled mb-3">
                  <li>
                    <strong>Year of publication:</strong>{" "}
                    {item.year_publication}
                  </li>

                  <li>
                    <strong>Real Celan collection:</strong>{" "}
                    <span className="text-capitalize">
                      {item.is_real_celan_collection}
                    </span>
                  </li>

                  <li>
                    <strong>Number of verses:</strong>{" "}
                    {item.number_verses}
                  </li>

                  <li className="mt-2">
                    <Link
                      to={`/collections/${item.pk}/toc`}
                      className="btn btn-sm btn-outline-primary"
                    >
                      Open list of verses
                    </Link>
                  </li>
                </ul>

                {/* Notes */}
                {item.notes && (
                  <>
                    <hr />
                    <p className="card-text small text-secondary mb-0">
                      {item.notes}
                    </p>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Collection;
