import { useEffect } from "react";

export default function Agent() {
    useEffect(() => {
        window.location.href = "/sessions";
    }, []);
}