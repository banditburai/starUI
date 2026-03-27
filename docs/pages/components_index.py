from starhtml import Div, P, A, Icon, Span, FT, Code, Style
from component_registry import ComponentRegistry
from layouts.base import DocsLayout, LayoutConfig, SidebarConfig


# ── Component icon mapping ──────────────────────────────────────────

COMPONENT_ICONS = {
    "accordion": "lucide:chevrons-down-up",
    "alert": "lucide:alert-circle",
    "alert_dialog": "lucide:alert-triangle",
    "avatar": "lucide:circle-user",
    "badge": "lucide:tag",
    "breadcrumb": "lucide:navigation",
    "button": "lucide:mouse-pointer-click",
    "calendar": "lucide:calendar",
    "card": "lucide:credit-card",
    "checkbox": "lucide:square-check",
    "code_block": "lucide:code-2",
    "command": "lucide:terminal",
    "date_picker": "lucide:calendar-days",
    "dialog": "lucide:app-window",
    "dropdown_menu": "lucide:menu",
    "menubar": "lucide:menu",
    "hover_card": "lucide:mouse-pointer",
    "input": "lucide:type",
    "label": "lucide:text",
    "navigation_menu": "lucide:compass",
    "pagination": "lucide:chevrons-left-right",
    "popover": "lucide:message-square",
    "progress": "lucide:loader",
    "radio_group": "lucide:circle-dot",
    "select": "lucide:chevron-down",
    "separator": "lucide:minus",
    "sheet": "lucide:panel-right",
    "skeleton": "lucide:loader-2",
    "switch": "lucide:toggle-left",
    "table": "lucide:table",
    "tabs": "lucide:layout-list",
    "textarea": "lucide:align-left",
    "theme_toggle": "lucide:sun-moon",
    "toast": "lucide:bell",
    "toggle": "lucide:toggle-right",
    "toggle_group": "lucide:group",
    "tooltip": "lucide:message-circle",
    "typography": "lucide:heading",
    "aspect_ratio": "lucide:proportions",
    "collapsible": "lucide:chevrons-up-down",
    "drawer": "lucide:panel-bottom",
    "field": "lucide:text-cursor-input",
    "input_otp": "lucide:rectangle-ellipsis",
    "scroll_area": "lucide:scroll-text",
    "slider": "lucide:sliders-horizontal",
}


# ── Miniature skeleton previews ─────────────────────────────────────


def _preview_button() -> FT:
    return Div(
        Div("Primary", cls="flex h-7 items-center rounded-md bg-primary px-3 text-[10px] font-medium text-primary-foreground"),
        Div("Outline", cls="flex h-7 items-center rounded-md border border-border px-3 text-[10px] font-medium text-muted-foreground"),
        cls="flex items-center gap-2",
    )


def _preview_input() -> FT:
    return Div(
        Span("Email", cls="mb-1 block text-[10px] font-medium text-foreground"),
        Div(
            Span("you@example.com", cls="text-[10px] text-muted-foreground"),
            cls="flex h-7 w-44 items-center rounded-md border border-border bg-background px-2",
        ),
    )


def _preview_field() -> FT:
    return Div(
        Span("Email", cls="mb-0.5 block text-[10px] font-medium text-foreground"),
        Div(
            Span("you@example.com", cls="text-[10px] text-muted-foreground"),
            cls="flex h-7 w-44 items-center rounded-md border border-border bg-background px-2",
        ),
        Span("We'll never share your email.", cls="mt-0.5 block text-[9px] text-muted-foreground"),
    )


def _preview_card() -> FT:
    return Div(
        Div(cls="mb-1 h-2 w-20 rounded bg-foreground/80"),
        Div(cls="mb-2.5 h-1.5 w-28 rounded bg-muted-foreground/40"),
        Div(cls="mb-0.5 h-1.5 w-full rounded bg-muted-foreground/20"),
        Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/20"),
        cls="w-44 rounded-lg border border-border bg-background p-3",
    )


