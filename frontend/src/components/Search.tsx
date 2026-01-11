import type { ChangeEvent } from "react";

type SearchProps = {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
};

export function Search({
  value,
  onChange,
  placeholder = "Search…",
}: SearchProps) {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  return (
    <div className="mb-3">
      <input
        type="text"
        className="form-control"
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        autoComplete="off"
      />
    </div>
  );
}
