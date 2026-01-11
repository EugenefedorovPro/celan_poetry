export type FreqFilterValue = {
  min?: number;
  max?: number;
};

type FilterProps = {
  value: FreqFilterValue;
  onChange: (value: FreqFilterValue) => void;
};

export function Filter({ value, onChange }: FilterProps) {
  return (
    <div className="mb-3">
      <div className="d-flex gap-2">
        <input
          type="number"
          className="form-control"
          placeholder="min freq"
          value={value.min ?? ""}
          onChange={(e) =>
            onChange({
              ...value,
              min: e.target.value === "" ? undefined : Number(e.target.value),
            })
          }
        />

        <input
          type="number"
          className="form-control"
          placeholder="max freq"
          value={value.max ?? ""}
          onChange={(e) =>
            onChange({
              ...value,
              max: e.target.value === "" ? undefined : Number(e.target.value),
            })
          }
        />
      </div>
    </div>
  );
}
