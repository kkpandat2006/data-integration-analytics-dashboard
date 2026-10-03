import { useEffect } from "react";
import { useData } from "../context/DataContext";
import KPICard from "./KPICard";
import Filters from "./Filters";
import ViewToggle from "./ViewToggle";
import RevenueChart from "./RevenueChart";
import CategoryChart from "./CategoryChart";
import DeliveryChart from "./DeliveryChart";
import DrillDown from "./DrillDown";

function Dashboard() {
  const { data, loading, error, filters, loadData, dispatch } = useData();

  useEffect(() => {
    loadData(filters, 1);
  }, []);

  const handleApplyFilters = (newFilters) => {
    dispatch({ type: "SET_FILTERS", payload: newFilters });
    loadData(newFilters, 1);
  };

  const handlePageChange = (newPage) => {
    dispatch({ type: "SET_PAGE", payload: newPage });
    loadData(filters, newPage);
  };

  if (loading && !data) {
    return (
      <div className="dashboard">
        <div className="loading-state">
          <div className="spinner" />
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="dashboard">
        <div className="error-state">
          <h2>Something went wrong</h2>
          <p>{error}</p>
          <button onClick={() => loadData(filters, 1)}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>Analytics Dashboard</h1>
          <p className="subtitle">Order &amp; delivery insights</p>
        </div>
      </header>

      <div className="kpi-grid">
        <KPICard title="Total Orders" value={data?.total_orders ?? 0} color="var(--accent)" />
        <KPICard title="Total Revenue" value={`$${(data?.total_revenue ?? 0).toLocaleString()}`} color="var(--success)" />
        <KPICard title="Delayed Orders" value={data?.delayed_orders ?? 0} color="var(--danger)" />
      </div>

      <div className="controls-row">
        <Filters onApply={handleApplyFilters} />
        <ViewToggle />
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Revenue Trend</h3>
          <RevenueChart data={data?.revenue_trend || []} />
        </div>
        <div className="chart-card">
          <h3>Revenue by Category</h3>
          <CategoryChart data={data?.categories || []} />
        </div>
      </div>

      <div className="charts-grid charts-grid--single">
        <div className="chart-card">
          <h3>Delivery Performance</h3>
          <DeliveryChart data={data?.delivery_performance || []} />
        </div>
      </div>

      {data?.orders?.length > 0 && (
        <div className="orders-section">
          <h3>Order Details</h3>
          <div className="orders-table-wrapper">
            <table className="orders-table">
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Customer</th>
                  <th>Date</th>
                  <th>Total Value</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {data.orders.map((order) => (
                  <tr key={order.order_id} className={order.delay_flag ? "row-delayed" : ""}>
                    <td>{order.order_id}</td>
                    <td>{order.customer_name}</td>
                    <td>{order.order_date}</td>
                    <td>${order.total_value?.toLocaleString()}</td>
                    <td>
                      <span className={`status-badge ${(order.delivery_status || "").toLowerCase()}`}>
                        {order.delivery_status || "N/A"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {data.pagination && data.pagination.total_pages > 1 && (
            <div className="pagination">
              {Array.from({ length: data.pagination.total_pages }, (_, i) => (
                <button
                  key={i + 1}
                  className={`page-btn ${data.pagination.page === i + 1 ? "active" : ""}`}
                  onClick={() => handlePageChange(i + 1)}
                >
                  {i + 1}
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      <DrillDown />
    </div>
  );
}

export default Dashboard;