def _preview_switch() -> FT:
    return Div(
        Div(
            Span("Notifications", cls="text-[10px] text-foreground"),
            Div(
                Div(cls="absolute top-[2px] right-0.5 h-3 w-3 rounded-full bg-white shadow-sm"),
                cls="relative h-4 w-7 shrink-0 rounded-full bg-primary",
            ),
            cls="flex items-center gap-3",
        ),
        Div(
            Span("Dark mode", cls="text-[10px] text-muted-foreground"),
            Div(
                Div(cls="absolute top-[2px] left-0.5 h-3 w-3 rounded-full bg-foreground/40"),
                cls="relative h-4 w-7 shrink-0 rounded-full bg-foreground/15",
            ),
            cls="flex items-center gap-3",
        ),
        cls="space-y-2",
    )


def _preview_tabs() -> FT:
    return Div(
        Div(
            Span("Account", cls="rounded bg-background px-2 py-1 text-[10px] font-medium text-foreground"),
            Span("Password", cls="px-2 py-1 text-[10px] text-muted-foreground"),
            cls="mb-2 flex w-fit gap-0.5 rounded-md bg-foreground/[0.06] p-0.5",
        ),
        Div(cls="mb-1.5 h-1.5 w-28 rounded bg-muted-foreground/20"),
        Div(cls="h-6 w-full rounded-md border border-border"),
    )


def _preview_dialog() -> FT:
    return Div(
        Div(cls="mb-1 h-2 w-24 rounded bg-foreground/80"),
        Div(cls="mb-0.5 h-1.5 w-full rounded bg-muted-foreground/30"),
        Div(cls="mb-2.5 h-1.5 w-3/4 rounded bg-muted-foreground/30"),
        Div(
            Div("Cancel", cls="flex h-6 items-center rounded-md border border-border px-2 text-[9px] text-muted-foreground"),
            Div("Continue", cls="flex h-6 items-center rounded-md bg-primary px-2 text-[9px] text-primary-foreground"),
            cls="flex justify-end gap-1.5",
        ),
        cls="w-44 rounded-lg border border-border bg-background p-3 shadow-lg",
    )


def _preview_badge() -> FT:
    return Div(
        Span("Badge", cls="rounded-full bg-primary px-2 py-0.5 text-[9px] font-medium text-primary-foreground"),
        Span("Secondary", cls="rounded-full bg-muted px-2 py-0.5 text-[9px] font-medium text-muted-foreground"),
        Span("Outline", cls="rounded-full border border-border px-2 py-0.5 text-[9px] font-medium text-foreground"),
        cls="flex flex-wrap items-center gap-1.5",
    )


def _preview_accordion() -> FT:
    return Div(
        Div(
            Span("Is it accessible?", cls="text-[10px] font-medium text-foreground"),
            Icon("lucide:chevron-down", width="10", height="10", cls="text-muted-foreground"),
            cls="flex items-center justify-between border-b border-border py-1.5",
        ),
        Div(
            Span("How does it work?", cls="text-[10px] font-medium text-foreground"),
            Icon("lucide:chevron-down", width="10", height="10", cls="text-muted-foreground"),
            cls="flex items-center justify-between border-b border-border py-1.5",
        ),
        Div(
            Span("Can I customize it?", cls="text-[10px] font-medium text-foreground"),
            Icon("lucide:chevron-down", width="10", height="10", cls="text-muted-foreground"),
            cls="flex items-center justify-between py-1.5",
        ),
        cls="w-44",
    )


def _preview_command() -> FT:
    return Div(
        Div(
            Icon("lucide:search", width="10", height="10", cls="text-muted-foreground"),
            Span("Search...", cls="text-[10px] text-muted-foreground"),
            cls="flex items-center gap-1.5 border-b border-border px-2 py-1.5",
        ),
        Div(
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-18 rounded bg-muted-foreground/20"),
            cls="space-y-1.5 p-1.5",
        ),
        cls="w-36 overflow-hidden rounded-lg border border-border bg-background shadow-lg",
    )


def _preview_select() -> FT:
    return Div(
        Span("Theme", cls="mb-1 block text-[10px] font-medium text-foreground"),
        Div(
            Span("Select...", cls="text-[10px] text-muted-foreground"),
            Icon("lucide:chevron-down", width="10", height="10", cls="text-muted-foreground"),
            cls="flex h-7 w-36 items-center justify-between rounded-md border border-border bg-background px-2",
        ),
    )


def _preview_checkbox() -> FT:
    return Div(
        Div(
            Div(
                Icon("lucide:check", width="8", height="8", cls="text-primary-foreground"),
                cls="flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-sm border border-primary bg-primary",
            ),
            Span("Accept terms", cls="text-[10px] text-foreground"),
            cls="flex items-center gap-1.5",
        ),
        Div(
            Div(cls="h-3.5 w-3.5 shrink-0 rounded-sm border border-border"),
            Span("Subscribe", cls="text-[10px] text-muted-foreground"),
            cls="flex items-center gap-1.5",
        ),
        cls="space-y-2",
    )


