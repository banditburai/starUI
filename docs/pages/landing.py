"""Landing page sections for StarUI documentation site.

Asymmetric editorial hero with terminal sidebar.
Dark mode: navy→warm horizon. Light mode: cool dawn gradient.
"""

from starhtml import *
from starhtml.plugins import in_view, press


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


# ── The Constellation section ───────────────────────────────────────


def _constellation_card(
    fig_num: str,
    title: str,
    subtitle: str,
    preview_content: FT,
    fig_align: str = "top-4 right-4",
    label_align: str = "text-left",
    extra_cls: str = "rounded-sm",
) -> FT:
    return Div(
        Div(f"FIG. {fig_num}", cls=f"absolute {fig_align} text-[10px] tracking-widest text-sunset font-mono"),
        Div(
            preview_content,
            cls="card-preview flex-grow flex items-center justify-center border border-white/[0.05] m-4 bg-[#0B1221] overflow-hidden relative",
        ),
        Div(
            H3(title, cls="font-display text-xl italic mb-1 text-moon"),
            P(subtitle, cls="text-xs text-moon-dim uppercase tracking-wider"),
            cls=label_align,
        ),
        cls=f"mystic-card p-8 h-[400px] flex flex-col justify-between relative group {extra_cls}",
        data_motion=in_view(y=30, opacity=0, duration=600, spring="gentle"),
    )


def features_section() -> FT:
    """The Constellation — 3 tall cards with component previews and SVG connectors."""

    button_preview = Div(
        Div(
            "Summon",
            cls="bg-[#F8FAFC] text-[#0f172a] px-6 py-2 font-display italic hover:bg-[#FB923C] transition-colors cursor-pointer",
        ),
    )

    card_preview = Div(
        Div(cls="h-2 w-1/3 bg-[#334155]"),
        Div(cls="h-2 w-2/3 bg-[#1e293b]"),
        Div(cls="h-2 w-1/2 bg-[#1e293b]"),
        cls="w-full space-y-3 p-4 border border-white/[0.1]",
    )

    dialog_preview = Div(
        Div(
            Div(
                Div(cls="w-16 h-1 bg-[#FB923C] mb-2"),
                Div(cls="w-10 h-1 bg-[#475569]"),
                cls="bg-[#1e293b] border border-[#FB923C] p-4 w-32 h-20 flex flex-col justify-center items-center",
                style="box-shadow: 0 0 15px rgba(251, 146, 60, 0.2);",
            ),
            cls="absolute inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center",
        ),
    )

    return Section(
        Div(
            # Section header
            Div(
                Span("✦", cls="block text-sunset text-3xl mb-2"),
                H2(
                    "The Constellation",
                    cls="font-display text-4xl italic text-moon",
                ),
                P(
                    "Zero JavaScript authoring. Pure Python reactivity.",
                    cls="font-serif-body text-lg text-moon-dim mt-2 italic",
                ),
                cls="text-center mb-24",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            # Cards grid with constellation SVG lines
            Div(
                # SVG connectors (desktop only)
                Svg(
                    Line(x1="16%", y1="50%", x2="50%", y2="50%", cls="constellation-line"),
                    Line(x1="50%", y1="50%", x2="83%", y2="50%", cls="constellation-line"),
                    Circle(cx="50%", cy="50%", r="200", fill="none", stroke="rgba(203,213,225,0.1)", stroke_width="1"),
                    cls="absolute inset-0 w-full h-full pointer-events-none hidden md:block",
                    style="z-index: 0;",
                    aria_hidden="true",
                ),
                _constellation_card("01", "Button", "Polymorphic & Interactive", button_preview),
                _constellation_card(
                    "02", "Card", "Container Logic", card_preview,
                    fig_align="top-8 left-1/2 -translate-x-1/2",
                    label_align="text-center z-10",
                    extra_cls="rounded-t-[100px] border-t-0",
                ),
                _constellation_card(
                    "03", "Dialog", "Overlay Physics", dialog_preview,
                    fig_align="top-4 left-4",
                    label_align="text-right",
                ),
                cls="grid grid-cols-1 md:grid-cols-3 gap-8 relative",
            ),
            cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        cls="relative z-10 py-32 section-border-top",
    )


# ── The Trinity section ─────────────────────────────────────────────


def trinity_section() -> FT:
    """Three core principles, reference-style layout."""
    principles = [
        ("01", "Zero JavaScript", "Leverage the power of Datastar to drive reactive interfaces purely from your backend. No hydration gaps. No build steps."),
        ("02", "Type Safety", "Fully typed Python components. Catch errors in your IDE, not in the browser. Full autocompletion and IDE support out of the box."),
        ("03", "Vendor Ownership", "The code lives in your project. Customize every pixel, every border radius, and every animation timing to fit your brand."),
    ]

    return Section(
        Div(
            Div(
                H3(
                    "The Trinity",
                    cls="font-display text-3xl mb-6 italic text-moon",
                ),
                P(
                    "Three core principles guide the StarUI framework, ensuring your Python applications remain maintainable, scalable, and beautiful.",
                    cls="font-serif-body text-xl text-moon-dim leading-relaxed",
                ),
                cls="md:w-1/3 md:border-r md:border-white/[0.1] md:pr-8",
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
                    cls="font-display italic text-xl text-moon mb-4",
                ),
                P(
                    "© 2025 StarUI. Open Source MIT.",
                    cls="text-xs uppercase tracking-[0.2em] text-moon-dim",
                ),
                cls="text-center",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
        ),
        cls="relative z-10 section-border-top",
    )
