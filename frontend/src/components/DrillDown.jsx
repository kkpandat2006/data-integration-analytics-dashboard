import { useData } from "../context/DataContext";

function DrillDown() {
  const { drillDown, dispatch } = useData();

  if (!drillDown) return null;

  return (
    <div className="drilldown">
      <div className="drilldown-header">
        <h3>Drill-Down Detail</h3>
        <button className="btn-close" onClick={() => dispatch({ type: "CLEAR_DRILL_DOWN" })}>
          Close
        </button>
      </div>
      <div className="drilldown-content">
        <div className="drilldown-item">
          <span className="label">
            {drillDown.type === "category" ? "Category" : drillDown.type === "date" ? "Date" : "Status"}
          </span>
          <span className="value">{drillDown.value}</span>
        </div>
        {drillDown.revenue !== undefined && (
          <div className="drilldown-item">
            <span className="label">Revenue</span>
            <span className="value">${drillDown.revenue?.toLocaleString()}</span>
          </div>
        )}
        {drillDown.orderCount !== undefined && (
          <div className="drilldown-item">
            <span className="label">Orders</span>
            <span className="value">{drillDown.orderCount}</span>
          </div>
        )}
        {drillDown.count !== undefined && drillDown.type === "status" && (
          <div className="drilldown-item">
            <span className="label">Count</span>
            <span className="value">{drillDown.count}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default DrillDown;