def _preview_alert() -> FT:
    return Div(
        Div(
            Icon("lucide:alert-circle", width="12", height="12", cls="mt-0.5 shrink-0 text-foreground"),
            Div(
                Div(cls="mb-0.5 h-2 w-14 rounded bg-foreground/80"),
                Div(cls="h-1.5 w-32 rounded bg-muted-foreground/30"),
            ),
            cls="flex gap-2",
        ),
        cls="w-44 rounded-lg border border-border bg-background p-2.5",
    )


def _preview_alert_dialog() -> FT:
    return _preview_dialog()


def _preview_progress() -> FT:
    return Div(
        Div(
            Div(cls="h-full w-2/3 rounded-full bg-primary"),
            cls="h-2 w-40 overflow-hidden rounded-full bg-foreground/10",
        ),
    )


def _preview_table() -> FT:
    return Div(
        Div(
            Div(cls="h-1.5 w-10 rounded bg-muted-foreground/40"),
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/40"),
            Div(cls="h-1.5 w-8 rounded bg-muted-foreground/40"),
            cls="flex gap-3 border-b border-border px-2 py-1.5",
        ),
        Div(
            Div(cls="h-1.5 w-10 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-8 rounded bg-muted-foreground/20"),
            cls="flex gap-3 border-b border-border px-2 py-1.5",
        ),
        Div(
            Div(cls="h-1.5 w-10 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-8 rounded bg-muted-foreground/20"),
            cls="flex gap-3 px-2 py-1.5",
        ),
        cls="w-40 overflow-hidden rounded-lg border border-border",
    )


def _preview_avatar() -> FT:
    return Div(
        Div(Span("JD", cls="text-[9px] font-medium text-primary-foreground"), cls="flex h-8 w-8 items-center justify-center rounded-full bg-primary"),
        Div(Span("AB", cls="text-[9px] font-medium text-primary-foreground"), cls="flex h-8 w-8 items-center justify-center rounded-full bg-primary/70"),
        Div(Span("KL", cls="text-[9px] font-medium text-primary-foreground"), cls="flex h-8 w-8 items-center justify-center rounded-full bg-primary/50"),
        cls="flex -space-x-2",
    )


def _preview_skeleton() -> FT:
    return Div(
        Div(cls="h-8 w-8 animate-pulse rounded-full bg-foreground/10"),
        Div(
            Div(cls="h-2 w-28 animate-pulse rounded bg-foreground/10"),
            Div(cls="h-1.5 w-20 animate-pulse rounded bg-foreground/10"),
            cls="space-y-1.5",
        ),
        cls="flex items-center gap-2.5",
    )


def _preview_separator() -> FT:
    return Div(
        Div(cls="h-1.5 w-full rounded bg-muted-foreground/20"),
        Div(cls="my-1.5 h-px w-full bg-border"),
        Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/20"),
        cls="w-36",
    )


def _preview_radio_group() -> FT:
    return Div(
        Div(
            Div(
                Div(cls="h-1.5 w-1.5 rounded-full bg-primary"),
                cls="flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-full border-2 border-primary",
            ),
            Span("Default", cls="text-[10px] text-foreground"),
            cls="flex items-center gap-1.5",
        ),
        Div(
            Div(cls="h-3.5 w-3.5 shrink-0 rounded-full border border-border"),
            Span("Comfortable", cls="text-[10px] text-muted-foreground"),
            cls="flex items-center gap-1.5",
        ),
        cls="space-y-2",
    )


def _preview_textarea() -> FT:
    return Div(
        Span("Message", cls="mb-1 block text-[10px] font-medium text-foreground"),
        Div(
            Span("Type your message...", cls="text-[10px] text-muted-foreground"),
            cls="h-12 w-40 rounded-md border border-border bg-background p-2",
        ),
    )


def _preview_sheet() -> FT:
    return Div(
        Div(cls="flex-1 rounded bg-foreground/[0.04]"),
        Div(
            Div(cls="mb-1.5 h-2 w-10 rounded bg-foreground/80"),
            Div(cls="mb-0.5 h-1.5 w-full rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/20"),
            cls="w-14 border-l border-border p-1.5",
        ),
        cls="flex h-14 w-40 gap-0 overflow-hidden rounded-lg border border-border bg-background",
    )


