import React, { useState, useEffect } from "react";
import "./App.css";

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
    <div className="App">
      <div className="card">
        <h2 className="title">Unit Converter (Meters → Feet)</h2>

        {user ? (
          <>
            <p className="welcome">
              Welcome, <strong>{user.name}</strong> ({user.email})
            </p>

            <div className="input-group">
              <input
                type="number"
                value={meters}
                onChange={(e) => setMeters(e.target.value)}
                placeholder="Enter meters"
              />
              <button onClick={handleConvert}>Convert</button>
            </div>

            {feet !== null && <p className="result">{meters} meters = {feet} feet</p>}
            {error && <p className="error">{error}</p>}

            <a className="link" href="/logout">Logout</a>
          </>
        ) : (
          <a className="link" href="/login/google">Login with Google</a>
        )}
      </div>
    </div>
  );
}

export default App;
