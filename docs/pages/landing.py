from starhtml import *
from starhtml.plugins import in_view, press
from starui.registry.components.code_block import CodeBlock as StarlighterCode
from starui.registry.components.button import Button as StarButton
from starui.registry.components.card import (
    Card as StarCard, CardHeader, CardTitle, CardDescription, CardContent,
)
from starui.registry.components.input import Input as StarInput
from starui.registry.components.label import Label as StarLabel
from starui.registry.components.switch import Switch as StarSwitch
from starui.registry.components.tabs import Tabs, TabsList, TabsTrigger, TabsContent
from starui.registry.components.command import (
    Command, CommandInput, CommandList, CommandGroup,
    CommandItem, CommandEmpty, CommandSeparator, CommandShortcut,
)


# ── Hero section ────────────────────────────────────────────────────



def _component_showcase() -> FT:
    aperture = Signal("aperture", 50)
    active = aperture > 50

    return Div(
        aperture,
        Div(cls="showcase-flash"),
        P("APERTURE", cls="text-[9px] font-mono font-medium tracking-[0.25em] uppercase text-[#94A3B8] showcase-card-title", style="font-family: 'Inter', sans-serif;"),
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
        # CSS custom properties for theme-aware colors
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
        # Warms card as aperture rises
        Div(
            cls="aperture-glow absolute inset-0 rounded-[inherit] pointer-events-none transition-opacity duration-300",
            data_style_opacity=aperture / 100,
        ),
        # Light mode only — desaturates at low aperture
        Div(
            cls="aperture-cool absolute inset-0 rounded-[inherit] pointer-events-none transition-opacity duration-500",
            data_style_opacity=1 - aperture / 100,
        ),
        Div(cls="showcase-pulse-ring"),
        # Sweep aperture from 50 to 90
        Div(data_init=(aperture.set(90), dict(delay="1400ms"))),
        cls="showcase-card px-4 py-2 select-none",
    )


