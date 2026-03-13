from starhtml import *
from starhtml.plugins import in_view, press
from components.code_block import CodeBlock as StarlighterCode
from components.button import Button as StarButton
from components.card import (
    Card as StarCard, CardHeader, CardTitle, CardDescription, CardContent,
)
from components.input import Input as StarInput
from components.label import Label as StarLabel
from components.switch import Switch as StarSwitch
from components.tabs import Tabs, TabsList, TabsTrigger, TabsContent
from components.command import (
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
        P("APERTURE", cls="font-mono text-[9px] font-medium tracking-[0.25em] text-[#94A3B8] uppercase showcase-card-title", style="font-family: 'Inter', sans-serif;"),
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
                    cls="inline-block h-1 w-1 rounded-full transition-colors duration-300",
                    data_style_background_color=active.if_("var(--indicator-active)", "var(--indicator-dim)"),
                ),
                Span(data_text=active.if_("ACTIVE", "DIM")),
                cls="inline-flex items-center gap-1.5 rounded-sm border px-1.5 py-0.5 font-mono text-[9px] font-medium tracking-[0.08em] uppercase transition-all duration-300",
                data_style_color=active.if_("var(--indicator-active)", "var(--indicator-dim)"),
                data_style_border_color=active.if_("var(--indicator-active-border)", "var(--indicator-dim-border)"),
                data_style_background_color=active.if_("var(--indicator-active-bg)", "var(--indicator-dim-bg)"),
            ),
            Span(
                data_text="" + aperture + "%",
                cls="font-mono text-[11px] tabular-nums transition-colors duration-300",
                data_style_color=active.if_("var(--indicator-active)", "var(--indicator-dim)"),
            ),
            cls="mt-1 flex items-center justify-between",
        ),
        # Warms card as aperture rises
        Div(
            cls="pointer-events-none absolute inset-0 rounded-[inherit] transition-opacity duration-300 aperture-glow",
            data_style_opacity=aperture / 100,
        ),
        # Light mode only — desaturates at low aperture
        Div(
            cls="pointer-events-none absolute inset-0 rounded-[inherit] transition-opacity duration-500 aperture-cool",
            data_style_opacity=1 - aperture / 100,
        ),
        Div(cls="showcase-pulse-ring"),
        # Sweep aperture from 50 to 90
        Div(data_init=(aperture.set(90), dict(delay="1400ms"))),
        cls="px-4 py-2 select-none showcase-card",
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
                            cls="mt-6 block font-normal hero-subline text-sunset",
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
                        cls="mt-5 text-xl font-light italic md:mt-[55px] md:text-2xl font-serif-body text-moon-dim",
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
                            cls="rounded-none focus-visible:ring-2 focus-visible:ring-[#FB923C] focus-visible:ring-offset-2 focus-visible:outline-none btn-star",
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
                            Span("Quickstart", cls="mb-2 block font-mono text-[11px] font-semibold tracking-[0.25em] uppercase text-sunset"),
                            Div(cls="h-px w-full bg-current opacity-40 showcase-divider-line text-sunset"),
                            cls="showcase-label mb-4",
                        ),
                        Div(
                            Div(
                                *[P(Span("$", cls="text-[#FB923C]"), f" {cmd}", cls="text-[#94A3B8]")
                              for cmd in ("pip install starui", "star init", "star add button")],
                                cls="space-y-2 p-6 font-mono text-sm terminal-window",
                            ),
                            _component_showcase(),
                            cls="showcase-terminal-group",
                        ),
                        cls="showcase-float-wrapper relative",
                    ),
                    cls="flex flex-col hero-right-col",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=400, spring="gentle"),
                ),
                cls="relative z-10 grid grid-cols-1 gap-5 hero-grid-phi",
            ),
            cls="mx-auto w-full max-w-7xl px-6 lg:px-8",
        ),
        Div(
            Svg(
                SvgPath(d="M6 9l6 6 6-6", fill="none", stroke="currentColor", stroke_width="1.5", stroke_linecap="round", stroke_linejoin="round"),
                viewBox="0 0 24 24",
                cls="h-5 w-5",
            ),
            cls="absolute bottom-8 left-1/2 z-20 -translate-x-1/2 scroll-hint text-moon-dim",
            aria_hidden="true",
        ),
        cls="relative flex min-h-[90vh] items-center overflow-x-clip pt-16 pb-[89px] md:pt-20 lg:pt-24 hero-section-mobile",
        aria_label="Welcome to StarUI",
    )