def _preview_tooltip() -> FT:
    return Div(
        Span("Hover me", cls="text-[10px] text-foreground underline decoration-dashed underline-offset-2"),
        Div(
            Span("Tooltip content", cls="text-[9px] text-primary-foreground"),
            cls="mt-1 rounded bg-primary px-1.5 py-0.5",
        ),
    )


def _preview_hover_card() -> FT:
    return Div(
        Span("@user", cls="text-[10px] font-medium text-primary underline underline-offset-2"),
        Div(
            Div(cls="mb-1 h-5 w-5 rounded-full bg-foreground/10"),
            Div(cls="mb-0.5 h-1.5 w-16 rounded bg-muted-foreground/30"),
            Div(cls="h-1.5 w-12 rounded bg-muted-foreground/20"),
            cls="mt-1 w-24 rounded-lg border border-border bg-background p-2 shadow-lg",
        ),
    )


def _preview_dropdown_menu() -> FT:
    return Div(
        Div(
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-18 rounded bg-muted-foreground/20"),
            Div(cls="my-0.5 h-px w-full bg-border"),
            Div(cls="h-1.5 w-12 rounded bg-muted-foreground/20"),
            cls="w-28 space-y-1 rounded-lg border border-border bg-background p-1.5 shadow-lg",
        ),
    )


def _preview_menubar() -> FT:
    return Div(
        Div(
            Div("File", cls="rounded px-1.5 py-0.5 text-[9px] text-foreground"),
            Div("Edit", cls="rounded px-1.5 py-0.5 text-[9px] text-foreground"),
            Div("View", cls="rounded px-1.5 py-0.5 text-[9px] text-foreground"),
            Div("Help", cls="rounded px-1.5 py-0.5 text-[9px] text-foreground"),
            cls="flex gap-0.5 rounded-md border border-border bg-background px-1 py-1",
        ),
    )


def _preview_navigation_menu() -> FT:
    return Div(
        Div(
            Span("Getting Started", cls="px-2 py-1 text-[9px] font-medium text-foreground"),
            Span("Components", cls="px-2 py-1 text-[9px] font-medium text-foreground"),
            Span("Docs", cls="px-2 py-1 text-[9px] font-medium text-muted-foreground"),
            cls="flex gap-0.5 rounded-md border border-border bg-background px-1 py-1",
        ),
        Div(
            Div(cls="mb-1 h-1.5 w-20 rounded bg-muted-foreground/30"),
            Div(cls="h-1.5 w-24 rounded bg-muted-foreground/20"),
            cls="mt-1 w-40 rounded-lg border border-border bg-popover p-2 shadow-lg",
        ),
    )


def _preview_pagination() -> FT:
    return Div(
        Div(
            Icon("lucide:chevron-left", width="8", height="8", cls="text-muted-foreground"),
            Div("1", cls="flex h-6 w-6 items-center justify-center rounded-md bg-primary text-[9px] font-medium text-primary-foreground"),
            Div("2", cls="flex h-6 w-6 items-center justify-center rounded-md text-[9px] font-medium text-muted-foreground"),
            Div("3", cls="flex h-6 w-6 items-center justify-center rounded-md text-[9px] font-medium text-muted-foreground"),
            Icon("lucide:ellipsis", width="8", height="8", cls="text-muted-foreground"),
            Icon("lucide:chevron-right", width="8", height="8", cls="text-muted-foreground"),
            cls="flex items-center gap-1",
        ),
    )


def _preview_toast() -> FT:
    return Div(
        Div(
            Div(
                Div(cls="mb-0.5 h-2 w-20 rounded bg-foreground/80"),
                Div(cls="h-1.5 w-28 rounded bg-muted-foreground/30"),
                cls="flex-1",
            ),
            Div("×", cls="shrink-0 text-[10px] text-muted-foreground"),
            cls="flex items-start gap-2",
        ),
        cls="w-44 rounded-lg border border-border bg-background p-2.5 shadow-lg",
    )


