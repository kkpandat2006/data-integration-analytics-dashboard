function KPICard({ title, value, color, subtitle }) {
  return (
    <div className="kpi-card" style={{ borderTopColor: color }}>
      <span className="kpi-title">{title}</span>
      <span className="kpi-value">{value}</span>
      {subtitle && <span className="kpi-subtitle">{subtitle}</span>}
    </div>
  );
}

export default KPICard;
