"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Playfair_Display, Space_Grotesk } from "next/font/google";
import { login } from "@/src/lib/api";
import { getUserRole } from "@/src/lib/auth";

const display = Playfair_Display({
  subsets: ["latin"],
  weight: ["600", "700"],
});

const body = Space_Grotesk({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

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
    <main
      className={`${body.className} relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-50 via-white to-amber-50`}
    >
      <div className="pointer-events-none absolute left-10 top-10 h-64 w-64 rounded-full bg-amber-200/40 blur-3xl" />
      <div className="pointer-events-none absolute right-10 top-24 h-72 w-72 rounded-full bg-cyan-200/40 blur-3xl" />
      <div className="pointer-events-none absolute bottom-10 left-1/2 h-80 w-80 -translate-x-1/2 rounded-full bg-slate-200/60 blur-3xl" />

      <div className="relative mx-auto flex min-h-screen max-w-5xl items-center justify-center px-6 py-12">
        <div className="grid w-full max-w-3xl gap-8 lg:grid-cols-[1.1fr_1fr]">
          <div className="flex flex-col justify-center gap-4 rounded-3xl border border-slate-200 bg-white/70 p-8 shadow-xl backdrop-blur">
            <span className="inline-flex w-fit items-center rounded-full border border-slate-200 bg-white px-3 py-1 text-xs uppercase tracking-[0.2em] text-slate-500">
              Welcome Back
            </span>
            <h1 className={`${display.className} text-4xl text-slate-900`}>
              Log in to Ai Tutor
            </h1>
            <p className="text-sm leading-relaxed text-slate-600">
              Manage courses, review student insights, and keep the knowledge
              base curated with confidence.
            </p>
            <div className="mt-4 grid gap-3 text-sm text-slate-500">
              <div className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
                Trusted by academic teams
              </div>
              <div className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-amber-400" />
                Secure, role-based access
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-2xl">
            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label
                  className="block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500"
                  htmlFor="email"
                >
                  Email / Username
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  className="mt-3 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-200"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                />
              </div>

              <div>
                <label
                  className="block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500"
                  htmlFor="password"
                >
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  className="mt-3 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-200"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />
              </div>

              {error && (
                <p className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                  {error}
                </p>
              )}

              <button
                type="submit"
                className="group inline-flex w-full items-center justify-center rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold uppercase tracking-[0.2em] text-white transition hover:-translate-y-0.5 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={loading}
              >
                {loading ? "Signing in…" : "Sign in"}
              </button>

              <div className="text-xs text-slate-500">
                Need access? Contact your administrator for credentials.
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  );
}
