import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

function SearchPanel() {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const search = async () => {
    if (!keyword) return;
    setLoading(true);
    setError("");

    try {
      const res = await axios.get(`${API_BASE}/search?keyword=${keyword}`, {
        headers: { "x-api-key": "12345" },
      });
      setResults(res.data.results || []);
      setCount(res.data.matches || 0);
    } catch (err) {
      setError("Error fetching results");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-panel">
      <h2>Distributed Scraper Dashboard</h2>
      <div className="search-box">
        <input
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Enter a keyword..."
        />
        <button onClick={search}>Search</button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      <h3>{count} result(s) found</h3>

      <div className="results">
        {results.map((r, idx) => (
          <div className="card" key={idx}>
            <a href={r.url} target="_blank" rel="noreferrer">{r.url}</a>
            <p>{r.clean_text?.slice(0, 400)}...</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchPanel;
