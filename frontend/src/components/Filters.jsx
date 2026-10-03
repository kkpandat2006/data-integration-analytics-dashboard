import { useState, useEffect } from "react";
import { useData } from "../context/DataContext";

function Filters({ onApply }) {
  const { filters } = useData();
  const [local, setLocal] = useState(filters);

  useEffect(() => {
    setLocal(filters);
  }, [filters]);

  const update = (key, value) => setLocal((f) => ({ ...f, [key]: value }));

  const handleApply = () => onApply(local);

  const handleReset = () => {
    const empty = { date_from: "", date_to: "", category: "", delivery_status: "" };
    setLocal(empty);
    onApply(empty);
  };

  return (
    <div className="filters">
      <div className="filter-group">
        <label>Date From</label>
        <input type="date" value={local.date_from} onChange={(e) => update("date_from", e.target.value)} />
      </div>
      <div className="filter-group">
        <label>Date To</label>
        <input type="date" value={local.date_to} onChange={(e) => update("date_to", e.target.value)} />
      </div>
      <div className="filter-group">
        <label>Category</label>
        <select value={local.category} onChange={(e) => update("category", e.target.value)}>
          <option value="">All</option>
          <option value="Electronics">Electronics</option>
          <option value="Furniture">Furniture</option>
        </select>
      </div>
      <div className="filter-group">
        <label>Status</label>
        <select value={local.delivery_status} onChange={(e) => update("delivery_status", e.target.value)}>
          <option value="">All</option>
          <option value="Delivered">Delivered</option>
          <option value="Delayed">Delayed</option>
        </select>
      </div>
      <button className="btn-apply" onClick={handleApply}>Apply</button>
      <button className="btn-reset" onClick={handleReset}>Reset</button>
    </div>
  );
}

export default Filters;
