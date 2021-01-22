import React, { useRef, useState, useEffect } from 'react';

export const WebsocketStatus = {
    CONNECTING: "CONNECTING",
    CONNECTED: "CONNECTED",
    RECONNECTING: "RECONNECTING",
    ERROR: "ERROR",
    DISCONNECTING: "DISCONNECTING",
    DISCONNECTED: "DISCONNECTED",
}

const RETRY_TIMEOUT = 1000;
const ADDRESS = "127.0.0.1";
const PORT = 6789;

export default function useWebsocket() {
    const [status, setStatus] = useState(WebsocketStatus.DISCONNECTED);
    const ws_ref = useRef(null);

    const [retryFlag, setRetryFlag] = useState({ go: true });
    const [disconnectingFlag, setDisconnectingFlag] = useState(false)

    useEffect(() => {
        if (disconnectingFlag) {
            return
        }

        const ws = new WebSocket(`ws://${ADDRESS}:${PORT}`);
        ws_ref.current = ws;
        setStatus(WebsocketStatus.CONNECTING);

        ws.addEventListener("open", () => {
            setStatus(WebsocketStatus.CONNECTED);
        })

        const toggleRetryFlag = () => {
            const code = setTimeout(() => setRetryFlag({ go: true }), RETRY_TIMEOUT)
            setRetryFlag({ code, go: false })
        }

        ws.addEventListener("error", toggleRetryFlag)
        ws.addEventListener("close", toggleRetryFlag)

        return (() => {
            setStatus(WebsocketStatus.DISCONNECTING);
            setDisconnectingFlag(true);

            ws.removeEventListener("close", toggleRetryFlag);
            ws.removeEventListener("error", toggleRetryFlag);

            ws.addEventListener("close", () => {
                setStatus(WebsocketStatus.DISCONNECTED);
                setDisconnectingFlag(false);
            });
            ws.addEventListener("error", () => setStatus(WebsocketStatus.ERROR));

            retryFlag.code && clearTimeout(retryFlag.code);

            ws.close();
        })

    }, [retryFlag, disconnectingFlag])

    return [ws_ref.current, status]
}