"""Landing page sections for StarUI documentation site.

Asymmetric editorial hero with terminal sidebar.
Dark mode: navy→warm horizon. Light mode: cool dawn gradient.
"""

from starhtml import *
from starhtml.plugins import in_view, press
from starui.registry.components.code_block import CodeBlock as StarlighterCode



# ── Star mark SVG (4-pointed, used as typographic ornament) ────────

def _star_mark(cls: str = "") -> FT:
    return Svg(
        Path(d="M12 2L14 10L22 12L14 14L12 22L10 14L2 12L10 10Z", fill="currentColor"),
        viewBox="0 0 24 24",
        cls=f"star-mark w-5 h-5 text-sunset inline-block align-middle {cls}",
        aria_hidden="true",
    )


# ── Hero section ────────────────────────────────────────────────────



def _component_showcase() -> FT:
    """Aperture brightness control — observatory instrument that controls starfield."""
    aperture = Signal("aperture", 50)
    active = aperture > 50

    return Div(
        aperture,
        # Energy flash overlay (triggered by star arrival)
        Div(cls="showcase-flash"),
        # Instrument label
        P("APERTURE", cls="text-[9px] font-mono font-medium tracking-[0.25em] uppercase text-[#94A3B8] showcase-card-title", style="font-family: 'Inter', sans-serif;"),
        # Range slider
        Div(
            Input(
                type="range",
                min="0",
                max="100",
                cls="aperture-slider w-full",
                data_bind=aperture,
            ),
            cls="mt-1.5",
        ),
        # Readout row — uses CSS custom properties for theme-aware colors
        Div(
            Span(
                Span(
                    cls="w-1 h-1 rounded-full inline-block transition-colors duration-300",
                    data_style_background_color=active.if_("var(--indicator-active)", "var(--indicator-dim)"),
                ),
                Span(data_text=active.if_("ACTIVE", "DIM")),
                cls="inline-flex items-center gap-1.5 text-[9px] font-mono font-medium uppercase tracking-[0.08em] px-1.5 py-0.5 rounded-sm border transition-all duration-300",
                data_style_color=active.if_("var(--indicator-active)", "var(--indicator-dim)"),
                data_style_border_color=active.if_("var(--indicator-active-border)", "var(--indicator-dim-border)"),
                data_style_background_color=active.if_("var(--indicator-active-bg)", "var(--indicator-dim-bg)"),
            ),
            Span(
                data_text="" + aperture + "%",
                cls="text-[11px] font-mono tabular-nums transition-colors duration-300",
                data_style_color=active.if_("var(--indicator-active)", "var(--indicator-dim)"),
            ),
            cls="flex items-center justify-between mt-1",
        ),
        # Reactive glow overlay — warms card as aperture rises
        Div(
            cls="aperture-glow absolute inset-0 rounded-[inherit] pointer-events-none transition-opacity duration-300",
            data_style_opacity="$aperture / 100",
        ),
        # Cool overlay — desaturates card at low aperture (light mode only, hidden in dark)
        Div(
            cls="aperture-cool absolute inset-0 rounded-[inherit] pointer-events-none transition-opacity duration-500",
            data_style_opacity="1 - $aperture / 100",
        ),
        # Pulse ring (emanates outward on star impact)
        Div(cls="showcase-pulse-ring"),
        # Star activates — sweep aperture from 50 to 90
        Div(data_init=(aperture.set(90), dict(delay="1400ms"))),
        cls="showcase-card px-4 py-2 select-none",
    )


