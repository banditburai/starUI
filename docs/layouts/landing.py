import random

from starhtml import *
from starhtml.plugins import scroll
from layouts.header import DocsHeader
from layouts.base import HeaderConfig


def _generate_starfield() -> tuple:
    rng = random.Random(42)
    stars, crosses = [], []

    for i in range(90):
        extra = " hidden lg:block" if i >= 80 else (" hidden md:block" if i >= 55 else "")
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

    for i in range(30):
        extra = " hidden lg:block" if i >= 25 else (" hidden md:block" if i >= 15 else "")
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
) -> FT:
    header = header or HeaderConfig()

    return Div(
        Div(cls="dawn-sky", aria_hidden="true"),
        Div(
            cls="dawn-sky-warm",
            aria_hidden="true",
            data_scroll="",
            data_style_opacity=scroll.page_progress * 1.5 / 100,
        ),
        Div(
            *_generate_starfield(),
            id="starfield-fixed",
            cls="fixed inset-0 pointer-events-none z-[1]",
            aria_hidden="true",
            data_style_transform="translateY(" + scroll.y * -0.05 + "px)",
            data_style_opacity="$aperture / 100",
        ),
        Div(cls="grain-overlay", aria_hidden="true"),
        Div(DocsHeader(header), cls="landing-header relative z-50"),
        Main(*content, cls="relative z-10"),
        cls="landing-page flex min-h-screen flex-col relative",
    )
