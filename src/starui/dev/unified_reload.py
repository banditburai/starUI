"""Unified development reload system that consolidates CSS and Python file watching."""

import json
from pathlib import Path

from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket


class DevReloadHandler(WebSocketEndpoint):
    """Unified WebSocket handler for development reload notifications."""

    clients: set[WebSocket] = set()

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.clients.add(websocket)
        await self._send_message(websocket, {"type": "connected", "message": "StarUI dev reload connected"})

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        self.clients.discard(websocket)

    @classmethod
    async def notify_css_update(cls, css_path: Path, build_time: float = 0) -> None:
        """Notify all clients of CSS updates."""
        await cls._broadcast_message(
            {
                "type": "css-update",
                "path": str(css_path.name),
                "buildTime": build_time,
            }
        )

    @classmethod
    async def _broadcast_message(cls, message: dict) -> None:
        """Broadcast message to all connected clients."""
        if not cls.clients:
            return

        disconnected = set()
        message_str = json.dumps(message)

        for client in cls.clients:
            try:
                await client.send_text(message_str)
            except Exception:
                disconnected.add(client)

        cls.clients -= disconnected

    @staticmethod
    async def _send_message(websocket: WebSocket, message: dict) -> None:
        """Send message to specific client."""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception:
            pass


def create_dev_reload_route() -> WebSocketRoute:
    """Create the unified dev reload WebSocket route."""
    return WebSocketRoute("/live-reload", endpoint=DevReloadHandler)


def DevReloadJs():
    """Generate unified development reload JavaScript."""
    from starhtml.xtend import Script

    js_code = """(() => {
    if (!['localhost', '127.0.0.1'].includes(location.hostname)) return;

    let attempts = 0;
    const maxAttempts = 20;
    const reconnectInterval = 1000;

    const connect = () => {
        const ws = new WebSocket(`ws://${window.location.host}/live-reload`);

        ws.onopen = async () => {
            if (attempts > 0) {
                try {
                    const res = await fetch(window.location.href);
                    if (res.ok) {
                        console.log('[DEV] Server reconnected, reloading page');
                        window.location.reload();
                        return;
                    }
                } catch (e) {}
            }
            console.log('[DEV] Development reload connected');
            attempts = 0;
        };

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);

            switch (message.type) {
                case 'css-update':
                    const links = document.querySelectorAll('link[href*="starui.css"], link[href*="tailwind"]');
                    links.forEach(link => {
                        const newLink = link.cloneNode();
                        const url = new URL(link.href);
                        url.searchParams.set('t', Date.now());
                        newLink.href = url.toString();
                        newLink.onload = () => link.remove();
                        link.after(newLink);
                    });
                    console.log(`[CSS] Updated ${message.path} in ${(message.buildTime || 0).toFixed(2)}s`);
                    break;

                case 'build-error':
                    console.error('[BUILD ERROR]', message.error);
                    break;

                case 'connected':
                    break;

                default:
                    console.log('[DEV]', message);
            }
        };

        ws.onclose = () => {
            if (attempts < maxAttempts) {
                attempts++;
                console.log(`[DEV] Connection lost, reconnecting... (${attempts}/${maxAttempts})`);
                setTimeout(connect, reconnectInterval);
            } else {
                console.log('[DEV] Max reconnection attempts reached, reloading page');
                window.location.reload();
            }
        };

        ws.onerror = () => {
            console.log('[DEV] WebSocket error');
        };
    };

    connect();
})();"""

    return Script(js_code)