def hero_section() -> FT:
    """Asymmetric hero: headline left, terminal right, observatory arc behind."""

    # ── Timing choreography ──────────────────────────────────────
    # 100ms  "Components" + "you own."  slide up together
    # 300ms  Star arc begins            traces dome (2.0s duration)
    # 400ms  Right column (terminal) + card arc-in
    # 500ms  "No JS required."          blooms in
    # 800ms  Subtitle + CTA             fade in together
    # ~1.4s  Card ignite + pulse + flash (star ~55% through arc)
    # ~1.4s  Aperture sweeps 50→90
    # ~2.3s  Star finishes arc
    # ──────────────────────────────────────────────────────────────

    arc_begin = "0.3s"
    arc_dur = "2.0s"

    # Arc path: cubic bezier with control points at phi divisions of 1100×680 viewBox
    arc_path = "M 60 260 C 434 7 666 18 1040 520"

    return Section(
        # Observatory arc SVG — golden spiral line + star tracing the path
        Svg(
            NotStr(
                '<defs>'
                '<linearGradient id="arc-fade" gradientUnits="userSpaceOnUse" x1="60" y1="260" x2="1040" y2="520">'
                '<stop offset="0%" stop-color="#FB923C" stop-opacity="0"/>'
                '<stop offset="12%" stop-color="#FB923C" stop-opacity="0.12"/>'
                '<stop offset="88%" stop-color="#FB923C" stop-opacity="0.12"/>'
                '<stop offset="100%" stop-color="#FB923C" stop-opacity="0"/>'
                '</linearGradient>'
                '</defs>'
            ),
            SvgPath(
                d=arc_path,
                fill="none",
                stroke="url(#arc-fade)",
                cls="arc-line",
            ),
            G(
                G(
                    SvgPath(
                        d="M0 -10 L3 -3 L10 0 L3 3 L0 10 L-3 3 L-10 0 L-3 -3 Z",
                        cls="arc-star-halo",
                        opacity="0",
                    ),
                    NotStr(
                        '<animate attributeName="opacity" '
                        'values="0;0;0.85;0;0" keyTimes="0;0.25;0.5;0.75;1" '
                        f'dur="{arc_dur}" begin="{arc_begin}" fill="freeze" '
                        'calcMode="spline" '
                        'keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/>'
                    ),
                ),
                SvgPath(
                    d="M0 -10 L3 -3 L10 0 L3 3 L0 10 L-3 3 L-10 0 L-3 -3 Z",
                    cls="arc-star",
                ),
                NotStr(
                    f'<animateMotion path="{arc_path}" '
                    f'dur="{arc_dur}" begin="{arc_begin}" fill="freeze" '
                    'calcMode="spline" keySplines="0.25 0.1 0.25 1" keyTimes="0;1"/>'
                ),
                NotStr(
                    '<animate attributeName="opacity" '
                    'values="0;1;1;0" keyTimes="0;0.05;0.92;1" '
                    f'dur="{arc_dur}" begin="{arc_begin}" fill="freeze"/>'
                ),
                NotStr(
                    '<animateTransform attributeName="transform" type="rotate" '
                    'from="0 0 0" to="180 0 0" '
                    f'dur="{arc_dur}" begin="{arc_begin}" fill="freeze" '
                    'calcMode="spline" keySplines="0.42 0 0.58 1" keyTimes="0;1" '
                    'additive="sum"/>'
                ),
                NotStr(
                    '<animateTransform attributeName="transform" type="scale" '
                    'values="0.4;1.3;0.4" keyTimes="0;0.5;1" '
                    f'dur="{arc_dur}" begin="{arc_begin}" fill="freeze" '
                    'calcMode="spline" '
                    'keySplines="0.42 0 0.58 1;0.42 0 0.58 1" '
                    'additive="sum"/>'
                ),
                cls="arc-star-group",
                opacity="0",
            ),
            viewBox="0 0 1100 680",
            cls="hero-arc",
            aria_hidden="true",
        ),
        # Content grid — 3fr / 2fr ≈ 60/40 split
        Div(
            Div(
                # ── Left column: headline + subtitle + CTA ──
                Div(
                    H1(
                        # Lines 1+2 appear nearly together
                        Span(
                            "Components",
                            cls="block",
                            data_motion=in_view(
                                y=30, x=-8, opacity=0,
                                duration=600, delay=100,
                                spring="gentle",
                            ),
                        ),
                        Span(
                            "you own.",
                            cls="block italic",
                            data_motion=in_view(
                                y=30, opacity=0,
                                duration=600, delay=200,
                                spring="gentle",
                            ),
                        ),
                        # Orange punchline — quick beat after headline
                        Span(
                            "No JS required.",
                            cls="block hero-subline text-sunset font-normal mt-6",
                            data_motion=in_view(
                                y=-6, scale=0.96, opacity=0,
                                duration=500, delay=500,
                                spring="snappy",
                            ),
                        ),
                        cls="hero-headline font-display font-light text-moon",
                    ),
                    # Subtitle + CTA — Fibonacci vertical rhythm (34px, 55px)
                    P(
                        "No npm. No React. Just Python.",
                        cls="mt-5 md:mt-[55px] font-serif-body text-xl md:text-2xl text-moon-dim italic font-light",
                        data_motion=in_view(
                            y=12, opacity=0,
                            duration=400, delay=800,
                            spring="gentle",
                        ),
                    ),
                    Div(
                        A(
                            "Get Started",
                            href="/installation",
                            cls="btn-star rounded-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[#FB923C]",
                            data_motion=press(scale=0.97, duration=100),
                        ),
                        cls="mt-[34px] md:mt-[55px]",
                        data_motion=in_view(
                            y=8, opacity=0,
                            duration=400, delay=900,
                            spring="gentle",
                        ),
                    ),
                ),
                # ── Right column: label above, card overlaps terminal upper-right ──
                Div(
                    Div(
                        Div(
                            Span("Quickstart", cls="text-[11px] font-mono font-semibold tracking-[0.25em] uppercase text-sunset block mb-2"),
                            Div(cls="showcase-divider-line w-full h-px bg-current text-sunset opacity-40"),
                            cls="showcase-label mb-4",
                        ),
                        Div(
                            Div(
                                P(
                                    Span("$", cls="text-[#FB923C]"), " pip install starui",
                                    cls="text-[#94A3B8]",
                                ),
                                P(
                                    Span("$", cls="text-[#FB923C]"), " star init",
                                    cls="text-[#94A3B8]",
                                ),
                                P(
                                    Span("$", cls="text-[#FB923C]"), " star add switch card dialog",
                                    cls="text-[#94A3B8]",
                                ),
                                cls="terminal-window p-6 space-y-2 font-mono text-sm",
                            ),
                            _component_showcase(),
                            cls="showcase-terminal-group",
                        ),
                        cls="showcase-float-wrapper relative",
                    ),
                    cls="hero-right-col flex flex-col",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=400, spring="gentle"),
                ),
                cls="hero-grid-phi relative z-10 grid grid-cols-1 gap-5",
            ),
            cls="w-full max-w-7xl mx-auto px-6 lg:px-8",
        ),
        # Fibonacci bottom padding: 89px (Fib 11); top padding stays at 128px (pt-32)
        cls="hero-section-mobile relative min-h-[90vh] flex items-center pb-[89px] pt-16 md:pt-20 lg:pt-24 overflow-x-clip",
        aria_label="Welcome to StarUI",
    )


