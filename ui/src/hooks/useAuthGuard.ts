"use client"
import { getToken } from "@/src/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";




export function useAuthGuard(){
    const router = useRouter();
    useEffect(() =>{
        const token = getToken();
        if(!token){
            router.push("/login");
        }
    }, [router])
}
