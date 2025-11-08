import { useState } from "react"

function App() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  const search = async (e) => {
    e.preventDefault()
    setLoading(true)
    const res = await fetch(`http://127.0.0.1:8000/search?keyword=${query}`, {
      headers: { "x-api-key": "12345" },
    })
    const data = await res.json()
    setResults(data.results || [])
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-4 shadow-md">
        <div className="container mx-auto px-6 flex items-center justify-between">
          <h1 className="text-2xl font-bold tracking-wide">Distributed Data Explorer</h1>
          <span className="text-sm opacity-80">Step 6 – Web UI</span>
        </div>
      </header>

      <main className="container mx-auto px-6 py-10">
        <form onSubmit={search} className="flex gap-3 mb-8">
          <input
            type="text"
            placeholder="Enter keyword..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 outline-none"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-all"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </form>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((r) => (
            <div
              key={r._id}
              className="bg-white p-5 rounded-2xl shadow hover:shadow-lg transition-shadow border border-gray-100"
            >
              <a
                href={r.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 font-semibold hover:underline"
              >
                {r.url.length > 60 ? r.url.slice(0, 60) + "..." : r.url}
              </a>
              <p className="text-sm text-gray-600 mt-3 line-clamp-5">{r.clean_text}</p>
              <p className="text-xs text-gray-400 mt-2">
                {new Date(r.timestamp).toLocaleString()}
              </p>
            </div>
          ))}
        </div>

        {results.length === 0 && !loading && (
          <p className="text-center text-gray-500 mt-20">No results yet. Try a search.</p>
        )}
      </main>
    </div>
  )
}

export default App
