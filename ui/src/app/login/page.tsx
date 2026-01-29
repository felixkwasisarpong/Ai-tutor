"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/src/lib/api";
import { getUserRole } from "@/src/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await login(email, password);
      const role = getUserRole();
      if (role === "admin") {
        router.push("/admin");
      } else {
        router.push("/student");
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Login failed. Try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-md mx-auto py-12">
      <h1 className="text-3xl font-bold mb-6">Log in</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="email">
            Email / Username
          </label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            className="w-full border rounded-md px-3 py-2"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            className="w-full border rounded-md px-3 py-2"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>

        {error && <p className="text-red-600 text-sm">{error}</p>}

        <button
          type="submit"
          className="w-full bg-black text-white py-2 rounded-md"
          disabled={loading}
        >
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </main>
  );
}
