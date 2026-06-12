import React, { useState } from "react";
import { createRoot } from "react-dom/client";

const API = "http://localhost:8100/api/v1/simulation";

function App() {
  const [result, setResult] = useState(null);

  async function runFullSimulation() {
    const res = await fetch(`${API}/run/full-school-network`, { method: "POST" });
    const data = await res.json();
    setResult(data);
  }

  return (
    <div style={{ fontFamily: "Arial", padding: "32px" }}>
      <h1>QCCP School Network Simulator</h1>
      <p>MOEHE oversight, 20 schools, 60 TerraAir devices.</p>

      <button onClick={runFullSimulation}>
        Run Full School Simulation
      </button>

      {result && (
        <pre style={{ marginTop: "24px", background: "#f4f4f4", padding: "16px" }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
