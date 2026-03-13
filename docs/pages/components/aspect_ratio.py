TITLE = "Aspect Ratio"
DESCRIPTION = "Displays content within a desired ratio, preventing layout shift."
CATEGORY = "ui"
ORDER = 5
STATUS = "stable"

from starhtml import Div, Img, P, Icon
from components.aspect_ratio import AspectRatio
from components.card import Card, CardHeader, CardTitle, CardDescription
from components.skeleton import Skeleton
from utils import with_code, Prop, build_api_reference, auto_generate_page


@with_code
def default_example():
    return Div(
        AspectRatio(
            Img(
                src="https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&q=80",
                alt="Sunlit valley with winding river between green mountain ridges",
                cls="absolute inset-0 h-full w-full rounded-md object-cover",
            ),
            ratio=16 / 9,
            cls="rounded-md",
        ),
        cls="w-full max-w-xl",
    )


@with_code
def framing_example():
    src = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&q=80"
    ratios = [
        ("YouTube", 16 / 9),
        ("Ultrawide", 21 / 9),
        ("Instagram Post", 1),
        ("Portrait Photo", 3 / 4),
    ]
    return Div(
        *[
            Div(
                AspectRatio(
                    Img(
                        src=src,
                        alt="Mountain lake reframed at different ratios",
                        cls="absolute inset-0 h-full w-full rounded-md object-cover",
                    ),
                    ratio=ratio,
                    cls="rounded-md",
                ),
                P(label, cls="mt-2 text-center text-sm text-muted-foreground"),
            )
            for label, ratio in ratios
        ],
        cls="grid w-full max-w-3xl grid-cols-2 gap-6",
    )


@with_code
def video_embed_example():
    return Div(
        AspectRatio(
            Div(
                Div(
                    Icon("lucide:play", cls="size-8 fill-current"),
                    cls="flex size-16 items-center justify-center rounded-full bg-white/90 text-black shadow-lg",
                ),
                cls="absolute inset-0 flex items-center justify-center rounded-md bg-gradient-to-br from-zinc-900 to-zinc-700",
            ),
            ratio=4 / 3,
            cls="rounded-md",
        ),
        cls="w-full max-w-md",
    )


@with_code
def media_cards_example():
    cards = [
        ("https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=400&q=80", "Architecture", "Modern design patterns"),
        ("https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&q=80", "Culinary Arts", "Seasonal tasting menus"),
        ("https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&q=80", "Technology", "Developer workspaces"),
    ]
    return Div(
        *[
            Card(
                AspectRatio(
                    Img(src=src, alt=title, cls="absolute inset-0 h-full w-full object-cover"),
                    ratio=4 / 3,
                ),
                CardHeader(
                    CardTitle(title, level="h4"),
                    CardDescription(desc),
                ),
                cls="overflow-hidden",
            )
            for src, title, desc in cards
        ],
        cls="grid w-full grid-cols-3 gap-4",
    )


@with_code
def skeleton_example():
    return Div(
        AspectRatio(
            Skeleton(cls="absolute inset-0 rounded-md"),
            ratio=16 / 9,
            cls="rounded-md",
        ),
        cls="w-full max-w-xl",
    )


EXAMPLES_DATA = [
    {"fn": default_example, "title": "Default", "description": "Landscape image constrained to 16:9"},
    {"fn": framing_example, "title": "Content Framing", "description": "Same photo at four ratios shows how cropping changes with each format"},
    {"fn": video_embed_example, "title": "Video Embed", "description": "Non-image content in a 4:3 container. AspectRatio works with any children, not just images"},
    {"fn": media_cards_example, "title": "Media Card Grid", "description": "Three source images with different native proportions, all normalized to 4:3 by AspectRatio", "preview_class": "[&>*]:w-full [&>*]:max-w-3xl"},
    {"fn": skeleton_example, "title": "Loading Placeholder", "description": "AspectRatio + Skeleton prevents layout shift while media loads"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("ratio", "float", "Width-to-height ratio (e.g. 16/9, 4/3, 1)", "16 / 9"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def create_aspect_ratio_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
