export async function fetchAnalytics(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      query.append(key, value);
    }
  });

  const response = await fetch(`/analytics/summary?${query.toString()}`);
  if (!response.ok) throw new Error(`API error: ${response.status}`);

  const result = await response.json();
  if (!result.success) throw new Error(result.message || "API returned an error");
  return result;
}
