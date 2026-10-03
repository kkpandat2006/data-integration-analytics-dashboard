import { createContext, useContext, useReducer, useCallback } from "react";
import { fetchAnalytics } from "../services/api";

const DataContext = createContext(null);

const initialState = {
  data: null,
  loading: false,
  error: null,
  filters: { date_from: "", date_to: "", category: "", delivery_status: "" },
  viewMode: "revenue",
  drillDown: null,
  page: 1,
  pageSize: 10,
};

function reducer(state, action) {
  switch (action.type) {
    case "SET_LOADING":
      return { ...state, loading: action.payload };
    case "SET_DATA":
      return { ...state, data: action.payload, loading: false, error: null };
    case "SET_ERROR":
      return { ...state, error: action.payload, loading: false };
    case "SET_FILTERS":
      return { ...state, filters: { ...state.filters, ...action.payload } };
    case "SET_VIEW_MODE":
      return { ...state, viewMode: action.payload };
    case "SET_DRILL_DOWN":
      return { ...state, drillDown: action.payload };
    case "CLEAR_DRILL_DOWN":
      return { ...state, drillDown: null };
    case "SET_PAGE":
      return { ...state, page: action.payload };
    default:
      return state;
  }
}

export function DataProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const loadData = useCallback(
    async (filters, page = 1) => {
      dispatch({ type: "SET_LOADING", payload: true });
      try {
        const params = { page, page_size: state.pageSize };
        if (filters?.date_from) params.date_from = filters.date_from;
        if (filters?.date_to) params.date_to = filters.date_to;
        if (filters?.category) params.category = filters.category;
        if (filters?.delivery_status) params.delivery_status = filters.delivery_status;

        const result = await fetchAnalytics(params);
        dispatch({ type: "SET_DATA", payload: result.data });
      } catch (err) {
        dispatch({ type: "SET_ERROR", payload: err.message });
      }
    },
    [state.pageSize]
  );

  return (
    <DataContext.Provider value={{ ...state, dispatch, loadData }}>
      {children}
    </DataContext.Provider>
  );
}

export function useData() {
  const ctx = useContext(DataContext);
  if (!ctx) throw new Error("useData must be used within a DataProvider");
  return ctx;
}
