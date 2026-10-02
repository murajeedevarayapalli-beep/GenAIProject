"use client";

import { FormEvent, useState } from "react";

const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [message, setMessage] = useState("My order ORD-1001 is delayed and I need an update.");
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);

    try {
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: "user-001", message }),
      });
      const payload = await res.json();
      setResponse(payload);
    } catch (error) {
      setResponse({ error: "Could not reach the backend API." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-cyan-400">Multi-agent AI</p>
            <h1 className="mt-2 text-4xl font-bold">Delivery Support Resolution Agent</h1>
          </div>
          <div className="rounded-full border border-cyan-500/40 bg-cyan-500/10 px-4 py-2 text-sm text-cyan-200">
            Backend ready
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">
            <h2 className="mb-4 text-xl font-semibold">Main chat</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <textarea
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                className="min-h-[120px] w-full rounded-xl border border-slate-700 bg-slate-950 p-3 text-slate-100 outline-none ring-0"
              />
              <button
                type="submit"
                disabled={loading}
                className="rounded-xl bg-cyan-500 px-5 py-3 font-medium text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? "Running workflow..." : "Run workflow"}
              </button>
            </form>

            <div className="mt-6 rounded-xl border border-slate-700 bg-slate-950 p-4">
              <h3 className="mb-2 font-semibold text-slate-200">Agent response</h3>
              {response ? (
                <div className="space-y-3 text-sm text-slate-300">
                  <p>{response.final_response || response.error || "No response yet."}</p>
                  {response.sources && response.sources.length > 0 && (
                    <ul className="list-disc space-y-1 pl-5">
                      {response.sources.map((source: any, index: number) => (
                        <li key={`${source.title || "doc"}-${index}`}>
                          {source.title || source.source} — {source.section || "section"}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ) : (
                <p className="text-slate-400">No response generated yet.</p>
              )}
            </div>
          </section>

          <aside className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <h3 className="mb-3 text-lg font-semibold">Workflow panel</h3>
              <ul className="space-y-3 text-sm text-slate-300">
                <li>• Triage</li>
                <li>• Retrieval</li>
                <li>• Investigation</li>
                <li>• Validation</li>
                <li>• Response</li>
              </ul>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <h3 className="mb-3 text-lg font-semibold">Human approval</h3>
              <p className="text-sm text-slate-300">Refunds over $100 and lost-package escalations require a human to approve before execution.</p>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <h3 className="mb-3 text-lg font-semibold">Sources</h3>
              <p className="text-sm text-slate-300">Delivery delay policy, refund policy, and claims guidance are retrieved from the local knowledge base.</p>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}