def _preview_popover() -> FT:
    return Div(
        Div("Open", cls="flex h-6 items-center rounded-md bg-primary px-2 text-[9px] font-medium text-primary-foreground"),
        Div(
            Div(cls="mb-1 h-1.5 w-16 rounded bg-muted-foreground/30"),
            Div(cls="h-5 w-full rounded-md border border-border"),
            cls="mt-1 w-28 rounded-lg border border-border bg-background p-2 shadow-lg",
        ),
    )


def _preview_date_picker() -> FT:
    return Div(
        Div(
            Icon("lucide:calendar", width="10", height="10", cls="text-muted-foreground"),
            Span("Pick a date", cls="text-[10px] text-muted-foreground"),
            cls="flex h-7 w-36 items-center gap-1.5 rounded-md border border-border bg-background px-2",
        ),
    )


def _preview_calendar() -> FT:
    return Div(
        Div(
            Icon("lucide:chevron-left", width="8", height="8", cls="text-muted-foreground"),
            Span("Feb 2026", cls="text-[8px] font-medium text-foreground"),
            Icon("lucide:chevron-right", width="8", height="8", cls="text-muted-foreground"),
            cls="mb-1.5 flex items-center justify-between px-0.5",
        ),
        Div(
            *[Div(d, cls="flex h-4 w-4 items-center justify-center text-[7px] text-muted-foreground") for d in ["S", "M", "T", "W", "T", "F", "S"]],
            *[Div(
                str(n),
                cls=f"w-4 h-4 text-[7px] flex items-center justify-center {'rounded bg-primary text-primary-foreground' if n == 23 else 'text-foreground'}"
            ) for n in range(1, 15)],
            cls="grid grid-cols-7 gap-px",
        ),
        cls="w-32 rounded-lg border border-border bg-background p-1.5",
    )


def _preview_breadcrumb() -> FT:
    return Div(
        Span("Home", cls="text-[10px] text-muted-foreground"),
        Icon("lucide:chevron-right", width="8", height="8", cls="mx-0.5 text-muted-foreground"),
        Span("Docs", cls="text-[10px] text-muted-foreground"),
        Icon("lucide:chevron-right", width="8", height="8", cls="mx-0.5 text-muted-foreground"),
        Span("Page", cls="text-[10px] font-medium text-foreground"),
        cls="flex items-center",
    )


def _preview_label() -> FT:
    return Div(
        Span("Email address", cls="text-[10px] font-medium text-foreground"),
        Div(cls="mt-1 h-7 w-36 rounded-md border border-border bg-background"),
    )


def _preview_theme_toggle() -> FT:
    return Div(
        Div(
            Icon("lucide:sun", width="14", height="14", cls="text-foreground"),
            cls="flex h-8 w-8 items-center justify-center rounded-md border border-border bg-background",
        ),
    )


def _preview_toggle() -> FT:
    return Div(
        Div(
            Icon("lucide:bold", width="12", height="12", cls="text-foreground"),
            cls="flex h-8 w-8 items-center justify-center rounded-md border border-border bg-foreground/10",
        ),
        Div(
            Icon("lucide:italic", width="12", height="12", cls="text-muted-foreground"),
            cls="flex h-8 w-8 items-center justify-center rounded-md border border-border",
        ),
        cls="flex gap-1",
    )


def _preview_toggle_group() -> FT:
    return Div(
        Div(
            Icon("lucide:align-left", width="10", height="10", cls="text-foreground"),
            cls="flex h-7 w-7 items-center justify-center rounded-l-md border border-border bg-foreground/10",
        ),
        Div(
            Icon("lucide:align-center", width="10", height="10", cls="text-muted-foreground"),
            cls="flex h-7 w-7 items-center justify-center border-y border-border",
        ),
        Div(
            Icon("lucide:align-right", width="10", height="10", cls="text-muted-foreground"),
            cls="flex h-7 w-7 items-center justify-center rounded-r-md border border-border",
        ),
        cls="flex",
    )


def _preview_typography() -> FT:
    return Div(
        Div("Heading", cls="mb-0.5 text-sm font-bold text-foreground"),
        Div(cls="mb-0.5 h-1.5 w-full rounded bg-muted-foreground/20"),
        Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/20"),
        cls="w-36",
    )


def _preview_code_block() -> FT:
    return Div(
        Div(cls="mb-1 h-1.5 w-16 rounded bg-blue-400/40"),
        Div(cls="mb-1 h-1.5 w-24 rounded bg-green-400/30"),
        Div(cls="h-1.5 w-20 rounded bg-orange-400/30"),
        cls="w-36 rounded-md border border-slate-700 bg-slate-900 p-2.5",
    )


