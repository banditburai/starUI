import random

from starhtml import *
from starhtml.plugins import scroll
from layouts.header import DocsHeader
from layouts.footer import DocsFooter
from layouts.base import HeaderConfig, FooterConfig


def _landing_styles() -> FT:
    return Style("""
        /* ══════════════════════════════════════
           STARUI LANDING — Sunrise / Sunset
           Dark (default): navy→warm horizon, white text
           Light: cool dawn gradient, dark text
           ══════════════════════════════════════ */

        /* ── Landing page body font ── */
        .landing-page {
            font-family: 'Inter', sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* ── Font utilities ── */
        .font-display { font-family: 'Playfair Display', serif; }
        .font-serif-body { font-family: 'Cormorant Garamond', serif; }

        /* ── Hero headline — enormous with tight leading ── */
        .hero-headline {
            line-height: 0.85;
            letter-spacing: -0.03em;
        }
        .hero-subline {
            font-size: 0.55em;
            letter-spacing: 0.02em;
        }

        /* ── Star mark — breathing ornament ── */
        @keyframes star-breathe {
            0%, 100% { opacity: 0.4; }
            50% { opacity: 1; }
        }
        .star-mark {
            animation: star-breathe 4s ease-in-out infinite;
        }

        /* ── Observatory arc — single dome shape behind hero ── */
        .hero-arc {
            position: absolute;
            left: 50%;
            bottom: 35%;
            transform: translateX(-50%);
            width: 900px;
            height: 450px;
            border-radius: 450px 450px 0 0;
            border-top: 1px solid rgba(251, 146, 60, 0.12);
            border-left: 1px solid rgba(251, 146, 60, 0.12);
            border-right: 1px solid rgba(251, 146, 60, 0.12);
            border-bottom: none;
            pointer-events: none;
            z-index: 0;
        }
        [data-theme="light"] .hero-arc {
            border-color: rgba(212, 112, 10, 0.15);
        }
        @media (max-width: 768px) {
            .hero-arc {
                width: 500px;
                height: 250px;
                border-radius: 250px 250px 0 0;
            }
        }

        /* ── Fixed sky gradient ── */
        /* Default = dark mode (observatory_dawn_blue original) */
        .dawn-sky {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            transition: background 0.6s ease;
            background: linear-gradient(to bottom,
                #0B1221 0%,
                #1e293b 40%,
                #3e4c5f 70%,
                #8c5e45 100%);
            background-attachment: fixed;
        }

        /* Light = cool pre-dawn sky: blue-gray zenith → lavender → rose → warm gold horizon */
        [data-theme="light"] .dawn-sky {
            background: linear-gradient(180deg,
                #dfe8f3 0%,
                #e2dff0 25%,
                #f0e4e0 55%,
                #f5dbc4 80%,
                #edc9a0 100%);
        }

        /* ── Scroll-driven warm overlay ── */
        /* Fades in as user scrolls — dramatically warmer than base */
        .dawn-sky-warm {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            opacity: 0;
            background: linear-gradient(to bottom,
                rgba(26, 16, 24, 0.0) 0%,
                rgba(74, 32, 16, 0.35) 35%,
                rgba(160, 80, 32, 0.45) 65%,
                rgba(208, 104, 32, 0.5) 100%);
            background-attachment: fixed;
        }

        /* Light: gentle sunrise warmth — top stays transparent to preserve cool zenith */
        [data-theme="light"] .dawn-sky-warm {
            background: linear-gradient(180deg,
                rgba(245, 228, 210, 0.0) 0%,
                rgba(248, 215, 175, 0.4) 30%,
                rgba(245, 195, 130, 0.5) 60%,
                rgba(235, 175, 100, 0.6) 100%);
        }

        /* ── Star field ── */
        .star {
            position: absolute;
            border-radius: 50%;
            background: #fff;
            pointer-events: none;
            opacity: 0;
            box-shadow: 0 0 3px rgba(255, 255, 255, 0.8);
            animation: twinkle var(--dur, 3s) ease-in-out infinite;
            animation-delay: var(--delay, 0s);
        }

        /* Light: hide stars — they're a night phenomenon; let the gradient carry the atmosphere */
        [data-theme="light"] .star {
            display: none;
        }

        @keyframes twinkle {
            0% { opacity: 0; transform: scale(0.5); }
            50% { opacity: var(--max-opacity, 0.7); transform: scale(1); }
            100% { opacity: 0; transform: scale(0.5); }
        }

        /* ── Flashing crosses ── */
        .cross-mark {
            position: absolute;
            width: var(--size, 10px);
            height: var(--size, 10px);
            pointer-events: none;
            animation: cross-flash var(--dur, 8s) ease-in-out infinite;
            animation-delay: var(--delay, 0s);
        }

        .cross-mark::before, .cross-mark::after {
            content: '';
            position: absolute;
            background: #FB923C;
            opacity: 0.5;
        }

        .cross-mark::before {
            left: 50%; top: 0; width: 1px; height: 100%;
            transform: translateX(-50%);
        }

        .cross-mark::after {
            top: 50%; left: 0; width: 100%; height: 1px;
            transform: translateY(-50%);
        }

        /* Light: telescope reticle marks in warm copper — bridging cool sky and warm horizon */
        [data-theme="light"] .cross-mark::before,
        [data-theme="light"] .cross-mark::after {
            background: #b87a5a;
            opacity: 0.35;
        }

        @keyframes cross-flash {
            0%, 90%, 100% { opacity: 0; }
            5%, 8% { opacity: 0.9; }
        }

        /* ── Film grain overlay ── */
        .grain-overlay {
            position: fixed;
            inset: 0;
            opacity: 0.05;
            pointer-events: none;
            z-index: 100;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        }

        [data-theme="light"] .grain-overlay {
            opacity: 0.06;
            mix-blend-mode: multiply;
        }

        /* ── Glass morphism panels ── */
        .mystic-card {
            background: rgba(15, 23, 42, 0.35);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1);
        }

        .mystic-card:hover {
            border-color: #FB923C;
            box-shadow: 0 20px 40px -10px rgba(154, 52, 18, 0.25);
            transform: translateY(-4px);
            background: rgba(15, 23, 42, 0.5);
        }

        [data-theme="light"] .mystic-card {
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(140, 130, 150, 0.15);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 4px 20px -4px rgba(100, 80, 60, 0.08);
        }

        [data-theme="light"] .mystic-card:hover {
            border-color: #c87a3e;
            box-shadow: 0 20px 40px -10px rgba(200, 122, 62, 0.18);
            background: rgba(255, 255, 255, 0.8);
        }

        /* ── Card preview interiors ── */
        /* Light mode: softer background so previews don't punch dark holes */
        [data-theme="light"] .card-preview {
            background: #e8e4ee;
            border-color: rgba(100, 90, 120, 0.1);
        }

        /* ── Terminal code block (always dark) ── */
        .terminal-window {
            background: #020617;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 0 1px #000, 0 20px 50px -10px rgba(0, 0, 0, 0.7);
        }

        [data-theme="light"] .terminal-window {
            background: #1e293b;
            border: 1px solid rgba(160, 140, 110, 0.3);
            border-radius: 4px;
            box-shadow: 0 4px 20px rgba(120, 80, 30, 0.12);
        }

        /* ── Corner brackets ── */
        .corner-bracket {
            position: absolute;
            width: 20px;
            height: 20px;
            pointer-events: none;
        }
        .corner-bracket.tl { top: -3px; left: -3px; border-top: 2px solid #FB923C; border-left: 2px solid #FB923C; }
        .corner-bracket.tr { top: -3px; right: -3px; border-top: 2px solid #FB923C; border-right: 2px solid #FB923C; }
        .corner-bracket.bl { bottom: -3px; left: -3px; border-bottom: 2px solid #FB923C; border-left: 2px solid #FB923C; }
        .corner-bracket.br { bottom: -3px; right: -3px; border-bottom: 2px solid #FB923C; border-right: 2px solid #FB923C; }

        [data-theme="light"] .corner-bracket.tl,
        [data-theme="light"] .corner-bracket.tr,
        [data-theme="light"] .corner-bracket.bl,
        [data-theme="light"] .corner-bracket.br {
            border-color: #d4700a;
        }

        /* ── Constellation SVG lines ── */
        .constellation-line {
            stroke: #475569;
            stroke-width: 0.5;
            stroke-dasharray: 4 4;
            animation: dash 60s linear infinite;
            opacity: 0.5;
        }

        [data-theme="light"] .constellation-line {
            stroke: #a0aec0;
        }

        @keyframes dash {
            to { stroke-dashoffset: 1000; }
        }

        /* ── Text glow for headlines ── */
        .text-glow {
            text-shadow: 0 0 25px rgba(251, 146, 60, 0.4);
        }

        [data-theme="light"] .text-glow {
            text-shadow: 0 0 40px rgba(212, 112, 10, 0.12);
        }

        /* ── Live render pulse ── */
        .live-dot {
            animation: live-pulse 2s ease-in-out infinite;
        }

        @keyframes live-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* ── Reduced motion ── */
        @media (prefers-reduced-motion: reduce) {
            .star, .cross-mark, .star-mark { animation: none !important; }
            .star { opacity: 0.5; }
            .cross-mark { opacity: 0; }
            .star-mark { opacity: 0.7; }
            .live-dot { animation: none !important; opacity: 1; }
            .constellation-line { animation: none !important; }
            [data-motion] { transition: none !important; }
            .dawn-sky, .dawn-sky-warm { transition: none !important; }
            .mystic-card { transition: none !important; }
            .btn-star { transition: none !important; }
            svg[class*="animate-pulse"] { animation: none !important; }
            #starfield-fixed, .geo-circles { transform: none !important; }
        }

        /* ── Landing text utilities ── */
        /* Dark mode (default): light text on dark bg */
        .text-moon { color: #F8FAFC; }
        .text-moon-dim { color: #94A3B8; }
        .text-sunset { color: #FB923C; }
        .text-sunset-dim { color: #9A3412; }
        .border-sunset { border-color: #FB923C; }

        /* Light mode: dark text on cool dawn bg */
        [data-theme="light"] .text-moon { color: #1e293b; }
        [data-theme="light"] .text-moon-dim { color: #5e6d82; }
        [data-theme="light"] .text-sunset { color: #d4700a; }

        /* ── CTA button ── */
        /* Dark mode: light border/text */
        .btn-star {
            border: 1px solid #F8FAFC;
            color: #F8FAFC;
            background: rgba(255, 255, 255, 0.05);
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-size: 0.7rem;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
        }

        .btn-star:hover {
            background: #F8FAFC;
            color: #0f172a;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
        }

        /* Light mode: dark border/text with frost backing */
        [data-theme="light"] .btn-star {
            border-color: #1e293b;
            color: #1e293b;
            background: rgba(255, 255, 255, 0.3);
        }

        [data-theme="light"] .btn-star:hover {
            background: #1e293b;
            color: #f8fafc;
            box-shadow: 0 0 20px rgba(30, 41, 59, 0.15);
        }

        /* ── Decorative geometric circles ── */
        .geo-circles {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            opacity: 0.2;
        }

        .geo-circle {
            position: absolute;
            border-radius: 50%;
            border: 1px solid rgba(203, 213, 225, 0.1);
        }

        .geo-arch {
            position: absolute;
            border-radius: 100% 100% 0 0;
            border-top: 1px solid rgba(251, 146, 60, 0.1);
            border-left: 1px solid rgba(251, 146, 60, 0.1);
            border-right: 1px solid rgba(251, 146, 60, 0.1);
            border-bottom: none;
        }

        [data-theme="light"] .geo-circles {
            opacity: 0.25;
        }

        [data-theme="light"] .geo-circle {
            border-color: rgba(130, 140, 170, 0.12);
        }

        [data-theme="light"] .geo-arch {
            border-top-color: rgba(200, 130, 80, 0.12);
            border-left-color: rgba(200, 130, 80, 0.12);
            border-right-color: rgba(200, 130, 80, 0.12);
        }

        /* ── Landing header transparent variant ── */
        .landing-header {
            background: transparent !important;
            border-color: transparent !important;
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
        }

        .landing-header header {
            background: transparent !important;
            border-color: transparent !important;
        }

        .landing-header a,
        .landing-header button,
        .landing-header span {
            color: #F8FAFC;
        }

        .landing-header a:hover,
        .landing-header button:hover {
            color: #FB923C;
        }

        [data-theme="light"] .landing-header a,
        [data-theme="light"] .landing-header button,
        [data-theme="light"] .landing-header span {
            color: #1e293b;
        }

        [data-theme="light"] .landing-header a:hover,
        [data-theme="light"] .landing-header button:hover {
            color: #d4700a;
        }

        /* ── Section border ── */
        .section-border-top {
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        [data-theme="light"] .section-border-top {
            border-top-color: rgba(120, 100, 80, 0.12);
        }
    """)


