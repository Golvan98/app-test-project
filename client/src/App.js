import React, { useState, useEffect } from "react";

function App() {
  const [user, setUser] = useState(null);
  const [meters, setMeters] = useState("");
  const [feet, setFeet] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/me", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.error) setUser(data);
      });
  }, []);

  const handleConvert = async () => {
    try {
      const res = await fetch("/convert", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ value: meters }),
      });

      if (!res.ok) throw new Error("Conversion failed");

      const data = await res.json();
      setFeet(data.feet);
      setError("");
    } catch (err) {
      setError("Error converting");
    }
  };

  return (
    <div
      className="App"
      style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}
    >
      <h2>Unit Converter (Meters → Feet)</h2>

      {user ? (
        <>
          <p>
            Welcome, {user.name} ({user.email})
          </p>

          <div style={{ marginBottom: "1rem" }}>
            <input
              type="number"
              value={meters}
              onChange={(e) => setMeters(e.target.value)}
              placeholder="Enter meters"
              style={{ marginRight: "1rem" }}
            />
            <button onClick={handleConvert}>Convert</button>
          </div>

          {feet !== null && <p>{meters} meters = {feet} feet</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}

          <br />
          <a href="/logout">Logout</a>
        </>
      ) : (
        <a href="/login/google">Login with Google</a>
      )}
    </div>
  );
}

export default App;
