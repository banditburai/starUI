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
    "hover_card": "lucide:mouse-pointer",
    "input": "lucide:type",
    "label": "lucide:text",
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
    "toggle": "lucide:toggle-right",
    "toggle_group": "lucide:group",
    "tooltip": "lucide:message-circle",
    "typography": "lucide:heading",
}


# ── Miniature skeleton previews ─────────────────────────────────────


def _preview_button() -> FT:
    return Div(
        Div("Primary", cls="h-7 px-3 rounded-md bg-primary text-primary-foreground text-[10px] flex items-center font-medium"),
        Div("Outline", cls="h-7 px-3 rounded-md border border-border text-[10px] flex items-center font-medium text-muted-foreground"),
        cls="flex gap-2 items-center",
    )


def _preview_input() -> FT:
    return Div(
        Span("Email", cls="text-[10px] font-medium text-foreground mb-1 block"),
        Div(
            Span("you@example.com", cls="text-[10px] text-muted-foreground"),
            cls="h-7 w-44 rounded-md border border-border bg-background px-2 flex items-center",
        ),
    )


def _preview_card() -> FT:
    return Div(
        Div(cls="h-2 w-20 rounded bg-foreground/80 mb-1"),
        Div(cls="h-1.5 w-28 rounded bg-muted-foreground/40 mb-2.5"),
        Div(cls="h-1.5 w-full rounded bg-muted-foreground/20 mb-0.5"),
        Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/20"),
        cls="w-44 rounded-lg border border-border p-3 bg-background",
    )


def _preview_switch() -> FT:
    return Div(
        Div(
            Span("Notifications", cls="text-[10px] text-foreground"),
            Div(
                Div(cls="w-3 h-3 rounded-full bg-white absolute right-0.5 top-[2px] shadow-sm"),
                cls="w-7 h-4 rounded-full bg-primary relative shrink-0",
            ),
            cls="flex items-center gap-3",
        ),
        Div(
            Span("Dark mode", cls="text-[10px] text-muted-foreground"),
            Div(
                Div(cls="w-3 h-3 rounded-full bg-foreground/40 absolute left-0.5 top-[2px]"),
                cls="w-7 h-4 rounded-full bg-foreground/15 relative shrink-0",
            ),
            cls="flex items-center gap-3",
        ),
        cls="space-y-2",
    )


def _preview_tabs() -> FT:
    return Div(
        Div(
            Span("Account", cls="text-[10px] font-medium text-foreground px-2 py-1 rounded bg-background"),
            Span("Password", cls="text-[10px] text-muted-foreground px-2 py-1"),
            cls="flex gap-0.5 p-0.5 rounded-md bg-foreground/[0.06] w-fit mb-2",
        ),
        Div(cls="h-1.5 w-28 rounded bg-muted-foreground/20 mb-1.5"),
        Div(cls="h-6 w-full rounded-md border border-border"),
    )


def _preview_dialog() -> FT:
    return Div(
        Div(cls="h-2 w-24 rounded bg-foreground/80 mb-1"),
        Div(cls="h-1.5 w-full rounded bg-muted-foreground/30 mb-0.5"),
        Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/30 mb-2.5"),
        Div(
            Div("Cancel", cls="h-6 px-2 rounded-md border border-border text-[9px] flex items-center text-muted-foreground"),
            Div("Continue", cls="h-6 px-2 rounded-md bg-primary text-primary-foreground text-[9px] flex items-center"),
            cls="flex gap-1.5 justify-end",
        ),
        cls="w-44 rounded-lg border border-border p-3 bg-background shadow-lg",
    )


def _preview_badge() -> FT:
    return Div(
        Span("Badge", cls="px-2 py-0.5 rounded-full bg-primary text-primary-foreground text-[9px] font-medium"),
        Span("Secondary", cls="px-2 py-0.5 rounded-full bg-muted text-muted-foreground text-[9px] font-medium"),
        Span("Outline", cls="px-2 py-0.5 rounded-full border border-border text-foreground text-[9px] font-medium"),
        cls="flex gap-1.5 items-center flex-wrap",
    )


def _preview_accordion() -> FT:
    return Div(
        Div(
            Span("Is it accessible?", cls="text-[10px] text-foreground font-medium"),
            Icon("lucide:chevron-down", width="10", height="10", cls="text-muted-foreground"),
            cls="flex items-center justify-between py-1.5 border-b border-border",
        ),
        Div(
            Span("How does it work?", cls="text-[10px] text-foreground font-medium"),
            Icon("lucide:chevron-down", width="10", height="10", cls="text-muted-foreground"),
            cls="flex items-center justify-between py-1.5 border-b border-border",
        ),
        Div(
            Span("Can I customize it?", cls="text-[10px] text-foreground font-medium"),
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
            cls="flex items-center gap-1.5 px-2 py-1.5 border-b border-border",
        ),
        Div(
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-18 rounded bg-muted-foreground/20"),
            cls="p-1.5 space-y-1.5",
        ),
        cls="w-36 rounded-lg border border-border bg-background shadow-lg overflow-hidden",
    )


