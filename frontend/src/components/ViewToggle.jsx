import { useData } from "../context/DataContext";

function ViewToggle() {
  const { viewMode, dispatch } = useData();

  return (
    <div className="view-toggle">
      <button
        className={`toggle-btn ${viewMode === "revenue" ? "active" : ""}`}
        onClick={() => dispatch({ type: "SET_VIEW_MODE", payload: "revenue" })}
      >
        Revenue
      </button>
      <button
        className={`toggle-btn ${viewMode === "orders" ? "active" : ""}`}
        onClick={() => dispatch({ type: "SET_VIEW_MODE", payload: "orders" })}
      >
        Orders
      </button>
    </div>
  );
}

export default ViewToggle;
