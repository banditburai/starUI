from typing import Any, TYPE_CHECKING
from starhtml import *
from starui.registry.components.theme_toggle import ThemeToggle
from starui.registry.components.button import Button

if TYPE_CHECKING:
    from layouts.base import HeaderConfig


def MobileMenuButton(signal: Signal, **attrs) -> FT:
    mobile_menu_open = Signal(f"{signal._id}_open", _ref_only=True)
    return Button(
        Icon("ph:list-bold", width="20", height="20"),
        data_on_click=mobile_menu_open.toggle(),
        variant="ghost",
        cls="xl:hidden h-9 px-4 py-2 flex-shrink-0",
        aria_label="Toggle mobile menu",
        **attrs,
    )


# ── Star mark — 4-pointed star ornament (16px) ──────────────────────


def _star_mark_small() -> FT:
    return Svg(
        SvgPath(d="M12 2L14 10L22 12L14 14L12 22L10 14L2 12L10 10Z", fill="currentColor"),
        viewBox="0 0 24 24",
        cls="star-mark-header w-5 h-5 text-sunset inline-block align-middle relative -top-[1px]",
        aria_hidden="true",
    )


# ── Navigation — single uppercase mono link ─────────────────────────


def _navigation_menu(nav_items: list[dict[str, Any]]) -> FT:
    return Nav(
        *[
            A(
                item["label"],
                href=item["href"],
                cls="text-xs font-mono uppercase tracking-[0.15em] text-foreground/60 hover:text-foreground transition-colors",
            )
            for item in nav_items
        ],
        cls="hidden xl:flex items-center gap-6",
    )


# ── Inline GitHub repo links with star ornament ─────────────────────


def _github_links() -> FT:
    link_cls = "text-[11px] font-mono text-foreground/50 hover:text-foreground transition-colors"
    return Div(
        A("starHTML", href="https://github.com/banditburai/starhtml", target="_blank", rel="noopener noreferrer", cls=link_cls),
        A(_star_mark_small(), href="https://ko-fi.com/promptsiren", target="_blank", rel="noopener noreferrer", aria_label="Support on Ko-fi", cls="flex items-center"),
        A("starUI", href="https://github.com/banditburai/starui", target="_blank", rel="noopener noreferrer", cls=link_cls),
        cls="hidden lg:flex items-center gap-2",
    )


# ── Header ───────────────────────────────────────────────────────────


def DocsHeader(config: "HeaderConfig", mobile_menu_signal: Signal | None = None, **attrs) -> FT:
    return Header(        
        Div(
            # Left: logo + nav
            Div(
                A(
                    _star_mark_small(),
                    Span("starui", cls="font-display text-lg tracking-wide"),
                    href=config.logo_href,
                    cls="flex items-baseline gap-0.5",
                ),
                _navigation_menu(config.nav_items),
                cls="flex items-baseline gap-6",
            ),
            # Right: GitHub links + theme toggle + mobile menu
            Div(
                _github_links(),
                ThemeToggle() if config.show_theme_toggle else None,
                MobileMenuButton(mobile_menu_signal) if mobile_menu_signal else None,
                cls="flex items-center gap-3",
            ),
            cls="flex h-14 w-full items-center justify-between px-4 sm:px-6 md:px-8 lg:px-6 max-w-full mx-auto",
        ),
        cls="sticky top-0 z-50 w-full border-b border-border bg-background",
        style="will-change: transform; transform: translateZ(0); backface-visibility: hidden;",
        **attrs,
    )
