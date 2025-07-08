import React, { useState } from "react";

function Converter() {
  const [meters, setMeters] = useState("");
  const [feet, setFeet] = useState(null);
  const [error, setError] = useState("");

  const handleConvert = async () => {
    try {
      const res = await fetch("http://localhost:5000/convert", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ value: meters }),
        credentials: "include"
      });

      if (!res.ok) throw new Error("Failed to convert");

      const data = await res.json();
      setFeet(data.feet);
      setError("");
    } catch (err) {
      setError("Error converting");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Meter to Feet Converter</h2>
      <input
        type="number"
        value={meters}
        onChange={(e) => setMeters(e.target.value)}
        placeholder="Enter meters"
        style={{ marginRight: "1rem" }}
      />
      <button onClick={handleConvert}>Convert</button>
      {feet !== null && <p>{meters} meters = {feet} feet</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Converter;