def _preview_aspect_ratio() -> FT:
    return Div(
        Div(
            Icon("lucide:image", width="16", height="16", cls="text-muted-foreground/50"),
            cls="absolute inset-0 flex items-center justify-center rounded-md bg-muted/50",
        ),
        cls="relative w-40 overflow-hidden rounded-lg border border-border bg-background",
        style="aspect-ratio: 16/9",
    )


def _preview_collapsible() -> FT:
    return Div(
        Div(
            Span("Section A", cls="text-[10px] font-medium text-foreground"),
            Icon("lucide:chevron-down", width="8", height="8", cls="rotate-180 text-muted-foreground"),
            cls="flex items-center justify-between px-2 py-1.5",
        ),
        Div(
            Div(cls="mb-1 h-1.5 w-24 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-16 rounded bg-muted-foreground/20"),
            cls="px-2 pb-2",
        ),
        Div(
            Span("Section B", cls="text-[10px] font-medium text-muted-foreground"),
            Icon("lucide:chevron-down", width="8", height="8", cls="text-muted-foreground"),
            cls="flex items-center justify-between border-t border-border px-2 py-1.5",
        ),
        cls="w-36 overflow-hidden rounded-lg border border-border bg-background",
    )


def _preview_drawer() -> FT:
    return Div(
        Div(cls="flex-1 rounded bg-foreground/[0.04]"),
        Div(
            Div(cls="mx-auto mb-1.5 h-1 w-8 rounded-full bg-muted-foreground/30"),
            Div(cls="mb-1 h-2 w-16 rounded bg-foreground/80"),
            Div(cls="h-1.5 w-full rounded bg-muted-foreground/20"),
            cls="border-t border-border p-2",
        ),
        cls="flex h-16 w-36 flex-col overflow-hidden rounded-lg border border-border bg-background",
    )


def _preview_input_otp() -> FT:
    return Div(
        Div(
            *[Div(
                Span(c, cls="font-mono text-[10px] font-medium text-foreground") if c else None,
                cls="flex h-8 w-7 items-center justify-center rounded-md border border-border bg-background",
            ) for c in ["4", "2", ""]],
            cls="flex gap-0.5",
        ),
        Div(
            Div(cls="h-px w-1.5 bg-muted-foreground/40"),
            cls="flex items-center px-1",
        ),
        Div(
            *[Div(cls="h-8 w-7 rounded-md border border-border bg-background") for _ in range(3)],
            cls="flex gap-0.5",
        ),
        cls="flex items-center",
    )