# ── Code Example section ────────────────────────────────────────────


def code_example_section() -> FT:
    """FIG. 01 — Code editor + live preview in constellation glass panels."""

    example_code = '''from starhtml import *
from starui import (
    Card, CardHeader, CardTitle,
    CardDescription, CardContent,
    Input,
)

def profile():
    name = Signal("name", "friend")

    return Card(
        name,
        CardHeader(
            CardTitle(data_text=name.if_(
                "Hello, " + name,
                "Hello, stranger")),
            CardDescription(
                "Update your profile"),
        ),
        CardContent(
            Input(
                placeholder="Your name",
                data_bind=name),
        ),
    )'''

    # Live demo — mini-* styled for landing aesthetic, with real Datastar bindings
    name = Signal("hero_name", "friend")
    greeting = name.if_("Hello, " + name, "Hello, stranger")

    return Section(
        Div(
            # Header
            Div(
                Span("FIG. 01", cls="text-[10px] tracking-widest text-sunset font-mono block mb-3"),
                H2(
                    "Write Python. Get reactivity.",
                    cls="font-display text-3xl md:text-4xl italic text-moon mt-2",
                ),
                cls="mb-12",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            # Editor + Preview — glass panels
            Div(
                # Left: code editor in glass panel with filename header
                Div(
                    Div(
                        Div(
                            Span(cls="w-2.5 h-2.5 rounded-full bg-[#ff5f57]"),
                            Span(cls="w-2.5 h-2.5 rounded-full bg-[#febc2e]"),
                            Span(cls="w-2.5 h-2.5 rounded-full bg-[#28c840]"),
                            cls="flex gap-1.5",
                        ),
                        Span("app.py", cls="text-[11px] font-mono mini-text-dim"),
                        Div(cls="w-[52px]"),
                        cls="flex items-center justify-between px-4 py-2.5 border-b mini-border",
                    ),
                    StarlighterCode(example_code, "python", cls="!rounded-none !border-none !shadow-none !bg-transparent"),
                    cls="md:col-span-5 mystic-card rounded-xl overflow-hidden editor-panel",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=100, spring="gentle"),
                ),
                # Right: live preview — hand-styled to match landing aesthetic
                Div(
                    name,
                    Div(
                        # Card title — reactive, updates as you type
                        P(data_text=greeting, cls="text-lg font-medium mini-text"),
                        P("Update your profile", cls="text-xs mini-text-dim mt-1 mb-6"),
                        # Input — two-way bound to name signal
                        Div(
                            P("Name", cls="text-xs mini-text font-medium mb-1.5"),
                            Input(
                                placeholder="Your name",
                                data_bind=name,
                                cls="w-full py-2 px-3 rounded-md text-sm bg-transparent border mini-border mini-text outline-none fig01-input transition-colors",
                            ),
                        ),
                        cls="mini-surface rounded-xl p-6 w-full max-w-sm shadow-xl",
                    ),
                    cls="md:col-span-7 showcase-preview rounded-xl p-8 md:p-12 relative min-h-[400px] flex items-center justify-center",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=200, spring="gentle"),
                ),
                cls="grid grid-cols-1 md:grid-cols-12 gap-6",
            ),
            cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        cls="relative z-10 py-24 section-border-top",
    )


