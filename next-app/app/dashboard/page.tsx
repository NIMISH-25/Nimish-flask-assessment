"use client";

import { useEffect, useState } from "react";
import type { FileItem } from "@/lib/types";

export default function DashboardPage() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        const res = await fetch("/api/files", { cache: "no-store" });
        if (!res.ok) throw new Error(`Request failed: ${res.status}`);
        const data: FileItem[] = await res.json();
        if (!cancelled) setFiles(data);
      } catch (e) {
        const msg = e instanceof Error ? e.message : "Unknown error";
        if (!cancelled) setError(msg);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main style={{ padding: 24, fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 12 }}>Dashboard</h1>

      {loading && <p>Loading files...</p>}

      {!loading && error && <p style={{ color: "crimson" }}>Failed to load files: {error}</p>}

      {!loading && !error && (
        <div style={{ border: "1px solid #ddd", borderRadius: 8, overflow: "hidden" }}>
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr", padding: 12, fontWeight: 600, background: "#4558ff" }}>
            <div>Name</div>
            <div>Size</div>
            <div>Date</div>
            <div>Owner</div>
          </div>

          {files.length === 0 ? (
            <div style={{ padding: 12 }}>No files found.</div>
          ) : (
            files.map((f) => (
              <div key={f.id} style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr", padding: 12, borderTop: "1px solid #eee" }}>
                <div>{f.name}</div>
                <div>{f.size}</div>
                <div>{f.date}</div>
                <div>{f.user_name}</div>
              </div>
            ))
          )}
        </div>
      )}
    </main>
  );
}
