from typing import Any, TYPE_CHECKING
from starhtml import *
from components.theme_toggle import ThemeToggle
from components.button import Button

if TYPE_CHECKING:
    from layouts.base import HeaderConfig


def MobileMenuButton(signal: Signal, **attrs) -> FT:
    mobile_menu_open = Signal(f"{signal._id}_open", _ref_only=True)
    return Button(
        Icon("ph:list-bold", width="20", height="20"),
        data_on_click=mobile_menu_open.toggle(),
        variant="ghost",
        cls="h-9 flex-shrink-0 px-4 py-2 xl:hidden",
        aria_label="Toggle mobile menu",
        **attrs,
    )


# ── Star mark — 4-pointed star ornament (16px) ──────────────────────


def _star_mark_small() -> FT:
    return Svg(
        SvgPath(d="M12 2L14 10L22 12L14 14L12 22L10 14L2 12L10 10Z", fill="currentColor"),
        viewBox="0 0 24 24",
        cls="relative -top-[1px] inline-block h-5 w-5 align-middle star-mark-header text-sunset",
        aria_hidden="true",
    )


# ── Navigation — single uppercase mono link ─────────────────────────


def _navigation_menu(nav_items: list[dict[str, Any]]) -> FT:
    return Nav(
        *[
            A(
                item["label"],
                href=item["href"],
                cls="font-mono text-xs tracking-[0.15em] text-foreground/60 uppercase transition-colors hover:text-foreground",
            )
            for item in nav_items
        ],
        cls="hidden items-center gap-6 xl:flex",
        aria_label="Main",
    )


# ── Inline GitHub repo links with star ornament ─────────────────────


def _github_links() -> FT:
    link_cls = "font-mono text-[11px] text-muted-foreground transition-colors hover:text-foreground"
    return Div(
        A("starHTML", href="https://github.com/banditburai/starhtml", target="_blank", rel="noopener noreferrer", cls=link_cls),
        A(_star_mark_small(), href="https://ko-fi.com/promptsiren", target="_blank", rel="noopener noreferrer", aria_label="Support on Ko-fi", cls="flex items-center"),
        A("starUI", href="https://github.com/banditburai/starui", target="_blank", rel="noopener noreferrer", cls=link_cls),
        cls="hidden items-center gap-2 lg:flex",
    )


# ── Header ───────────────────────────────────────────────────────────


def DocsHeader(config: "HeaderConfig", mobile_menu_signal: Signal | None = None, **attrs) -> FT:
    return Header(        
        Div(
            # Left: logo + nav
            Div(
                A(
                    _star_mark_small(),
                    Span("starui", cls="text-lg tracking-wide font-display"),
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
            cls="mx-auto flex h-14 w-full max-w-full items-center justify-between px-4 sm:px-6 md:px-8 lg:px-6",
        ),
        cls="sticky top-0 z-50 w-full border-b border-border bg-background",
        style="will-change: transform; transform: translateZ(0); backface-visibility: hidden;",
        **attrs,
    )