# ── Component explorer previews ───────────────────────────────────


def _explorer_command() -> FT:
    """Command palette — search input + categorized suggestion list."""
    return Div(
        Div(
            Icon("lucide:search", width="16", height="16", cls="mini-text-dim"),
            Span("Type a command or search...", cls="text-sm mini-text-dim font-light"),
            cls="flex items-center gap-3 px-4 py-3.5 border-b mini-border",
        ),
        Div(
            Span("Suggestions", cls="text-[11px] mini-text-dim font-medium block px-2 py-2"),
            Div(
                Icon("lucide:calendar", width="15", height="15"),
                Span("Calendar", cls="text-sm font-medium"),
                cls="flex items-center gap-3 px-3 py-2.5 rounded-lg mini-text explorer-active-row",
            ),
            Div(
                Icon("lucide:smile", width="15", height="15", cls="mini-text-dim"),
                Span("Search Emoji", cls="text-sm"),
                cls="flex items-center gap-3 px-3 py-2.5 rounded-lg mini-text-dim",
            ),
            Div(
                Icon("lucide:calculator", width="15", height="15", cls="mini-text-dim"),
                Span("Calculator", cls="text-sm"),
                cls="flex items-center gap-3 px-3 py-2.5 rounded-lg mini-text-dim",
            ),
            Div(cls="h-px mini-divider mx-2 my-1"),
            Span("Settings", cls="text-[11px] mini-text-dim font-medium block px-2 py-2"),
            Div(
                Div(Icon("lucide:user", width="15", height="15"), Span("Profile", cls="text-sm"), cls="flex items-center gap-3"),
                Span("⌘P", cls="text-[10px] px-1.5 py-0.5 rounded mini-bg-secondary mini-text-dim"),
                cls="flex items-center justify-between px-3 py-2.5 rounded-lg mini-text-dim",
            ),
            Div(
                Div(Icon("lucide:credit-card", width="15", height="15"), Span("Billing", cls="text-sm"), cls="flex items-center gap-3"),
                Span("⌘B", cls="text-[10px] px-1.5 py-0.5 rounded mini-bg-secondary mini-text-dim"),
                cls="flex items-center justify-between px-3 py-2.5 rounded-lg mini-text-dim",
            ),
            cls="p-2",
        ),
        cls="mini-surface rounded-xl w-full max-w-md overflow-hidden shadow-xl",
    )