def _preview_select() -> FT:
    return Div(
        Span("Theme", cls="text-[10px] font-medium text-foreground mb-1 block"),
        Div(
            Span("Select...", cls="text-[10px] text-muted-foreground"),
            Icon("lucide:chevron-down", width="10", height="10", cls="text-muted-foreground"),
            cls="h-7 w-36 rounded-md border border-border px-2 flex items-center justify-between bg-background",
        ),
    )


def _preview_checkbox() -> FT:
    return Div(
        Div(
            Div(
                Icon("lucide:check", width="8", height="8", cls="text-primary-foreground"),
                cls="w-3.5 h-3.5 rounded-sm border border-primary bg-primary flex items-center justify-center shrink-0",
            ),
            Span("Accept terms", cls="text-[10px] text-foreground"),
            cls="flex items-center gap-1.5",
        ),
        Div(
            Div(cls="w-3.5 h-3.5 rounded-sm border border-border shrink-0"),
            Span("Subscribe", cls="text-[10px] text-muted-foreground"),
            cls="flex items-center gap-1.5",
        ),
        cls="space-y-2",
    )


def _preview_alert() -> FT:
    return Div(
        Div(
            Icon("lucide:alert-circle", width="12", height="12", cls="text-foreground shrink-0 mt-0.5"),
            Div(
                Div(cls="h-2 w-14 rounded bg-foreground/80 mb-0.5"),
                Div(cls="h-1.5 w-32 rounded bg-muted-foreground/30"),
            ),
            cls="flex gap-2",
        ),
        cls="w-44 rounded-lg border border-border p-2.5 bg-background",
    )


def _preview_alert_dialog() -> FT:
    return _preview_dialog()


def _preview_progress() -> FT:
    return Div(
        Div(
            Div(cls="h-full w-2/3 rounded-full bg-primary"),
            cls="h-2 w-40 rounded-full bg-foreground/10 overflow-hidden",
        ),
    )


def _preview_table() -> FT:
    return Div(
        Div(
            Div(cls="h-1.5 w-10 rounded bg-muted-foreground/40"),
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/40"),
            Div(cls="h-1.5 w-8 rounded bg-muted-foreground/40"),
            cls="flex gap-3 px-2 py-1.5 border-b border-border",
        ),
        Div(
            Div(cls="h-1.5 w-10 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-8 rounded bg-muted-foreground/20"),
            cls="flex gap-3 px-2 py-1.5 border-b border-border",
        ),
        Div(
            Div(cls="h-1.5 w-10 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-8 rounded bg-muted-foreground/20"),
            cls="flex gap-3 px-2 py-1.5",
        ),
        cls="w-40 rounded-lg border border-border overflow-hidden",
    )


def _preview_avatar() -> FT:
    return Div(
        Div(Span("JD", cls="text-[9px] font-medium text-primary-foreground"), cls="w-8 h-8 rounded-full bg-primary flex items-center justify-center"),
        Div(Span("AB", cls="text-[9px] font-medium text-primary-foreground"), cls="w-8 h-8 rounded-full bg-primary/70 flex items-center justify-center"),
        Div(Span("KL", cls="text-[9px] font-medium text-primary-foreground"), cls="w-8 h-8 rounded-full bg-primary/50 flex items-center justify-center"),
        cls="flex -space-x-2",
    )


def _preview_skeleton() -> FT:
    return Div(
        Div(cls="h-8 w-8 rounded-full bg-foreground/10 animate-pulse"),
        Div(
            Div(cls="h-2 w-28 rounded bg-foreground/10 animate-pulse"),
            Div(cls="h-1.5 w-20 rounded bg-foreground/10 animate-pulse"),
            cls="space-y-1.5",
        ),
        cls="flex gap-2.5 items-center",
    )


def _preview_separator() -> FT:
    return Div(
        Div(cls="h-1.5 w-full rounded bg-muted-foreground/20"),
        Div(cls="h-px w-full bg-border my-1.5"),
        Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/20"),
        cls="w-36",
    )


