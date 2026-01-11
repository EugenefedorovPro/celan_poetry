type SortDirection = "asc" | "desc";

export type SortValue = {
  key: "freq" | "lemma" | "translation";
  dir: SortDirection;
};

type SortProps = {
  value: SortValue;
  onChange: (value: SortValue) => void;
};

export function Sort({ value, onChange }: SortProps) {
  return (
    <div className="mb-3">
      <div className="d-flex gap-2 align-items-center">
        <select
          className="form-select"
          value={value.key}
          onChange={(e) =>
            onChange({ ...value, key: e.target.value as SortValue["key"] })
          }
        >
          <option value="freq">Frequency</option>
          <option value="translation">Translation</option>
          <option value="lemma">Lemma</option>
        </select>

        <button
          type="button"
          className="btn btn-outline-secondary"
          onClick={() =>
            onChange({ ...value, dir: value.dir === "asc" ? "desc" : "asc" })
          }
          title="Toggle direction"
        >
          {value.dir === "asc" ? "↑" : "↓"}
        </button>
      </div>
    </div>
  );
}
