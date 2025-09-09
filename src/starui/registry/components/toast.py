from typing import Any, Literal

from starhtml import FT, Button, Div, Icon, Span
from starhtml.datastar import ds_on_click, ds_show, ds_signals, ds_text, value

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

position_map = {
    "top-left": "top-0 left-0",
    "top-center": "top-0 left-1/2 -translate-x-1/2",
    "top-right": "top-0 right-0",
    "bottom-left": "bottom-0 left-0",
    "bottom-center": "bottom-0 left-1/2 -translate-x-1/2",
    "bottom-right": "bottom-0 right-0",
}

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

variant_icons = {
    "success": ("lucide:check-circle", "text-green-600 dark:text-green-400"),
    "error": ("lucide:x-circle", "text-red-600 dark:text-red-400"),
    "warning": ("lucide:alert-triangle", "text-yellow-600 dark:text-yellow-400"),
    "info": ("lucide:info", "text-blue-600 dark:text-blue-400"),
    "destructive": ("lucide:x-circle", ""),
}


def Toaster(
    position: ToastPosition = "bottom-right",
    signal: str = "toasts",
    max_visible: int = 3,
    class_name: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        ds_signals(
            **{
                signal: value([]),
                f"{signal}_counter": value(0),
            }
        ),
        Div(
            *[_toast_slot(signal, i) for i in range(max_visible)],
            cls=cn(
                "fixed z-[100] flex flex-col-reverse gap-2 p-4 max-w-[420px] pointer-events-none",
                position_map.get(position, "bottom-right"),
                class_name,
            ),
            **kwargs,
        ),
    )


def _toast_slot(signal: str, index: int) -> FT:
    return Div(
        *[
            _toast_element(signal, index, variant)
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


def _toast_element(signal: str, index: int, variant: str) -> FT:
    show_condition = (
        f"${signal}[{index}] && (!${signal}[{index}].variant || ${signal}[{index}].variant === 'default')"
        if variant == "default"
        else f"${signal}[{index}] && ${signal}[{index}].variant === '{variant}'"
    )

    icon_name, icon_cls = variant_icons.get(variant, (None, None))

    return Div(
        Div(
            Span(Icon(icon_name, cls=f"h-4 w-4 {icon_cls}"), cls="shrink-0")
            if icon_name
            else None,
            Div(
                Div(
                    ds_text(f"${signal}[{index}] ? ${signal}[{index}].title : ''"),
                    cls="text-sm font-semibold",
                ),
                Div(
                    ds_text(
                        f"${signal}[{index}] && ${signal}[{index}].description ? ${signal}[{index}].description : ''"
                    ),
                    ds_show(f"${signal}[{index}] && ${signal}[{index}].description"),
                    cls="text-sm opacity-90",
                ),
                cls="grid gap-1",
            ),
            cls="flex items-start space-x-3" if icon_name else "flex items-start",
        ),
        Button(
            Icon("lucide:x", cls="h-4 w-4"),
            ds_on_click(f"""
                const toastId = ${signal}[{index}].id;
                ${signal} = ${signal}.filter(t => t.id !== toastId);
            """),
            type="button",
            cls="absolute right-2 top-2 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none",
        ),
        ds_show(show_condition),
        cls=toast_variants(variant=variant),
        style="display: none;",  # Initial state to prevent flash
        role="status",
        aria_live="polite",
        aria_atomic="true",
    )


def toast(
    message: str,
    description: str = "",
    variant: ToastVariant = "default",
    duration: int = 4000,
    signal: str = "toasts",
    max_visible: int = 3,
) -> str:
    """Generate Datastar action to trigger a toast notification."""
    message = message.replace("'", "\\'")
    description = description.replace("'", "\\'")

    return f"""
        const newToast = {{
            id: ++${signal}_counter,
            title: '{message}',
            description: '{description}',
            variant: '{variant}',
            timestamp: Date.now()
        }};

        ${signal} = [newToast, ...${signal}];

        if (${signal}.length > {max_visible}) {{
            ${signal} = ${signal}.slice(0, {max_visible});
        }}

        if ({duration} > 0) {{
            setTimeout(() => {{
                ${signal} = ${signal}.filter(t => t.id !== newToast.id);
            }}, {duration});
        }}
    """


def success_toast(
    message: str, description: str = "", duration: int = 4000, signal: str = "toasts"
) -> str:
    """Generate a success toast notification."""
    return toast(
        message, description, variant="success", duration=duration, signal=signal
    )


def error_toast(
    message: str, description: str = "", duration: int = 4000, signal: str = "toasts"
) -> str:
    """Generate an error toast notification."""
    return toast(
        message, description, variant="error", duration=duration, signal=signal
    )


def warning_toast(
    message: str, description: str = "", duration: int = 4000, signal: str = "toasts"
) -> str:
    """Generate a warning toast notification."""
    return toast(
        message, description, variant="warning", duration=duration, signal=signal
    )


def info_toast(
    message: str, description: str = "", duration: int = 4000, signal: str = "toasts"
) -> str:
    """Generate an info toast notification."""
    return toast(message, description, variant="info", duration=duration, signal=signal)
