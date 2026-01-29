export function getToken(): string | null {
    if(typeof window === "undefined") return null;

  return localStorage.getItem("access_token");
}

export type TokenPayload = {
  sub: string;
  role: string;
  exp?: number;
};

export function getTokenPayload(): TokenPayload | null {
  const token = getToken();
  if (!token) return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded =
      base64 + "=".repeat((4 - (base64.length % 4)) % 4);
    const payload = JSON.parse(atob(padded));
    return payload as TokenPayload;
  } catch {
    return null;
  }
}

export function getUserRole(): string | null {
  return getTokenPayload()?.role || null;
}

export function setToken(token: string){
localStorage.setItem("access_token", token);
}

export function getRefreshToken(): string | null {
    if(typeof window === "undefined") return null;

  return localStorage.getItem("refresh_token");
}

export function setRefreshToken(token: string){
localStorage.setItem("refresh_token", token);
}

export function clearToken(){
localStorage.removeItem("access_token");
localStorage.removeItem("refresh_token");

}
