import { DataProvider } from "./context/DataContext";
import Dashboard from "./components/Dashboard";
import "./styles/App.css";

function App() {
  return (
    <DataProvider>
      <Dashboard />
    </DataProvider>
  );
}

export default App;