def _preview_radio_group() -> FT:
    return Div(
        Div(
            Div(
                Div(cls="w-1.5 h-1.5 rounded-full bg-primary"),
                cls="w-3.5 h-3.5 rounded-full border-2 border-primary flex items-center justify-center shrink-0",
            ),
            Span("Default", cls="text-[10px] text-foreground"),
            cls="flex items-center gap-1.5",
        ),
        Div(
            Div(cls="w-3.5 h-3.5 rounded-full border border-border shrink-0"),
            Span("Comfortable", cls="text-[10px] text-muted-foreground"),
            cls="flex items-center gap-1.5",
        ),
        cls="space-y-2",
    )


def _preview_textarea() -> FT:
    return Div(
        Span("Message", cls="text-[10px] font-medium text-foreground mb-1 block"),
        Div(
            Span("Type your message...", cls="text-[10px] text-muted-foreground"),
            cls="w-40 h-12 rounded-md border border-border bg-background p-2",
        ),
    )


def _preview_sheet() -> FT:
    return Div(
        Div(cls="flex-1 bg-foreground/[0.04] rounded"),
        Div(
            Div(cls="h-2 w-10 rounded bg-foreground/80 mb-1.5"),
            Div(cls="h-1.5 w-full rounded bg-muted-foreground/20 mb-0.5"),
            Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/20"),
            cls="w-14 border-l border-border p-1.5",
        ),
        cls="flex gap-0 w-40 h-14 rounded-lg border border-border overflow-hidden bg-background",
    )


def _preview_tooltip() -> FT:
    return Div(
        Span("Hover me", cls="text-[10px] text-foreground underline decoration-dashed underline-offset-2"),
        Div(
            Span("Tooltip content", cls="text-[9px] text-primary-foreground"),
            cls="px-1.5 py-0.5 rounded bg-primary mt-1",
        ),
    )


def _preview_hover_card() -> FT:
    return Div(
        Span("@user", cls="text-[10px] text-primary font-medium underline underline-offset-2"),
        Div(
            Div(cls="w-5 h-5 rounded-full bg-foreground/10 mb-1"),
            Div(cls="h-1.5 w-16 rounded bg-muted-foreground/30 mb-0.5"),
            Div(cls="h-1.5 w-12 rounded bg-muted-foreground/20"),
            cls="rounded-lg border border-border p-2 bg-background shadow-lg mt-1 w-24",
        ),
    )


def _preview_dropdown_menu() -> FT:
    return Div(
        Div(
            Div(cls="h-1.5 w-14 rounded bg-muted-foreground/20"),
            Div(cls="h-1.5 w-18 rounded bg-muted-foreground/20"),
            Div(cls="h-px w-full bg-border my-0.5"),
            Div(cls="h-1.5 w-12 rounded bg-muted-foreground/20"),
            cls="w-28 rounded-lg border border-border bg-background p-1.5 shadow-lg space-y-1",
        ),
    )


def _preview_popover() -> FT:
    return Div(
        Div("Open", cls="h-6 px-2 rounded-md bg-primary text-primary-foreground text-[9px] flex items-center font-medium"),
        Div(
            Div(cls="h-1.5 w-16 rounded bg-muted-foreground/30 mb-1"),
            Div(cls="h-5 w-full rounded-md border border-border"),
            cls="w-28 rounded-lg border border-border p-2 bg-background shadow-lg mt-1",
        ),
    )


def _preview_date_picker() -> FT:
    return Div(
        Div(
            Icon("lucide:calendar", width="10", height="10", cls="text-muted-foreground"),
            Span("Pick a date", cls="text-[10px] text-muted-foreground"),
            cls="h-7 w-36 rounded-md border border-border px-2 flex items-center gap-1.5 bg-background",
        ),
    )


def _preview_calendar() -> FT:
    return Div(
        Div(
            Icon("lucide:chevron-left", width="8", height="8", cls="text-muted-foreground"),
            Span("Feb 2026", cls="text-[8px] font-medium text-foreground"),
            Icon("lucide:chevron-right", width="8", height="8", cls="text-muted-foreground"),
            cls="flex items-center justify-between mb-1.5 px-0.5",
        ),
        Div(
            *[Div(d, cls="w-4 h-4 text-[7px] flex items-center justify-center text-muted-foreground") for d in ["S", "M", "T", "W", "T", "F", "S"]],
            *[Div(
                str(n),
                cls=f"w-4 h-4 text-[7px] flex items-center justify-center {'rounded bg-primary text-primary-foreground' if n == 23 else 'text-foreground'}"
            ) for n in range(1, 15)],
            cls="grid grid-cols-7 gap-px",
        ),
        cls="w-32 rounded-lg border border-border p-1.5 bg-background",
    )