def _explorer_card() -> FT:
    """Create account card with social login + form."""
    return Div(
        Div(
            P("Create account", cls="text-base font-medium mini-text"),
            P("Enter your email below to create your account", cls="text-xs mini-text-dim mt-1"),
            cls="mb-5",
        ),
        Div(
            Div(
                Icon("simple-icons:github", width="14", height="14"),
                Span("Github", cls="text-sm font-medium"),
                cls="flex items-center justify-center gap-2 w-full py-2.5 rounded-md border mini-border mini-text",
            ),
            Div(
                Icon("simple-icons:google", width="14", height="14"),
                Span("Google", cls="text-sm font-medium"),
                cls="flex items-center justify-center gap-2 w-full py-2.5 rounded-md border mini-border mini-text",
            ),
            cls="grid gap-2 mb-4",
        ),
        Div(
            Div(cls="flex-1 h-px mini-divider"),
            Span("Or continue with", cls="text-[10px] mini-text-dim uppercase px-2 whitespace-nowrap"),
            Div(cls="flex-1 h-px mini-divider"),
            cls="flex items-center mb-4",
        ),
        Div(
            P("Email", cls="text-xs mini-text font-medium mb-1"),
            Div(Span("m@example.com", cls="text-sm mini-text-dim"), cls="py-2 px-3 rounded-md border mini-border w-full"),
            cls="mb-3",
        ),
        Div(
            P("Password", cls="text-xs mini-text font-medium mb-1"),
            Div(cls="py-2 px-3 rounded-md border mini-border w-full h-[36px]"),
            cls="mb-4",
        ),
        Span("Create Account", cls="block text-center py-2.5 rounded-md mini-bg-primary font-medium text-sm w-full"),
        cls="mini-surface rounded-xl p-6 w-full max-w-sm shadow-xl",
    )


def _explorer_switch() -> FT:
    """Settings panel with toggles and badges."""
    return Div(
        Div(
            Span("Airplane Mode", cls="text-sm mini-text"),
            Div(
                Div(cls="w-4 h-4 rounded-full bg-white absolute right-0.5 top-[2px] shadow-sm"),
                cls="w-9 h-5 rounded-full mini-switch-on relative shrink-0",
            ),
            cls="flex items-center justify-between",
        ),
        Div(
            Span("Notifications", cls="text-sm mini-text-dim"),
            Div(
                Div(cls="w-4 h-4 rounded-full bg-white/70 absolute left-0.5 top-[2px]"),
                cls="w-9 h-5 rounded-full mini-switch-off relative shrink-0",
            ),
            cls="flex items-center justify-between",
        ),
        Div(
            Span("Dark Mode", cls="text-sm mini-text"),
            Div(
                Div(cls="w-4 h-4 rounded-full bg-white absolute right-0.5 top-[2px] shadow-sm"),
                cls="w-9 h-5 rounded-full mini-switch-on relative shrink-0",
            ),
            cls="flex items-center justify-between",
        ),
        Div(cls="h-px mini-divider my-2"),
        Div(
            Span("Active", cls="px-2.5 py-0.5 rounded-full text-[11px] font-medium mini-switch-on text-white"),
            Span("Beta", cls="px-2.5 py-0.5 rounded-full text-[11px] font-medium border mini-border mini-text-dim"),
            cls="flex gap-2",
        ),
        cls="mini-surface rounded-xl p-5 w-full max-w-xs space-y-4 shadow-xl",
    )


def _explorer_dialog() -> FT:
    """Alert dialog confirmation."""
    return Div(
        P("Are you absolutely sure?", cls="text-base font-medium mini-text"),
        P(
            "This action cannot be undone. This will permanently delete your account and remove your data from our servers.",
            cls="text-sm mini-text-dim mt-2 leading-relaxed",
        ),
        Div(
            Span("Cancel", cls="px-4 py-2 text-sm rounded-md border mini-border mini-text font-medium"),
            Span("Continue", cls="px-4 py-2 text-sm rounded-md mini-bg-primary font-medium"),
            cls="flex justify-end gap-3 mt-6",
        ),
        cls="mini-surface rounded-xl p-6 w-full max-w-md shadow-xl",
    )


def _explorer_tabs() -> FT:
    """Tab interface with account settings form."""
    return Div(
        Div(
            Span("Account", cls="text-sm font-medium mini-text px-4 py-2 rounded-md mini-bg-secondary"),
            Span("Password", cls="text-sm mini-text-dim px-4 py-2"),
            cls="flex gap-1 p-1 rounded-lg mini-bg-secondary w-fit mb-5",
        ),
        P("Make changes to your account here.", cls="text-sm mini-text-dim mb-4"),
        Div(
            P("Name", cls="text-xs mini-text font-medium mb-1.5"),
            Div(Span("Pedro Duarte", cls="text-sm mini-text"), cls="py-2 px-3 rounded-md border mini-border w-full"),
            cls="mb-3",
        ),
        Div(
            P("Username", cls="text-xs mini-text font-medium mb-1.5"),
            Div(Span("@peduarte", cls="text-sm mini-text"), cls="py-2 px-3 rounded-md border mini-border w-full"),
            cls="mb-5",
        ),
        Span("Save changes", cls="inline-block px-4 py-2 rounded-md mini-bg-primary font-medium text-sm"),
        cls="mini-surface rounded-xl p-6 w-full max-w-sm shadow-xl",
    )


