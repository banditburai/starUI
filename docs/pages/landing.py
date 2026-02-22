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
        cls=f"star-mark w-4 h-4 text-sunset inline-block align-middle {cls}",
        aria_hidden="true",
    )


# ── Hero section ────────────────────────────────────────────────────


def hero_section() -> FT:
    """Asymmetric hero: headline left, terminal right, observatory arc behind."""

    return Section(
        # Observatory arc — single confident geometric element
        Div(cls="hero-arc", aria_hidden="true"),
        # Content grid
        Div(
            Div(
                # ── Left column: headline + subtitle + CTA ──
                Div(
                    # Headline — enormous with internal scale contrast
                    H1(
                        Span("Components", cls="block"),
                        Span("you own.", cls="block italic"),
                        Span("No JS required.", cls="block hero-subline text-sunset font-normal mt-6"),
                        cls="hero-headline font-display text-5xl md:text-[7rem] lg:text-[9rem] font-light text-moon",
                        data_motion=in_view(y=30, opacity=0, duration=500, spring="gentle"),
                    ),
                    # Subtitle with star mark
                    P(
                        _star_mark(cls="mr-2 -mt-0.5"),
                        "No npm. No React. Just Python.",
                        cls="mt-8 md:mt-10 font-serif-body text-xl md:text-2xl text-moon-dim italic font-light",
                        data_motion=in_view(y=20, opacity=0, duration=500, delay=100, spring="gentle"),
                    ),
                    # Single CTA
                    Div(
                        A(
                            "Get Started",
                            href="/installation",
                            cls="btn-star rounded-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[#FB923C]",
                            data_motion=press(scale=0.97, duration=100),
                        ),
                        cls="mt-10 md:mt-12",
                        data_motion=in_view(y=15, opacity=0, duration=400, delay=200, spring="gentle"),
                    ),
                    cls="lg:col-span-3",
                ),
                # ── Right column: terminal quickstart ──
                Div(
                    # Editorial label + rule
                    Div(
                        Span("Quickstart", cls="text-[9px] font-mono tracking-[0.25em] uppercase text-sunset block mb-2"),
                        Div(cls="w-3/5 h-px bg-current text-sunset opacity-40"),
                        cls="mb-4",
                    ),
                    # Terminal content — clean, no brackets, no dots
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
                            Span("$", cls="text-[#FB923C]"), " star add button dialog card",
                            cls="text-[#94A3B8]",
                        ),
                        cls="terminal-window p-6 space-y-2 font-mono text-sm",
                    ),
                    cls="lg:col-span-2 lg:pt-12 lg:self-end",
                    data_motion=in_view(y=30, opacity=0, duration=600, delay=300, spring="gentle"),
                ),
                cls="relative z-10 grid grid-cols-1 lg:grid-cols-5 gap-12 lg:gap-16 items-end",
            ),
            cls="w-full max-w-7xl mx-auto px-6 lg:px-8",
        ),
        cls="relative min-h-[90vh] flex items-end pb-24 pt-32",
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
