import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useData } from "../context/DataContext";

function RevenueChart({ data }) {
  const { viewMode, dispatch } = useData();

  const dataKey = viewMode === "revenue" ? "revenue" : "order_count";
  const strokeColor = viewMode === "revenue" ? "var(--accent)" : "var(--info)";

  const handleClick = (e) => {
    if (e?.activePayload?.[0]) {
      const p = e.activePayload[0].payload;
      dispatch({
        type: "SET_DRILL_DOWN",
        payload: { type: "date", value: p.date, revenue: p.revenue, orderCount: p.order_count },
      });
    }
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} onClick={handleClick} style={{ cursor: "pointer" }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis dataKey="date" stroke="var(--text-muted)" fontSize={12} tickLine={false} />
        <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} />
        <Tooltip
          contentStyle={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 8, fontFamily: "DM Mono, monospace", fontSize: 12 }}
          labelStyle={{ color: "var(--text-primary)" }}
        />
        <Line
          type="monotone"
          dataKey={dataKey}
          stroke={strokeColor}
          strokeWidth={2}
          dot={{ fill: strokeColor, r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default RevenueChart;