def _explorer_button() -> FT:
    """Button variants showcase."""
    return Div(
        Div(
            Span("Primary", cls="px-5 py-2.5 text-sm rounded-md mini-bg-primary font-medium"),
            Span("Secondary", cls="px-5 py-2.5 text-sm rounded-md mini-bg-secondary mini-text font-medium"),
            Span("Outline", cls="px-5 py-2.5 text-sm rounded-md border mini-border mini-text font-medium"),
            cls="flex flex-wrap items-center gap-3 mb-5",
        ),
        Div(
            Span("Destructive", cls="px-5 py-2.5 text-sm rounded-md bg-red-600 text-white font-medium"),
            Span("Ghost", cls="px-5 py-2.5 text-sm mini-text-dim font-medium"),
            Span("Link", cls="px-5 py-2.5 text-sm text-sunset font-medium underline underline-offset-4"),
            cls="flex flex-wrap items-center gap-3",
        ),
        cls="mini-surface rounded-xl p-6 max-w-md shadow-xl",
    )


# ── Component Explorer section ────────────────────────────────────


def component_grid_section() -> FT:
    """FIG. 03 — Interactive component explorer with sidebar + preview panel."""

    active = Signal("explorer_cmp", "command")

    explorer_items = [
        ("Command", "command", "lucide:terminal", _explorer_command),
        ("Card", "card", "lucide:credit-card", _explorer_card),
        ("Switch", "switch", "lucide:toggle-left", _explorer_switch),
        ("Dialog", "dialog", "lucide:app-window", _explorer_dialog),
        ("Tabs", "tabs", "lucide:layout-list", _explorer_tabs),
        ("Button", "button", "lucide:mouse-pointer-click", _explorer_button),
    ]

    return Section(
        Div(
            # Header
            Div(
                Span("FIG. 03", cls="text-[10px] tracking-widest text-sunset font-mono block mb-3"),
                Div(
                    Div(
                        H2("The Constellation", cls="font-display text-4xl italic text-moon"),
                        P("34+ components built with Tailwind v4.", cls="font-serif-body text-lg text-moon-dim mt-2 italic"),
                    ),
                    A(
                        "View All Components →",
                        href="/components",
                        cls="text-sunset hover:text-[#FB923C] text-sm font-mono tracking-wide uppercase transition-colors hidden md:block shrink-0",
                    ),
                    cls="flex flex-col md:flex-row md:items-end md:justify-between gap-4",
                ),
                cls="mb-12",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            # Explorer: sidebar + preview
            Div(
                active,
                # Sidebar — component list
                Div(
                    Span("COMPONENTS", cls="text-[10px] font-mono tracking-widest text-sunset px-3 py-2 block"),
                    *[
                        Div(
                            Icon(icon, width="15", height="15", cls="shrink-0"),
                            Span(name, cls="text-sm"),
                            data_on_click=active.set(slug),
                            data_attr_cls=(active == slug).if_(
                                "mini-bg-secondary mini-text font-medium",
                                "mini-text-dim",
                            ),
                            cls="flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer transition-colors",
                        )
                        for name, slug, icon, _ in explorer_items
                    ],
                    cls="md:col-span-3 mystic-card rounded-xl p-3 flex flex-row md:flex-col gap-1 overflow-x-auto md:overflow-visible",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=100, spring="gentle"),
                ),
                # Preview area — shows active component
                Div(
                    *[
                        Div(
                            fn(),
                            data_show=active == slug,
                            cls="flex items-center justify-center w-full",
                        )
                        for _, slug, _, fn in explorer_items
                    ],
                    # star add command in corner
                    Div(
                        Code(
                            "star add command",
                            data_text="star add " + active,
                            cls="text-[10px] font-mono text-moon-dim",
                        ),
                        cls="absolute bottom-4 right-6",
                    ),
                    cls="md:col-span-9 showcase-preview rounded-xl p-8 md:p-12 relative min-h-[450px] flex items-center justify-center",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=200, spring="gentle"),
                ),
                cls="grid grid-cols-1 md:grid-cols-12 gap-6",
            ),
            # Mobile "view all" link
            Div(
                A(
                    "View All Components →",
                    href="/components",
                    cls="text-sunset hover:text-[#FB923C] text-sm font-mono tracking-wide uppercase transition-colors",
                ),
                cls="text-center mt-8 md:hidden",
            ),
            cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        cls="relative z-10 py-24 section-border-top",
    )


