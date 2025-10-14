from typing import Any, Literal
import json
import time

from starhtml import FT, Button, Div, Icon, Span, Signal, js, signals, set_timeout
from starhtml.datastar import _JSRaw

from .utils import cn, cva

ToastVariant = Literal["default", "success", "error", "warning", "info", "destructive"]
ToastPosition = Literal[
    "top-left",
    "top-center",
    "top-right",
    "bottom-left",
    "bottom-center",
    "bottom-right",
]

toast_variants = cva(
    base="group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-md border p-6 pr-8 shadow-lg transition-all",
    config={
        "variants": {
            "variant": {
                "default": "border border-input bg-background text-foreground",
                "success": "border border-input text-foreground bg-gradient-to-br from-green-50 to-background dark:from-green-950 dark:to-background",
                "error": "border border-input text-foreground bg-gradient-to-br from-red-50 to-background dark:from-red-950 dark:to-background",
                "warning": "border border-input text-foreground bg-gradient-to-br from-yellow-50 to-background dark:from-yellow-950 dark:to-background",
                "info": "border border-input text-foreground bg-gradient-to-br from-blue-50 to-background dark:from-blue-950 dark:to-background",
                "destructive": "border-destructive bg-destructive text-destructive-foreground",
            }
        },
        "defaultVariants": {"variant": "default"},
    },
)

def Toaster(
    position: ToastPosition = "bottom-right",
    max_visible: int = 3,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    toasts = Signal("toasts", [])

    position_cls = {
        "top-left": "top-0 left-0",
        "top-center": "top-0 left-1/2 -translate-x-1/2",
        "top-right": "top-0 right-0",
        "bottom-left": "bottom-0 left-0",
        "bottom-center": "bottom-0 left-1/2 -translate-x-1/2",
        "bottom-right": "bottom-0 right-0",
    }[position]

    return Div(
        toasts,
        Div(
            *[_toast_slot(i)(toasts=toasts) for i in range(max_visible)],
            cls=cn(
                "fixed z-[100] flex flex-col-reverse gap-2 p-4 w-[calc(100%-2rem)] sm:w-[420px] pointer-events-none",
                position_cls,
                cls,
            ),
            **kwargs,
        ),
    )


def _toast_slot(index: int) -> FT:
    def _(*, toasts, **_):
        return Div(
            *[
                _toast_element(index, variant)(toasts=toasts)
                for variant in [
                    "default",
                    "success",
                    "error",
                    "warning",
                    "info",
                    "destructive",
                ]
            ]
        )
    return _


def _toast_element(index: int, variant: str) -> FT:
    def _(*, toasts, **_):
        toast_item = toasts[index]

        if variant == "default":
            show_condition = toast_item & (~toast_item.variant | toast_item.variant.eq("default"))
        else:
            show_condition = toast_item & toast_item.variant.eq(variant)

        icon_name, icon_cls = {
            "success": ("lucide:check-circle", "text-green-600 dark:text-green-400"),
            "error": ("lucide:x-circle", "text-red-600 dark:text-red-400"),
            "warning": ("lucide:alert-triangle", "text-yellow-600 dark:text-yellow-400"),
            "info": ("lucide:info", "text-blue-600 dark:text-blue-400"),
            "destructive": ("lucide:x-circle", ""),
        }.get(variant, (None, None))

        return Div(
            Div(
                Span(Icon(icon_name, cls=cn("h-4 w-4", icon_cls)), cls="shrink-0") if icon_name else None,
                Div(
                    Div(
                        data_text=toast_item.title,
                        cls="text-sm font-semibold",
                    ),
                    Div(
                        data_text=toast_item.description,
                        data_show=toast_item.description,
                        style="display: none",
                        cls="text-sm opacity-90",
                    ),
                    cls="grid gap-1",
                ),
                cls=cn("flex items-start", "space-x-3" if icon_name else ""),
            ),
            Button(
                Icon("lucide:x", cls="h-4 w-4"),
                data_on_click=js(f"{toasts} = {toasts}.filter(t => t.id !== {toast_item.id})"),
                type="button",
                cls="absolute right-2 top-2 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none",
            ),
            data_show=show_condition,
            cls=toast_variants(variant=variant),
            style="display: none",
            role="status",
            aria_live="polite",
            aria_atomic="true",
        )
    return _


class ToastHelper:
    """shadcn/Sonner-style toast API for client-side usage."""

    def __call__(
        self,
        title: str,
        description: str = "",
        variant: ToastVariant = "default",
        duration: int = 4000,
    ) -> str:
        data = json.dumps({"title": title, "description": description, "variant": variant})
        auto_dismiss = set_timeout(js("$toasts=$toasts.filter(x=>x.id!==t.id)"), duration) if duration else ''
        return f"""(()=>{{const t={{...{data},id:Date.now(),timestamp:Date.now()}};$toasts=[t,...$toasts].slice(0,3);{auto_dismiss}}})()"""

    def success(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "success", duration)

    def error(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "error", duration)

    def warning(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "warning", duration)

    def info(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "info", duration)

    def destructive(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "destructive", duration)


class ToastQueue:
    """Toast state manager for SSE routes."""

    def __init__(self, max_visible: int = 3):
        self.toasts = []
        self.max_visible = max_visible

    def _make_toast(self, title: str, description: str, variant: ToastVariant) -> dict:
        return {
            "id": int(time.time() * 1000000),  # Microseconds for uniqueness
            "title": title,
            "description": description,
            "variant": variant,
            "timestamp": int(time.time() * 1000)
        }

    def __call__(self, title: str, description: str = "", variant: ToastVariant = "default"):
        return self.show(title, description, variant)

    def show(self, title: str, description: str = "", variant: ToastVariant = "default"):
        new_toast = self._make_toast(title, description, variant)
        self.toasts = [new_toast] + self.toasts[:self.max_visible - 1]
        return signals(toasts=self.toasts)

    def success(self, title: str, description: str = ""):
        return self.show(title, description, "success")

    def error(self, title: str, description: str = ""):
        return self.show(title, description, "error")

    def warning(self, title: str, description: str = ""):
        return self.show(title, description, "warning")

    def info(self, title: str, description: str = ""):
        return self.show(title, description, "info")

    def destructive(self, title: str, description: str = ""):
        return self.show(title, description, "destructive")

    def clear(self):
        self.toasts = []
        return signals(toasts=[])


toast = ToastHelper()


__all__ = [
    "Toaster",
    "toast",
    "ToastQueue",
    "ToastVariant",
    "ToastPosition",
]
