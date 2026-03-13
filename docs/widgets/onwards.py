from starhtml import *


def onwards_card(num: str, title: str, description: str, href: str, button_text: str) -> FT:
    return A(
        Div(
            Span(num, cls="font-mono text-xs tracking-widest text-muted-foreground"),
            H3(title, cls="mt-2 mb-2 text-base font-medium transition-colors group-hover:text-primary"),
            P(description, cls="flex-1 text-sm leading-relaxed text-muted-foreground"),
            Span(button_text, " \u2192", cls="mt-4 inline-block text-sm font-medium text-primary"),
            cls="flex h-full flex-col p-5",
        ),
        href=href,
        cls="block h-full rounded-lg border transition-colors hover:border-primary/30 group",
    )


def onwards_section(*cards: FT) -> FT:
    return Div(
        H2("Onwards", cls="mt-16 mb-8 text-2xl font-semibold tracking-tight"),
        Div(*cards, cls="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-3"),
    )