def _preview_scroll_area() -> FT:
    return Div(
        Div(
            Div(cls="mb-1.5 h-1.5 w-20 rounded bg-muted-foreground/20"),
            Div(cls="mb-1.5 h-1.5 w-16 rounded bg-muted-foreground/20"),
            Div(cls="mb-1.5 h-1.5 w-22 rounded bg-muted-foreground/20"),
            Div(cls="mb-1.5 h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="mb-1.5 h-1.5 w-18 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-20 rounded bg-muted-foreground/20"),
            cls="min-w-0 flex-1 p-2",
        ),
        Div(
            Div(cls="h-7 w-[3px] rounded-full bg-foreground/25"),
            cls="flex items-start justify-end py-1.5 pr-1",
        ),
        cls="flex h-16 w-36 overflow-hidden rounded-lg border border-border bg-background",
    )


def _preview_slider() -> FT:
    return Div(
        Div(
            Div(
                Div(cls="h-full w-3/5 rounded-full bg-primary"),
                cls="relative h-1.5 w-full rounded-full bg-foreground/10",
            ),
            Div(cls="absolute top-1/2 h-3.5 w-3.5 -translate-y-1/2 rounded-full border-2 border-primary bg-background shadow-sm",
                style="left: calc(60% - 7px)"),
            cls="relative w-36",
        ),
    )


# ── Preview mapping ─────────────────────────────────────────────────

PREVIEW_MAP = {
    "accordion": _preview_accordion,
    "alert": _preview_alert,
    "alert_dialog": _preview_alert_dialog,
    "avatar": _preview_avatar,
    "badge": _preview_badge,
    "breadcrumb": _preview_breadcrumb,
    "button": _preview_button,
    "calendar": _preview_calendar,
    "card": _preview_card,
    "checkbox": _preview_checkbox,
    "code_block": _preview_code_block,
    "command": _preview_command,
    "date_picker": _preview_date_picker,
    "dialog": _preview_dialog,
    "dropdown_menu": _preview_dropdown_menu,
    "hover_card": _preview_hover_card,
    "input": _preview_input,
    "label": _preview_label,
    "menubar": _preview_menubar,
    "navigation_menu": _preview_navigation_menu,
    "pagination": _preview_pagination,
    "popover": _preview_popover,
    "progress": _preview_progress,
    "radio_group": _preview_radio_group,
    "select": _preview_select,
    "separator": _preview_separator,
    "sheet": _preview_sheet,
    "skeleton": _preview_skeleton,
    "switch": _preview_switch,
    "table": _preview_table,
    "tabs": _preview_tabs,
    "toast": _preview_toast,
    "textarea": _preview_textarea,
    "theme_toggle": _preview_theme_toggle,
    "toggle": _preview_toggle,
    "toggle_group": _preview_toggle_group,
    "tooltip": _preview_tooltip,
    "typography": _preview_typography,
    "aspect_ratio": _preview_aspect_ratio,
    "collapsible": _preview_collapsible,
    "drawer": _preview_drawer,
    "field": _preview_field,
    "input_otp": _preview_input_otp,
    "scroll_area": _preview_scroll_area,
    "slider": _preview_slider,
}


# ── Page styles ─────────────────────────────────────────────────────

def _index_styles() -> FT:
    return Style("""
        :root {
            --preview-bg: oklch(0.945 0 0);
        }
        .dark, [data-theme="dark"] {
            --preview-bg: oklch(0.16 0 0);
        }
        .cmp-preview-bg {
            background-color: var(--preview-bg);
        }
        .cmp-card {
            transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
            transition-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
        }
        .cmp-card:hover {
            border-color: color-mix(in srgb, var(--foreground) 35%, transparent);
            box-shadow: 0 4px 20px -4px color-mix(in srgb, var(--foreground) 10%, transparent);
            transform: translateY(-2px);
        }
        a:focus-visible .cmp-card {
            outline: 2px solid var(--ring);
            outline-offset: 2px;
        }
    """)


# ── Main page ───────────────────────────────────────────────────────

def create_components_index(registry: ComponentRegistry, sidebar_sections: list = None) -> FT:
    components = sorted(
        registry.components.items(),
        key=lambda x: (x[1].get("title", x[0]))
    )

    def cli_name(name: str) -> str:
        return name.replace("_", "-")

    def component_preview(name: str) -> FT:
        if name in PREVIEW_MAP:
            return PREVIEW_MAP[name]()
        icon = COMPONENT_ICONS.get(name, "lucide:component")
        return Icon(icon, width="36", height="36", cls="text-muted-foreground/40")

    def component_card(name: str, comp: dict) -> FT:
        return A(
            Div(
                Div(
                    component_preview(name),
                    cls="flex min-h-[160px] items-center justify-center p-6 cmp-preview-bg",
                ),
                Div(
                    Span(comp["title"], cls="truncate text-sm font-semibold text-foreground"),
                    Code(
                        f"star add {cli_name(name)}",
                        cls="shrink-0 font-mono text-xs whitespace-nowrap text-muted-foreground",
                    ),
                    cls="flex items-center justify-between gap-3 border-t border-border px-4 py-2.5",
                ),
                cls="overflow-hidden rounded-lg border border-border bg-card cmp-card",
            ),
            href=f"/components/{name}",
            cls="block",
        )

    return DocsLayout(
        _index_styles(),
        Div(
            P(
                "Beautifully designed components built with Python and Tailwind CSS.",
                cls="mb-1 text-lg text-muted-foreground",
            ),
            P(
                "Accessible. Customizable. Open Source.",
                cls="mb-8 text-sm text-muted-foreground",
            ),
            Div(
                *[component_card(name, comp) for name, comp in components],
                cls="grid auto-rows-fr gap-4 sm:grid-cols-2 lg:grid-cols-3 lg:gap-5",
            ),
            cls="mx-auto max-w-6xl",
        ),
        layout=LayoutConfig(
            title="Components",
            description="Explore all available StarUI components",
        ),
        sidebar=SidebarConfig(sections=sidebar_sections or []),
    )
