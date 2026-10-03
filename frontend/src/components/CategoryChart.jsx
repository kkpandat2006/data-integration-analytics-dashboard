import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { useData } from "../context/DataContext";

const COLORS = ["var(--accent)", "var(--info)", "var(--success)", "var(--danger)", "#8b5cf6"];

function CategoryChart({ data }) {
  const { viewMode, dispatch } = useData();
  const dataKey = viewMode === "revenue" ? "revenue" : "order_count";

  const handleClick = (e) => {
    if (e?.activePayload?.[0]) {
      const p = e.activePayload[0].payload;
      dispatch({
        type: "SET_DRILL_DOWN",
        payload: { type: "category", value: p.category, revenue: p.revenue, orderCount: p.order_count },
      });
    }
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} onClick={handleClick} style={{ cursor: "pointer" }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis dataKey="category" stroke="var(--text-muted)" fontSize={12} tickLine={false} />
        <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} />
        <Tooltip
          contentStyle={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 8, fontFamily: "DM Mono, monospace", fontSize: 12 }}
        />
        <Bar dataKey={dataKey} radius={[6, 6, 0, 0]}>
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export default CategoryChart;