def hero_section() -> FT:
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
        Svg(
            Defs(
                LinearGradient(
                    Stop(offset="0%", stop_color="#FB923C", stop_opacity="0"),
                    Stop(offset="12%", stop_color="#FB923C", stop_opacity="0.12"),
                    Stop(offset="88%", stop_color="#FB923C", stop_opacity="0.12"),
                    Stop(offset="100%", stop_color="#FB923C", stop_opacity="0"),
                    id="arc-fade", gradientUnits="userSpaceOnUse",
                    x1="60", y1="260", x2="1040", y2="520",
                ),
            ),
            SvgPath(d=arc_path, fill="none", stroke="url(#arc-fade)", cls="arc-line"),
            G(
                G(
                    SvgPath(
                        d="M0 -10 L3 -3 L10 0 L3 3 L0 10 L-3 3 L-10 0 L-3 -3 Z",
                        cls="arc-star-halo", opacity="0",
                    ),
                    Animate(
                        attributeName="opacity",
                        values="0;0;0.85;0;0", keyTimes="0;0.25;0.5;0.75;1",
                        dur=arc_dur, begin=arc_begin, fill="freeze",
                        calcMode="spline",
                        keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1",
                    ),
                ),
                SvgPath(
                    d="M0 -10 L3 -3 L10 0 L3 3 L0 10 L-3 3 L-10 0 L-3 -3 Z",
                    cls="arc-star",
                ),
                AnimateMotion(
                    path=arc_path, dur=arc_dur, begin=arc_begin, fill="freeze",
                    calcMode="spline", keySplines="0.25 0.1 0.25 1", keyTimes="0;1",
                ),
                Animate(
                    attributeName="opacity",
                    values="0;1;1;0", keyTimes="0;0.05;0.92;1",
                    dur=arc_dur, begin=arc_begin, fill="freeze",
                ),
                AnimateTransform(
                    attributeName="transform", type="rotate",
                    **{"from": "0 0 0"}, to="180 0 0",
                    dur=arc_dur, begin=arc_begin, fill="freeze",
                    calcMode="spline", keySplines="0.42 0 0.58 1", keyTimes="0;1",
                    additive="sum",
                ),
                AnimateTransform(
                    attributeName="transform", type="scale",
                    values="0.4;1.3;0.4", keyTimes="0;0.5;1",
                    dur=arc_dur, begin=arc_begin, fill="freeze",
                    calcMode="spline", keySplines="0.42 0 0.58 1;0.42 0 0.58 1",
                    additive="sum",
                ),
                cls="arc-star-group", opacity="0",
            ),
            viewBox="0 0 1100 680",
            cls="hero-arc",
            aria_hidden="true",
        ),
        Div(
            Div(
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
                        style="opacity: 0.85;",
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
                Div(
                    Div(
                        Div(
                            Span("Quickstart", cls="text-[11px] font-mono font-semibold tracking-[0.25em] uppercase text-sunset block mb-2"),
                            Div(cls="showcase-divider-line w-full h-px bg-current text-sunset opacity-40"),
                            cls="showcase-label mb-4",
                        ),
                        Div(
                            Div(
                                *[P(Span("$", cls="text-[#FB923C]"), f" {cmd}", cls="text-[#94A3B8]")
                              for cmd in ("pip install starui", "star init", "star add button")],
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
        Div(
            Svg(
                SvgPath(d="M6 9l6 6 6-6", fill="none", stroke="currentColor", stroke_width="1.5", stroke_linecap="round", stroke_linejoin="round"),
                viewBox="0 0 24 24",
                cls="w-5 h-5",
            ),
            cls="scroll-hint absolute bottom-8 left-1/2 -translate-x-1/2 text-moon-dim z-20",
            aria_hidden="true",
        ),
        cls="hero-section-mobile relative min-h-[90vh] flex items-center pb-[89px] pt-16 md:pt-20 lg:pt-24 overflow-x-clip",
        aria_label="Welcome to StarUI",
    )


# ── Code Example section ────────────────────────────────────────────


def code_example_section() -> FT:
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

    name = Signal("hero_name", "friend")
    greeting = name.if_("Hello, " + name, "Hello, stranger")

    return Section(
        Div(
            Div(
                Span("FIG. 01", cls="text-[10px] tracking-widest text-sunset font-mono block mb-3", aria_hidden="true"),
                H2(
                    "Write Python. Get reactivity.",
                    cls="font-display text-3xl md:text-4xl italic text-moon mt-2",
                ),
                cls="mb-12",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            Div(
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
                Div(
                    name,
                    Div(
                        P(data_text=greeting, cls="text-lg font-medium mini-text"),
                        P("Update your profile", cls="text-xs mini-text-dim mt-1 mb-6"),
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
        aria_label="Code example",
    )


# ── Component explorer previews (real StarUI registry components) ──


def _explorer_command() -> FT:
    return Command(
        CommandInput(placeholder="Type a command or search..."),
        CommandList(
            CommandGroup(
                CommandItem(
                    Icon("lucide:calendar", width="15", height="15"),
                    "Calendar",
                    value="calendar",
                ),
                CommandItem(
                    Icon("lucide:smile", width="15", height="15"),
                    "Search Emoji",
                    value="search-emoji",
                    keywords="emoji",
                ),
                CommandItem(
                    Icon("lucide:calculator", width="15", height="15"),
                    "Calculator",
                    value="calculator",
                ),
                heading="Suggestions",
            ),
            CommandSeparator(),
            CommandGroup(
                CommandItem(
                    Icon("lucide:user", width="15", height="15"),
                    "Profile",
                    CommandShortcut("\u2318P"),
                    value="profile",
                ),
                CommandItem(
                    Icon("lucide:credit-card", width="15", height="15"),
                    "Billing",
                    CommandShortcut("\u2318B"),
                    value="billing",
                ),
                heading="Settings",
            ),
            CommandEmpty(),
        ),
        signal="cmd_explorer",
        cls="w-full max-w-md shadow-xl",
    )


def _explorer_card() -> FT:
    email = Signal("exp_email", "")

    return Div(
        email,
        StarCard(
            CardHeader(
                CardTitle("Create account"),
                CardDescription("Enter your email below to create your account"),
            ),
            CardContent(
                Div(
                    StarButton(
                        Icon("simple-icons:github", width="14", height="14"),
                        "Github",
                        variant="outline",
                        cls="w-full",
                    ),
                    StarButton(
                        Icon("simple-icons:google", width="14", height="14"),
                        "Google",
                        variant="outline",
                        cls="w-full",
                    ),
                    cls="grid gap-2 mb-4",
                ),
                Div(
                    Div(cls="flex-1 h-px bg-border"),
                    Span("Or continue with", cls="text-[10px] text-muted-foreground uppercase px-2 whitespace-nowrap"),
                    Div(cls="flex-1 h-px bg-border"),
                    cls="flex items-center mb-4",
                ),
                Div(
                    StarLabel("Email"),
                    StarInput(type="email", placeholder="m@example.com", signal=email),
                    cls="space-y-1.5 mb-3",
                ),
                Div(
                    StarLabel("Password"),
                    StarInput(type="password", placeholder="Enter password"),
                    cls="space-y-1.5 mb-4",
                ),
                StarButton("Create Account", cls="w-full"),
            ),
            cls="w-full max-w-sm shadow-xl",
        ),
    )


def _explorer_switch() -> FT:
    def _toggle_row(label_text: str, sig: str, checked: bool = False) -> FT:
        return Div(
            StarLabel(label_text, cls="cursor-pointer"),
            StarSwitch(signal=sig, checked=checked),
            cls="flex items-center justify-between",
        )

    return StarCard(
        CardContent(
            Div(
                _toggle_row("Airplane Mode", "sw_airplane", True),
                _toggle_row("Notifications", "sw_notifs"),
                _toggle_row("Dark Mode", "sw_dark", True),
                cls="space-y-4",
            ),
            Div(cls="h-px bg-border my-3"),
            Div(
                Span("Active", cls="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-[#FB923C] text-white"),
                Span("Beta", cls="px-2.5 py-0.5 rounded-full text-[11px] font-medium border text-muted-foreground"),
                cls="flex gap-2",
            ),
        ),
        cls="w-full max-w-xs shadow-xl",
    )


def _explorer_dialog() -> FT:
    confirmed = Signal("exp_confirmed", False)

    return Div(
        confirmed,
        StarCard(
            CardContent(
                Div(
                    H2("Are you absolutely sure?", cls="text-base font-medium"),
                    P(
                        "This action cannot be undone. This will permanently delete your account and remove your data from our servers.",
                        cls="text-sm text-muted-foreground mt-2 leading-relaxed",
                    ),
                    Div(
                        StarButton("Cancel", variant="outline"),
                        StarButton("Continue", data_on_click=confirmed.set(True)),
                        cls="flex justify-end gap-3 mt-6",
                    ),
                    data_show=~confirmed,
                ),
                Div(
                    Div(
                        Icon("lucide:check-circle", width="24", height="24", cls="text-[#4ade80]"),
                        cls="mb-3",
                    ),
                    H2("Account deleted.", cls="text-base font-medium"),
                    P("Your data has been permanently removed.", cls="text-sm text-muted-foreground mt-1"),
                    StarButton("Done", variant="outline", data_on_click=confirmed.set(False), cls="mt-4"),
                    data_show=confirmed,
                ),
            ),
            cls="w-full max-w-md shadow-xl",
        ),
    )


def _explorer_tabs() -> FT:
    return StarCard(
        CardContent(
            Tabs(
                TabsList(
                    TabsTrigger("Account", id="account"),
                    TabsTrigger("Password", id="password"),
                ),
                TabsContent(
                    P("Make changes to your account here.", cls="text-sm text-muted-foreground mb-4"),
                    Div(
                        StarLabel("Name"),
                        StarInput(value="Pedro Duarte"),
                        cls="space-y-1.5 mb-3",
                    ),
                    Div(
                        StarLabel("Username"),
                        StarInput(value="@peduarte"),
                        cls="space-y-1.5 mb-5",
                    ),
                    StarButton("Save changes"),
                    id="account",
                ),
                TabsContent(
                    P("Change your password here.", cls="text-sm text-muted-foreground mb-4"),
                    Div(
                        StarLabel("Current password"),
                        StarInput(type="password"),
                        cls="space-y-1.5 mb-3",
                    ),
                    Div(
                        StarLabel("New password"),
                        StarInput(type="password"),
                        cls="space-y-1.5 mb-5",
                    ),
                    StarButton("Save password"),
                    id="password",
                ),
                value="account",
                signal="exp_tab",
            ),
        ),
        cls="w-full max-w-sm shadow-xl",
    )


def _explorer_button() -> FT:
    return StarCard(
        CardContent(
            Div(
                StarButton("Primary"),
                StarButton("Secondary", variant="secondary"),
                StarButton("Outline", variant="outline"),
                cls="flex flex-wrap items-center gap-3 mb-5",
            ),
            Div(
                StarButton("Destructive", variant="destructive"),
                StarButton("Ghost", variant="ghost", cls="text-muted-foreground"),
                StarButton("Link", variant="link"),
                cls="flex flex-wrap items-center gap-3",
            ),
        ),
        cls="max-w-md shadow-xl",
    )


# ── Component Explorer section ────────────────────────────────────


def component_grid_section() -> FT:
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
            Div(
                Span("FIG. 03", cls="text-[10px] tracking-widest text-sunset font-mono block mb-3", aria_hidden="true"),
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
            Div(
                active,
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
                            role="tab",
                            tabindex="0",
                            data_attr_aria_selected=(active == slug).if_("true", "false"),
                            cls="flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer transition-colors",
                        )
                        for name, slug, icon, _ in explorer_items
                    ],
                    role="tablist",
                    aria_label="Component list",
                    cls="md:col-span-3 mystic-card rounded-xl p-3 flex flex-row md:flex-col gap-1 overflow-x-auto md:overflow-visible",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=100, spring="gentle"),
                ),
                Div(
                    *[
                        Div(
                            fn(),
                            data_show=active == slug,
                            cls="flex items-center justify-center w-full",
                        )
                        for _, slug, _, fn in explorer_items
                    ],
                    Div(
                        Code(
                            "star add command",
                            data_text="star add " + active,
                            cls="text-[10px] font-mono text-moon-dim",
                        ),
                        cls="absolute bottom-4 right-6",
                    ),
                    role="tabpanel",
                    aria_label="Component preview",
                    cls="md:col-span-9 showcase-preview rounded-xl p-8 md:p-12 relative min-h-[450px] flex items-center justify-center",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=200, spring="gentle"),
                ),
                cls="grid grid-cols-1 md:grid-cols-12 gap-6",
            ),
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
        cls="relative z-10 py-24 section-border-top constellation-section",
        aria_label="Component explorer",
    )


# ── Why StarUI section ─────────────────────────────────────────────


def why_starui_section() -> FT:
    principles = [
        ("01", "Own The Code", "star add button \u2014 that\u2019s it. The CLI copies the source into your project. Read it, modify it, make it yours."),
        ("02", "Server-First", "The server is the source of truth. Signals handle the rest \u2014 a modal open state, a form validation, a toggle. Client-side state only where you actually need it."),
        ("03", "Tailwind v4", "The star CLI downloads the Tailwind binary, runs watch mode, and handles minification. No Node. No npm. The entire CSS toolchain is one Python command."),
    ]

    return Section(
        Div(
            Div(
                Span("FIG. 02", cls="text-[10px] tracking-widest text-sunset font-mono block mb-4", aria_hidden="true"),
                H3(
                    "First Principles",
                    cls="font-display text-3xl mb-6 italic text-moon",
                ),
                P(
                    "The shadcn/ui model, rebuilt for Python. A component library that stays out of your way \u2014 do it all without leaving Python.",
                    cls="font-serif-body text-xl text-moon-dim leading-relaxed",
                ),
                Icon(
                    "simple-icons:python",
                    width="220",
                    height="220",
                    cls="python-watermark absolute -bottom-8 -right-4 rotate-12 text-sunset pointer-events-none",
                    aria_hidden="true",
                ),
                cls="md:w-1/3 why-starui-left md:pr-8 relative overflow-visible",
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
                            cls="pl-10 text-moon-dim leading-relaxed principle-accent py-2",
                        ),
                        cls="group cursor-default principle-row",
                        data_motion=in_view(y=20, opacity=0, duration=500, delay=i * 100, spring="gentle"),
                    )
                    for i, (num, title, desc) in enumerate(principles)
                ],
                cls="md:w-2/3 grid grid-cols-1 gap-12",
            ),
            cls="max-w-5xl mx-auto flex flex-col md:flex-row gap-16 px-4 sm:px-6 lg:px-8",
        ),
        cls="relative z-10 py-24 section-border-top why-starui-section",
        aria_label="Why StarUI",
    )


# ── Final CTA ───────────────────────────────────────────────────────


def cta_section() -> FT:
    return Section(
        Div(
            Div(
                Svg(
                    SvgPath(
                        d="M12 2L14 10L22 12L14 14L12 22L10 14L2 12L10 10Z",
                        fill="currentColor",
                    ),
                    viewBox="0 0 24 24",
                    cls="star-mark w-10 h-10 mx-auto text-sunset mb-10",
                    aria_hidden="true",
                ),
                H2(
                    "The observatory",
                    Br(),
                    Span("is "),
                    Span("open.", cls="italic text-sunset"),
                    cls="font-display text-5xl md:text-6xl lg:text-7xl text-moon leading-[0.95] tracking-[-0.02em]",
                ),
                P(
                    "Start building with components you actually own.",
                    cls="font-serif-body text-xl md:text-2xl text-moon-dim italic font-light mt-8 max-w-xl mx-auto",
                ),
                Div(
                    A(
                        "Get Started",
                        href="/installation",
                        cls="btn-star rounded-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[#FB923C]",
                        data_motion=press(scale=0.97, duration=100),
                    ),
                    A(
                        "View Components",
                        href="/components",
                        cls="btn-star-outline rounded-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[#FB923C]",
                        data_motion=press(scale=0.97, duration=100),
                    ),
                    cls="flex flex-wrap items-center justify-center gap-4 mt-12",
                ),
                cls="text-center",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32",
        ),
        cls="relative z-10 section-border-top cta-section",
        aria_label="Get started with StarUI",
    )


def footer_section() -> FT:
    return Footer(
        Div(
            P(
                "\u00a9 2026 StarUI. Open Source Apache 2.0.",
                cls="text-xs uppercase tracking-[0.2em] text-moon-dim text-center",
            ),
            cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
        ),
        cls="relative z-10 section-border-top footer-section",
    )
