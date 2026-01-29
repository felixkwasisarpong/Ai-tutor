export function getToken(): string | null {
    if(typeof window === "undefined") return null;

  return localStorage.getItem("access_token");
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