def _preview_breadcrumb() -> FT:
    return Div(
        Span("Home", cls="text-[10px] text-muted-foreground"),
        Icon("lucide:chevron-right", width="8", height="8", cls="text-muted-foreground mx-0.5"),
        Span("Docs", cls="text-[10px] text-muted-foreground"),
        Icon("lucide:chevron-right", width="8", height="8", cls="text-muted-foreground mx-0.5"),
        Span("Page", cls="text-[10px] text-foreground font-medium"),
        cls="flex items-center",
    )


def _preview_label() -> FT:
    return Div(
        Span("Email address", cls="text-[10px] font-medium text-foreground"),
        Div(cls="h-7 w-36 rounded-md border border-border bg-background mt-1"),
    )


def _preview_theme_toggle() -> FT:
    return Div(
        Div(
            Icon("lucide:sun", width="14", height="14", cls="text-foreground"),
            cls="w-8 h-8 rounded-md border border-border flex items-center justify-center bg-background",
        ),
    )


def _preview_toggle() -> FT:
    return Div(
        Div(
            Icon("lucide:bold", width="12", height="12", cls="text-foreground"),
            cls="w-8 h-8 rounded-md bg-foreground/10 border border-border flex items-center justify-center",
        ),
        Div(
            Icon("lucide:italic", width="12", height="12", cls="text-muted-foreground"),
            cls="w-8 h-8 rounded-md border border-border flex items-center justify-center",
        ),
        cls="flex gap-1",
    )


def _preview_toggle_group() -> FT:
    return Div(
        Div(
            Icon("lucide:align-left", width="10", height="10", cls="text-foreground"),
            cls="w-7 h-7 rounded-l-md bg-foreground/10 border border-border flex items-center justify-center",
        ),
        Div(
            Icon("lucide:align-center", width="10", height="10", cls="text-muted-foreground"),
            cls="w-7 h-7 border-y border-border flex items-center justify-center",
        ),
        Div(
            Icon("lucide:align-right", width="10", height="10", cls="text-muted-foreground"),
            cls="w-7 h-7 rounded-r-md border border-border flex items-center justify-center",
        ),
        cls="flex",
    )


def _preview_typography() -> FT:
    return Div(
        Div("Heading", cls="text-sm font-bold text-foreground mb-0.5"),
        Div(cls="h-1.5 w-full rounded bg-muted-foreground/20 mb-0.5"),
        Div(cls="h-1.5 w-3/4 rounded bg-muted-foreground/20"),
        cls="w-36",
    )


def _preview_code_block() -> FT:
    return Div(
        Div(cls="h-1.5 w-16 rounded bg-blue-400/40 mb-1"),
        Div(cls="h-1.5 w-24 rounded bg-green-400/30 mb-1"),
        Div(cls="h-1.5 w-20 rounded bg-orange-400/30"),
        cls="w-36 rounded-md bg-slate-900 p-2.5 border border-slate-700",
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
    "textarea": _preview_textarea,
    "theme_toggle": _preview_theme_toggle,
    "toggle": _preview_toggle,
    "toggle_group": _preview_toggle_group,
    "tooltip": _preview_tooltip,
    "typography": _preview_typography,
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
                    cls="cmp-preview-bg min-h-[160px] flex items-center justify-center p-6",
                ),
                Div(
                    Span(comp["title"], cls="text-sm font-semibold text-foreground truncate"),
                    Code(
                        f"star add {cli_name(name)}",
                        cls="text-xs font-mono text-muted-foreground whitespace-nowrap shrink-0",
                    ),
                    cls="flex items-center justify-between gap-3 px-4 py-2.5 border-t border-border",
                ),
                cls="cmp-card bg-card border border-border rounded-lg overflow-hidden",
            ),
            href=f"/components/{name}",
            cls="block",
        )

    return DocsLayout(
        _index_styles(),
        Div(
            P(
                "Beautifully designed components built with Python and Tailwind CSS.",
                cls="text-lg text-muted-foreground mb-1",
            ),
            P(
                "Accessible. Customizable. Open Source.",
                cls="text-sm text-muted-foreground mb-8",
            ),
            Div(
                *[component_card(name, comp) for name, comp in components],
                cls="grid gap-4 lg:gap-5 sm:grid-cols-2 lg:grid-cols-3 auto-rows-fr",
            ),
            cls="max-w-6xl mx-auto",
        ),
        layout=LayoutConfig(
            title="Components",
            description="Explore all available StarUI components",
        ),
        sidebar=SidebarConfig(sections=sidebar_sections or []),
    )