# ── Why StarUI section ─────────────────────────────────────────────


def why_starui_section() -> FT:
    """FIG. 02 — Editorial 1/3 + 2/3 split with value propositions."""

    principles = [
        ("01", "Own The Code", "No npm packages. No black boxes. The CLI copies component source directly into your project. Customize every pixel."),
        ("02", "Datastar Signals", "Full client-side reactivity without React. Toggle modals, update counters, and validate forms — all from Python-defined signals."),
        ("03", "Tailwind v4", "Styled with the latest engine. Dark mode, animations, and full utility support out of the box."),
    ]

    return Section(
        Div(
            Div(
                Span("FIG. 02", cls="text-[10px] tracking-widest text-sunset font-mono block mb-4"),
                H3(
                    "Why StarUI?",
                    cls="font-display text-3xl mb-6 italic text-moon",
                ),
                P(
                    "Stop fighting the frontend toolchain. StarUI brings the shadcn/ui architecture to Python.",
                    cls="font-serif-body text-xl text-moon-dim leading-relaxed",
                ),
                # Python logo — large watermark behind column content
                Icon(
                    "simple-icons:python",
                    width="220",
                    height="220",
                    cls="python-watermark absolute -bottom-8 -right-4 rotate-12 text-sunset pointer-events-none",
                    aria_hidden="true",
                ),
                cls="md:w-1/3 md:border-r md:border-white/[0.1] md:pr-8 relative overflow-visible",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            Div(
                *[
                    Div(
                        Div(
                            Span(num, cls="text-sunset font-mono text-sm font-semibold"),
                            H4(
                                title,
                                cls="text-lg uppercase tracking-[0.15em] font-light text-moon group-hover:text-sunset transition-colors",
                            ),
                            cls="flex items-baseline gap-4 mb-2",
                        ),
                        P(
                            desc,
                            cls="pl-10 text-moon-dim font-light leading-relaxed border-l border-white/[0.1] py-2",
                        ),
                        cls="group cursor-default",
                        data_motion=in_view(y=20, opacity=0, duration=500, delay=i * 100, spring="gentle"),
                    )
                    for i, (num, title, desc) in enumerate(principles)
                ],
                cls="md:w-2/3 grid grid-cols-1 gap-12",
            ),
            cls="max-w-5xl mx-auto flex flex-col md:flex-row gap-16 px-4 sm:px-6 lg:px-8",
        ),
        cls="relative z-10 py-24 section-border-top",
    )


# ── Final CTA ───────────────────────────────────────────────────────


def cta_section() -> FT:
    return Section(
        Div(
            Div(
                Svg(
                    Path(
                        d="M12 2L15 10L23 12L15 14L12 22L9 14L1 12L9 10L12 2Z",
                        fill="currentColor",
                    ),
                    cls="w-8 h-8 mx-auto text-sunset animate-pulse mb-8",
                    viewBox="0 0 24 24",
                ),
                P(
                    "Crafted for the Python Cosmos.",
                    cls="font-display italic text-xl text-moon mb-6",
                ),
                # Inline install terminal
                Div(
                    Pre(
                        NotStr(
                            '<span style="color:#FB923C">$</span> '
                            '<span style="color:#94A3B8">pip install starui</span>'
                        ),
                        cls="terminal-window px-6 py-3 font-mono text-sm inline-block",
                    ),
                    cls="mb-8",
                ),
                # Dual CTA
                Div(
                    A(
                        "Get Started",
                        href="/installation",
                        cls="btn-star rounded-none",
                        data_motion=press(scale=0.97, duration=100),
                    ),
                    A(
                        "View Components",
                        href="/components",
                        cls="btn-star-outline rounded-none",
                        data_motion=press(scale=0.97, duration=100),
                    ),
                    cls="flex flex-wrap items-center justify-center gap-4 mb-8",
                ),
                P(
                    "© 2026 StarUI. Open Source Apache 2.0.",
                    cls="text-xs uppercase tracking-[0.2em] text-moon-dim",
                ),
                cls="text-center",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
        ),
        cls="relative z-10 section-border-top",
    )