def _generate_starfield() -> tuple:
    rng = random.Random(42)
    stars, crosses = [], []

    for i in range(150):
        # responsive: 0-79 always, 80-119 md+, 120-149 lg+
        extra = " hidden lg:block" if i >= 120 else (" hidden md:block" if i >= 80 else "")
        size = rng.random() * 2 + 1
        max_opacity = rng.random() * 0.7 + 0.3
        stars.append(Div(
            cls=f"star{extra}",
            style=(
                f"width:{size:.1f}px;height:{size:.1f}px;"
                f"left:{rng.random() * 100:.1f}%;top:{rng.random() * 100:.1f}%;"
                f"--dur:{rng.random() * 3 + 2:.1f}s;--delay:{rng.random() * 5:.1f}s;"
                f"--max-opacity:{max_opacity:.2f}"
            ),
        ))

    for i in range(28):
        # responsive: 0-11 always, 12-19 md+, 20-27 lg+
        extra = " hidden lg:block" if i >= 20 else (" hidden md:block" if i >= 12 else "")
        crosses.append(Div(
            cls=f"cross-mark{extra}",
            style=(
                f"left:{rng.random() * 100:.1f}%;top:{rng.random() * 100:.1f}%;"
                f"--size:{rng.randint(6, 13)}px;"
                f"--dur:{rng.random() * 6 + 5:.1f}s;--delay:{rng.random() * 10:.1f}s"
            ),
        ))

    return (*stars, *crosses)


