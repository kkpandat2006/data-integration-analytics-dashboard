import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { useData } from "../context/DataContext";

const STATUS_COLORS = { Delivered: "var(--success)", Delayed: "var(--danger)", Unknown: "var(--text-muted)" };

function DeliveryChart({ data }) {
  const { dispatch } = useData();

  const handleClick = (entry) => {
    dispatch({
      type: "SET_DRILL_DOWN",
      payload: { type: "status", value: entry.status, count: entry.count },
    });
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={65}
          outerRadius={105}
          paddingAngle={4}
          dataKey="count"
          nameKey="status"
          onClick={handleClick}
          style={{ cursor: "pointer" }}
        >
          {data.map((entry, i) => (
            <Cell key={i} fill={STATUS_COLORS[entry.status] || "var(--text-muted)"} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 8, fontFamily: "DM Mono, monospace", fontSize: 12 }}
        />
        <Legend
          wrapperStyle={{ fontFamily: "DM Mono, monospace", fontSize: 12, color: "var(--text-secondary)" }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}

export default DeliveryChart;