# ── Code Example section ────────────────────────────────────────────


def code_example_section() -> FT:
    example_code = '''from starhtml import *
from components.ui.card import (
    Card, CardHeader, CardTitle,
    CardDescription, CardContent,
)
from components.ui.input import Input

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
                Span("FIG. 01", cls="mb-3 block font-mono text-[10px] tracking-widest text-sunset", aria_hidden="true"),
                H2(
                    "Write Python. Get reactivity.",
                    cls="mt-2 text-3xl italic md:text-4xl font-display text-moon",
                ),
                cls="mb-12",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            Div(
                Div(
                    Div(
                        Div(
                            Span(cls="h-2.5 w-2.5 rounded-full bg-[#ff5f57]"),
                            Span(cls="h-2.5 w-2.5 rounded-full bg-[#febc2e]"),
                            Span(cls="h-2.5 w-2.5 rounded-full bg-[#28c840]"),
                            cls="flex gap-1.5",
                        ),
                        Span("app.py", cls="font-mono text-[11px] mini-text-dim"),
                        Div(cls="w-[52px]"),
                        cls="flex items-center justify-between border-b px-4 py-2.5 mini-border",
                    ),
                    StarlighterCode(example_code, "python", cls="!rounded-none !border-none !bg-transparent !shadow-none"),
                    cls="overflow-hidden rounded-xl md:col-span-5 mystic-card editor-panel",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=100, spring="gentle"),
                ),
                Div(
                    name,
                    Div(
                        P(data_text=greeting, cls="text-lg font-medium mini-text"),
                        P("Update your profile", cls="mt-1 mb-6 text-xs mini-text-dim"),
                        Div(
                            P("Name", cls="mb-1.5 text-xs font-medium mini-text"),
                            Input(
                                placeholder="Your name",
                                data_bind=name,
                                cls="w-full rounded-md border bg-transparent px-3 py-2 text-sm transition-colors outline-none mini-border mini-text fig01-input",
                            ),
                        ),
                        cls="w-full max-w-sm rounded-xl p-6 shadow-xl mini-surface",
                    ),
                    cls="relative flex min-h-[400px] items-center justify-center rounded-xl p-8 md:col-span-7 md:p-12 showcase-preview",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=200, spring="gentle"),
                ),
                cls="grid grid-cols-1 gap-6 md:grid-cols-12",
            ),
            cls="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8",
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
                    cls="mb-4 grid gap-2",
                ),
                Div(
                    Div(cls="h-px flex-1 bg-border"),
                    Span("Or continue with", cls="px-2 text-[10px] whitespace-nowrap text-muted-foreground uppercase"),
                    Div(cls="h-px flex-1 bg-border"),
                    cls="mb-4 flex items-center",
                ),
                Div(
                    StarLabel("Email"),
                    StarInput(type="email", placeholder="m@example.com", signal=email),
                    cls="mb-3 space-y-1.5",
                ),
                Div(
                    StarLabel("Password"),
                    StarInput(type="password", placeholder="Enter password"),
                    cls="mb-4 space-y-1.5",
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
            Div(cls="my-3 h-px bg-border"),
            Div(
                Span("Active", cls="rounded-full bg-[#FB923C] px-2.5 py-0.5 text-[11px] font-medium text-white"),
                Span("Beta", cls="rounded-full border px-2.5 py-0.5 text-[11px] font-medium text-muted-foreground"),
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
                        cls="mt-2 text-sm leading-relaxed text-muted-foreground",
                    ),
                    Div(
                        StarButton("Cancel", variant="outline"),
                        StarButton("Continue", data_on_click=confirmed.set(True)),
                        cls="mt-6 flex justify-end gap-3",
                    ),
                    data_show=~confirmed,
                ),
                Div(
                    Div(
                        Icon("lucide:check-circle", width="24", height="24", cls="text-[#4ade80]"),
                        cls="mb-3",
                    ),
                    H2("Account deleted.", cls="text-base font-medium"),
                    P("Your data has been permanently removed.", cls="mt-1 text-sm text-muted-foreground"),
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
                    P("Make changes to your account here.", cls="mb-4 text-sm text-muted-foreground"),
                    Div(
                        StarLabel("Name"),
                        StarInput(value="Pedro Duarte"),
                        cls="mb-3 space-y-1.5",
                    ),
                    Div(
                        StarLabel("Username"),
                        StarInput(value="@peduarte"),
                        cls="mb-5 space-y-1.5",
                    ),
                    StarButton("Save changes"),
                    id="account",
                ),
                TabsContent(
                    P("Change your password here.", cls="mb-4 text-sm text-muted-foreground"),
                    Div(
                        StarLabel("Current password"),
                        StarInput(type="password"),
                        cls="mb-3 space-y-1.5",
                    ),
                    Div(
                        StarLabel("New password"),
                        StarInput(type="password"),
                        cls="mb-5 space-y-1.5",
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
                cls="mb-5 flex flex-wrap items-center gap-3",
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
                Span("FIG. 03", cls="mb-3 block font-mono text-[10px] tracking-widest text-sunset", aria_hidden="true"),
                Div(
                    Div(
                        H2("The Constellation", cls="font-display text-4xl italic text-moon"),
                        P("34+ components built with Tailwind v4.", cls="mt-2 text-lg italic font-serif-body text-moon-dim"),
                    ),
                    A(
                        "View All Components →",
                        href="/components",
                        cls="hidden shrink-0 font-mono text-sm tracking-wide uppercase transition-colors hover:text-[#FB923C] md:block text-sunset",
                    ),
                    cls="flex flex-col gap-4 md:flex-row md:items-end md:justify-between",
                ),
                cls="mb-12",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            Div(
                active,
                Div(
                    Span("COMPONENTS", cls="block px-3 py-2 font-mono text-[10px] tracking-widest text-sunset"),
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
                            cls="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2.5 transition-colors",
                        )
                        for name, slug, icon, _ in explorer_items
                    ],
                    role="tablist",
                    aria_label="Component list",
                    cls="flex flex-row gap-1 overflow-x-auto rounded-xl p-3 md:col-span-3 md:flex-col md:overflow-visible mystic-card",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=100, spring="gentle"),
                ),
                Div(
                    *[
                        Div(
                            fn(),
                            data_show=active == slug,
                            cls="flex w-full items-center justify-center",
                        )
                        for _, slug, _, fn in explorer_items
                    ],
                    Div(
                        Code(
                            "star add command",
                            data_text="star add " + active,
                            cls="font-mono text-[10px] text-moon-dim",
                        ),
                        cls="absolute right-6 bottom-4",
                    ),
                    role="tabpanel",
                    aria_label="Component preview",
                    cls="relative flex min-h-[450px] items-center justify-center rounded-xl p-8 md:col-span-9 md:p-12 showcase-preview",
                    data_motion=in_view(y=20, opacity=0, duration=500, delay=200, spring="gentle"),
                ),
                cls="grid grid-cols-1 gap-6 md:grid-cols-12",
            ),
            Div(
                A(
                    "View All Components →",
                    href="/components",
                    cls="font-mono text-sm tracking-wide uppercase transition-colors hover:text-[#FB923C] text-sunset",
                ),
                cls="mt-8 text-center md:hidden",
            ),
            cls="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8",
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
                Span("FIG. 02", cls="mb-4 block font-mono text-[10px] tracking-widest text-sunset", aria_hidden="true"),
                H3(
                    "First Principles",
                    cls="mb-6 text-3xl italic font-display text-moon",
                ),
                P(
                    "The shadcn/ui model, rebuilt for Python. A component library that stays out of your way \u2014 do it all without leaving Python.",
                    cls="font-serif-body text-xl text-moon-dim leading-relaxed",
                ),
                Icon(
                    "simple-icons:python",
                    width="220",
                    height="220",
                    cls="pointer-events-none absolute -right-4 -bottom-8 rotate-12 python-watermark text-sunset",
                    aria_hidden="true",
                ),
                cls="relative overflow-visible md:w-1/3 md:pr-8 why-starui-left",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            Div(
                *[
                    Div(
                        Div(
                            Span(num, cls="font-mono text-sm font-semibold text-sunset"),
                            H4(
                                title,
                                cls="text-lg font-light tracking-[0.15em] uppercase transition-colors text-moon group-hover:text-sunset",
                            ),
                            cls="mb-2 flex items-baseline gap-4",
                        ),
                        P(
                            desc,
                            cls="py-2 pl-10 leading-relaxed text-moon-dim principle-accent",
                        ),
                        cls="group cursor-default principle-row",
                        data_motion=in_view(y=20, opacity=0, duration=500, delay=i * 100, spring="gentle"),
                    )
                    for i, (num, title, desc) in enumerate(principles)
                ],
                cls="grid grid-cols-1 gap-12 md:w-2/3",
            ),
            cls="mx-auto flex max-w-5xl flex-col gap-16 px-4 sm:px-6 md:flex-row lg:px-8",
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
                    cls="mx-auto mb-10 h-10 w-10 star-mark text-sunset",
                    aria_hidden="true",
                ),
                H2(
                    "The observatory",
                    Br(),
                    Span("is "),
                    Span("open.", cls="italic text-sunset"),
                    cls="text-5xl leading-[0.95] tracking-[-0.02em] md:text-6xl lg:text-7xl font-display text-moon",
                ),
                P(
                    "Start building with components you actually own.",
                    cls="mx-auto mt-8 max-w-xl text-xl font-light italic md:text-2xl font-serif-body text-moon-dim",
                ),
                Div(
                    A(
                        "Get Started",
                        href="/installation",
                        cls="rounded-none focus-visible:ring-2 focus-visible:ring-[#FB923C] focus-visible:ring-offset-2 focus-visible:outline-none btn-star",
                        data_motion=press(scale=0.97, duration=100),
                    ),
                    A(
                        "View Components",
                        href="/components",
                        cls="rounded-none focus-visible:ring-2 focus-visible:ring-[#FB923C] focus-visible:ring-offset-2 focus-visible:outline-none btn-star-outline",
                        data_motion=press(scale=0.97, duration=100),
                    ),
                    cls="mt-12 flex flex-wrap items-center justify-center gap-4",
                ),
                cls="text-center",
                data_motion=in_view(y=20, opacity=0, duration=500, spring="gentle"),
            ),
            cls="mx-auto max-w-7xl px-4 py-24 sm:px-6 md:py-32 lg:px-8",
        ),
        cls="relative z-10 section-border-top cta-section",
        aria_label="Get started with StarUI",
    )


def footer_section() -> FT:
    return Footer(
        Div(
            P(
                "\u00a9 2026 StarUI. Open Source Apache 2.0.",
                cls="text-center text-xs tracking-[0.2em] uppercase text-moon-dim",
            ),
            cls="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8",
        ),
        cls="relative z-10 section-border-top footer-section",
    )