def LandingLayout(
    *content,
    header: HeaderConfig | None = None,
    footer: FooterConfig | None = None,
) -> FT:
    header = header or HeaderConfig()
    footer = footer or FooterConfig()

    return Div(
        _landing_styles(),
        # Fixed sky gradient background
        Div(cls="dawn-sky", aria_hidden="true"),
        # Scroll-driven warm overlay (opacity 0→1 as user scrolls)
        Div(
            cls="dawn-sky-warm",
            aria_hidden="true",
            data_scroll="",
            data_style_opacity=scroll.page_progress * 1.5 / 100,
        ),
        # Fixed star field (server-rendered, parallax)
        Div(
            *_generate_starfield(),
            id="starfield-fixed",
            cls="fixed inset-0 pointer-events-none z-[1]",
            aria_hidden="true",
            data_style_transform="translateY(" + scroll.y * -0.05 + "px)",
        ),
        # Decorative geometric circles (parallax)
        Div(
            Div(cls="geo-circle", style="top: 15%; left: 50%; transform: translateX(-50%); width: 800px; height: 800px;"),
            Div(cls="geo-circle", style="top: 15%; left: 50%; transform: translateX(-50%); width: 600px; height: 600px;"),
            Div(cls="geo-arch", style="bottom: 0; left: 50%; transform: translateX(-50%); width: 400px; height: 600px;"),
            cls="geo-circles",
            aria_hidden="true",
            data_style_transform="translateY(" + scroll.y * -0.03 + "px)",
        ),
        # Film grain
        Div(cls="grain-overlay", aria_hidden="true"),
        # Header
        Div(DocsHeader(header), cls="landing-header relative z-50"),
        # Content
        Main(*content, cls="relative z-10"),
        # Footer
        Div(
            DocsFooter(
                attribution=footer.attribution,
                hosting_info=footer.hosting_info,
            ),
            cls="relative z-10",
        ),
        cls="landing-page flex min-h-screen flex-col relative",
    )
