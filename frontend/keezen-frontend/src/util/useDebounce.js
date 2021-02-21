import { useRef } from "react";

export function useDebounce(callback, timeout) {
    const timeoutCode = useRef(null);

    function setTimeout(...args) {
        if (timeoutCode.current !== null) {
            window.clearTimeout(timeoutCode.current);
        }

        timeoutCode.current = window.setTimeout(() => {
            timeoutCode.current = null;
            callback(...args);
        }, timeout);
    }
    return setTimeout
}