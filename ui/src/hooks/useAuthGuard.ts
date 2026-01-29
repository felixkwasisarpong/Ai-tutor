"use client"
import { getToken, getUserRole } from "@/src/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function useAuthGuard(requiredRole?: "admin" | "student"){
    const router = useRouter();
    useEffect(() =>{
        const token = getToken();
        if(!token){
            router.push("/login");
            return;
        }
        if (requiredRole) {
            const role = getUserRole();
            if (role !== requiredRole) {
                router.push("/login");
            }
        }
    }, [router, requiredRole])
}
