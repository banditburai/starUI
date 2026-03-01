import json
import time
from typing import Any, Literal

from starhtml import FT, Button, Div, Icon, Signal, js, set_timeout, signals

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
    base="group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-lg border p-4 pr-8 shadow-lg",
    config={
        "variants": {
            "variant": {
                "default": "border border-input bg-background text-foreground",
                "success": "border border-input text-foreground bg-gradient-to-br from-green-100 to-background dark:from-green-950 dark:to-background",
                "error": "border border-input text-foreground bg-gradient-to-br from-red-100 to-background dark:from-red-950 dark:to-background",
                "warning": "border border-input text-foreground bg-gradient-to-br from-yellow-100 to-background dark:from-yellow-950 dark:to-background",
                "info": "border border-input text-foreground bg-gradient-to-br from-blue-100 to-background dark:from-blue-950 dark:to-background",
                "destructive": "border border-destructive/40 text-foreground bg-gradient-to-br from-red-200 to-background dark:from-red-950 dark:to-background",
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
    toasts = Signal("toasts", [None] * max_visible)

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
            data_toast_position=position,
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
        has_toast = toasts[index]
        toast_order = toasts[index].order

        return Div(
            Div(
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
                ],
                cls="overflow-hidden min-h-0",
            ),
            cls="grid transition-[grid-template-rows,opacity] duration-300 ease-out motion-reduce:transition-none",
            style=f"grid-template-rows: 0fr; opacity: 0; order: 99; view-transition-name: toast-slot-{index}",
            data_style_grid_template_rows=has_toast.if_("1fr", "0fr"),
            data_style_opacity=has_toast.if_("1", "0"),
            data_style_order=has_toast.if_(toast_order, "99"),
            data_toast_slot=str(index),
        )

    return _


def _toast_element(index: int, variant: str) -> FT:
    def _(*, toasts, **_):
        toast_item = toasts[index]

        if variant == "default":
            show_condition = toast_item & (
                ~toast_item.variant | toast_item.variant.eq("default")
            )
        else:
            show_condition = toast_item & toast_item.variant.eq(variant)

        icon_name, icon_cls = {
            "default": ("lucide:bell", "text-foreground/70"),
            "success": ("lucide:check-circle", "text-green-600 dark:text-green-400"),
            "error": ("lucide:x-circle", "text-red-600 dark:text-red-400"),
            "warning": (
                "lucide:alert-triangle",
                "text-yellow-600 dark:text-yellow-400",
            ),
            "info": ("lucide:info", "text-blue-600 dark:text-blue-400"),
            "destructive": ("lucide:x-circle", "text-red-600 dark:text-red-400"),
        }.get(variant, ("lucide:bell", "text-foreground/70"))

        return Div(
            Div(
                Icon(icon_name, cls=cn("h-4 w-4", icon_cls)) if icon_name else None,
                Div(
                    Div(
                        data_text=toast_item.title,
                        cls="text-sm font-semibold",
                    ),
                    Div(
                        data_text=toast_item.description,
                        data_show=toast_item.description,
                        cls="text-sm text-muted-foreground",
                    ),
                    cls="grid gap-1",
                ),
                cls=cn("flex items-start", "space-x-2" if icon_name else ""),
            ),
            Button(
                Icon("lucide:x", cls="h-4 w-4"),
                data_on_click=js(
                    f"{toasts} = {toasts}.map((t,i) => i==={index} ? null : t)"
                ),
                type="button",
                aria_label="Dismiss toast",
                cls="absolute right-2 top-2 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none",
            ),
            data_toast_item="",
            data_show=show_condition,
            cls=toast_variants(variant=variant),
            role="status",
            aria_live="polite",
            aria_atomic="true",
        )

    return _


class ToastHelper:
    """Client-side toast API — returns JS expressions for data_on_click."""

    def __call__(
        self,
        title: str,
        description: str = "",
        variant: ToastVariant = "default",
        duration: int = 4000,
    ) -> str:
        data = json.dumps(
            {"title": title, "description": description, "variant": variant}
        )
        auto_dismiss = (
            set_timeout(js("$toasts=$toasts.map(x=>x&&x.id===t.id?null:x)"), duration)
            if duration
            else ""
        )
        core = (
            f"const t={{...{data},id:Date.now(),timestamp:Date.now(),order:0}};"
            f"const a=$toasts.map(s=>s?{{...s,order:s.order+1}}:s);"
            f"let i=a.findIndex(s=>!s);"
            f"if(i<0)i=a.reduce((o,s,j)=>s.timestamp<a[o].timestamp?j:o,0);"
            f"a[i]=t;$toasts=a;"
            f"{auto_dismiss}"
        )
        return (
            f"(()=>{{const fn=()=>{{{core}}};"
            f"document.startViewTransition?document.startViewTransition(fn):fn()}})()"
        )

    def success(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "success", duration)

    def error(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "error", duration)

    def warning(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "warning", duration)

    def info(self, title: str, description: str = "", duration: int = 4000) -> str:
        return self(title, description, "info", duration)

    def destructive(
        self, title: str, description: str = "", duration: int = 4000
    ) -> str:
        return self(title, description, "destructive", duration)


class ToastQueue:
    """Toast state manager for SSE routes."""

    def __init__(self, max_visible: int = 3):
        self.toasts: list[dict | None] = [None] * max_visible
        self.max_visible = max_visible

    def _make_toast(self, title: str, description: str, variant: ToastVariant) -> dict:
        return {
            "id": int(time.time() * 1000000),
            "title": title,
            "description": description,
            "variant": variant,
            "timestamp": int(time.time() * 1000),
            "order": 0,
        }

    def __call__(
        self, title: str, description: str = "", variant: ToastVariant = "default"
    ):
        return self.show(title, description, variant)

    def show(
        self, title: str, description: str = "", variant: ToastVariant = "default"
    ):
        new_toast = self._make_toast(title, description, variant)
        for i, t in enumerate(self.toasts):
            if t is not None:
                self.toasts[i] = {**t, "order": t["order"] + 1}
        idx = next((i for i, t in enumerate(self.toasts) if t is None), None)
        if idx is None:
            oldest_idx, oldest_ts = 0, float("inf")
            for i, t in enumerate(self.toasts):
                if t is not None and t["timestamp"] < oldest_ts:
                    oldest_ts = t["timestamp"]
                    oldest_idx = i
            idx = oldest_idx
        self.toasts[idx] = new_toast
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
        self.toasts = [None] * self.max_visible
        return signals(toasts=self.toasts)


toast = ToastHelper()


__all__ = [
    "Toaster",
    "toast",
    "ToastQueue",
    "ToastVariant",
    "ToastPosition",
]
