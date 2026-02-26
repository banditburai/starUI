"""
Toggle component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Toggle"
DESCRIPTION = "A two-state button that can be either on or off."
CATEGORY = "ui"
ORDER = 80
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H3, Signal, js, collect
from starui.registry.components.toggle import Toggle
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.separator import Separator
from starui.registry.components.progress import Progress
from utils import auto_generate_page, with_code, Prop, build_api_reference


@with_code
def basic_toggle_example():
    return Div(
        (bold_toggle := Signal("bold_toggle", False)),
        Toggle(
            Icon("lucide:bold", cls="h-4 w-4"),
            variant="outline",
            signal=bold_toggle
        ),
        P(
            "Bold is ",
            Span(data_text=bold_toggle.if_("ON", "OFF"), cls="font-mono"),
            cls="text-sm text-muted-foreground mt-2"
        ),
        cls="flex flex-col items-center"
    )


@with_code
def feature_toggles_example():
    experimental = Signal("experimental", False)
    debug = Signal("debug", False)
    performance = Signal("performance", True)

    active_features = collect([
        (experimental, "Experimental"),
        (debug, "Debug"),
        (performance, "Performance")
    ], join_with=" • ")

    def create_feature_toggle(icon, color_class, title, description, sig, pressed=False):
        return Div(
            Toggle(
                Icon(icon, cls="h-4 w-4 mr-2", data_class=sig.if_(color_class)),
                Span(title),
                variant="outline",
                signal=sig,
                pressed=pressed
            ),
            P(description, cls="text-sm text-muted-foreground mt-1"),
            cls="space-y-1"
        )
    return Card(
        CardHeader(
            CardTitle("Feature Flags"),
            CardDescription("Enable experimental features")
        ),
        CardContent(
            Div(
                experimental, debug, performance,
                create_feature_toggle("lucide:flask-conical", "text-orange-500", "Experimental Mode", "Enable beta features", experimental),
                create_feature_toggle("lucide:bug", "text-red-500", "Debug Mode", "Show debug information", debug),
                create_feature_toggle("lucide:zap", "text-yellow-500", "Performance Mode", "Optimize for speed", performance, pressed=True),
                Separator(cls="my-4"),
                Div(
                    Badge(
                        data_text=active_features.if_(active_features, "Standard Mode"),
                        variant="secondary",
                        cls="w-full justify-center min-w-[200px]"
                    ),
                    cls="text-center"
                ),
                cls="space-y-3"
            )
        ),
        cls="w-80"
    )


@with_code
def size_variations_example():
    return Div(
        Div(
            H3("Small", cls="text-sm font-medium mb-2"),
            Toggle(
                Icon("lucide:star", cls="h-3 w-3"),
                variant="outline",
                size="sm"
            ),
            Toggle(
                Icon("lucide:heart", cls="h-3 w-3"),
                Span("Like", cls="text-xs"),
                variant="outline",
                size="sm"
            ),
            cls="space-y-2"
        ),
        Div(
            H3("Default", cls="text-sm font-medium mb-2"),
            Toggle(
                Icon("lucide:star", cls="h-4 w-4"),
                variant="outline"
            ),
            Toggle(
                Icon("lucide:heart", cls="h-4 w-4"),
                Span("Like"),
                variant="outline"
            ),
            cls="space-y-2"
        ),
        Div(
            H3("Large", cls="text-sm font-medium mb-2"),
            Toggle(
                Icon("lucide:star", cls="h-5 w-5"),
                variant="outline",
                size="lg"
            ),
            Toggle(
                Icon("lucide:heart", cls="h-5 w-5"),
                Span("Like", cls="text-lg"),
                variant="outline",
                size="lg"
            ),
            cls="space-y-2"
        ),
        cls="flex gap-8 justify-center"
    )


@with_code
def social_interactions_example():
    liked = Signal("liked", False)
    comment = Signal("comment", False)
    saved = Signal("saved", False)
    share = Signal("share", False)

    def create_social_toggle(icon, count_signal, sig, label):
        return Toggle(
            Icon(icon, cls="h-4 w-4 mr-1"),
            Span(data_text=count_signal, cls="text-sm"),
            variant="outline",
            signal=sig,
            aria_label=label
        )
    return Card(
        CardContent(
            Div(
                liked, comment, saved, share,
                Div(
                    Icon("lucide:image", cls="h-48 w-full text-muted-foreground/20"),
                    cls="bg-muted rounded-md flex items-center justify-center mb-4"
                ),
                P("Beautiful sunset over the mountains", cls="font-medium mb-2"),
                P("Posted 2 hours ago", cls="text-sm text-muted-foreground mb-4"),
                Div(
                    create_social_toggle("lucide:heart", liked.if_('124', '123'), liked, "Like post"),
                    create_social_toggle("lucide:message-circle", comment.if_('9', '8'), comment, "Comment"),
                    Toggle(
                        Icon("lucide:bookmark", cls="h-4 w-4"),
                        variant="outline",
                        signal=saved,
                        aria_label="Save post"
                    ),
                    Toggle(
                        Icon("lucide:share-2", cls="h-4 w-4"),
                        variant="outline",
                        signal=share,
                        aria_label="Share post"
                    ),
                    cls="flex gap-2"
                ),
                Div(
                    P(
                        Icon("lucide:heart", cls="h-4 w-4 mr-2 text-red-500"),
                        "You liked this",
                        cls="text-xs text-muted-foreground flex items-center",
                        data_show=liked
                    ),
                    P(
                        Icon("lucide:bookmark", cls="h-4 w-4 mr-2"),
                        "Saved to collection",
                        cls="text-xs text-muted-foreground flex items-center",
                        data_show=saved
                    ),
                    cls="mt-2 space-y-1 min-h-[32px]"
                )
            )
        ),
        cls="max-w-sm"
    )


@with_code
def music_player_simulation_example():
    shuffle = Signal("shuffle", False)
    playing = Signal("playing", True)
    repeat = Signal("repeat", True)
    current_time = Signal("current_time", 83)
    total_time = Signal("total_time", 296)
    song_progress = Signal("song_progress", 28)

    return Card(
        CardHeader(
            CardTitle("Now Playing"),
            CardDescription("Sunset Dreams - Ambient Mix")
        ),
        CardContent(
            Div(
                shuffle, playing, repeat, current_time, total_time, song_progress,

                Progress(
                    signal=song_progress,
                    cls="h-2"
                ),

                P(
                    data_text=js("Math.floor($current_time / 60) + ':' + String($current_time % 60).padStart(2, '0') + ' / ' + Math.floor($total_time / 60) + ':' + String($total_time % 60).padStart(2, '0')"),
                    cls="text-xs text-muted-foreground mt-2 text-center"
                ),

                Div(
                    Toggle(
                        Icon("lucide:shuffle", cls="h-4 w-4"),
                        variant="outline",
                        size="sm",
                        signal=shuffle,
                        aria_label="Shuffle"
                    ),
                    Button(
                        Icon("lucide:skip-back", cls="h-4 w-4"),
                        variant="outline",
                        size="sm",
                        aria_label="Previous Song",
                        data_on_click=[current_time.set(0), song_progress.set(0), playing.set(False)]
                    ),
                    Toggle(
                        Icon("lucide:play", cls="h-5 w-5", data_show=~playing),
                        Icon("lucide:pause", cls="h-5 w-5", data_show=playing),
                        variant="outline",
                        signal=playing,
                        pressed=True,
                        aria_label="Play/Pause"
                    ),
                    Button(
                        Icon("lucide:skip-forward", cls="h-4 w-4"),
                        variant="outline",
                        size="sm",
                        aria_label="Next Song",
                        data_on_click=[current_time.set(0), song_progress.set(0), playing.set(False)]
                    ),
                    Toggle(
                        Icon("lucide:repeat", cls="h-4 w-4"),
                        variant="outline",
                        size="sm",
                        signal=repeat,
                        pressed=True,
                        aria_label="Repeat"
                    ),
                    cls="flex items-center justify-center gap-2 mt-4"
                ),

                Div(
                    Badge(
                        data_text=shuffle.if_("Shuffle ON", "Shuffle OFF"),
                        variant="outline",
                        cls="text-xs"
                    ),
                    Badge(
                        data_text=repeat.if_("Repeat ON", "Repeat OFF"),
                        variant="outline",
                        cls="text-xs"
                    ),
                    cls="flex justify-center gap-2 mt-3"
                ),

                data_effect=js("""
                    if (window.musicTimer) {
                        clearInterval(window.musicTimer);
                        window.musicTimer = null;
                    }

                    if ($playing && $current_time < $total_time) {
                        window.musicTimer = setInterval(() => {
                            if (!$playing) {
                                clearInterval(window.musicTimer);
                                return;
                            }

                            if ($current_time < $total_time) {
                                $current_time = $current_time + 1;
                                $song_progress = Math.round(($current_time / $total_time) * 100);
                            } else {
                                clearInterval(window.musicTimer);
                                if ($repeat) {
                                    $current_time = 0;
                                    $song_progress = 0;
                                } else {
                                    $playing = false;
                                }
                            }
                        }, 1000);
                    }
                """)
            )
        ),
        cls="max-w-sm"
    )


@with_code
def disabled_states_example():
    return Div(
        Div(
            H3("Enabled", cls="text-sm font-medium mb-2"),
            Div(
                Toggle(
                    Icon("lucide:wifi", cls="h-4 w-4"),
                    variant="outline"
                ),
                Toggle(
                    Icon("lucide:bluetooth", cls="h-4 w-4"),
                    "Bluetooth",
                    variant="outline"
                ),
                cls="flex gap-2"
            )
        ),
        Div(
            H3("Disabled", cls="text-sm font-medium mb-2"),
            Div(
                Toggle(
                    Icon("lucide:wifi", cls="h-4 w-4"),
                    variant="outline",
                    disabled=True
                ),
                Toggle(
                    Icon("lucide:bluetooth", cls="h-4 w-4"),
                    "Bluetooth",
                    variant="outline",
                    disabled=True,
                    pressed=True
                ),
                cls="flex gap-2"
            )
        ),
        cls="space-y-4"
    )


EXAMPLES_DATA = [
    {"fn": basic_toggle_example, "title": "Basic Toggle", "description": "Simple toggle button with icon"},
    {"fn": feature_toggles_example, "title": "Feature Toggles", "description": "Enable/disable features with descriptive toggles"},
    {"fn": size_variations_example, "title": "Size Variations", "description": "Small, default, and large toggle sizes"},
    {"fn": social_interactions_example, "title": "Social Interactions", "description": "Like, comment, save, and share toggles"},
    {"fn": music_player_simulation_example, "title": "Music Player Simulation", "description": "Simulated music player with realistic timer and toggle controls"},
    {"fn": disabled_states_example, "title": "Disabled States", "description": "Disabled toggles in different states"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("variant", "Literal['default','outline']", "Visual style variant", "'default'"),
        Prop("size", "Literal['default','sm','lg']", "Button size", "'default'"),
        Prop("pressed", "bool", "Initial pressed state", "False"),
        Prop("signal", "str", "Datastar signal (auto-generated if blank)", "auto-generated"),
        Prop("disabled", "bool", "Disable the toggle", "False"),
        Prop("aria_label", "str | None", "ARIA label for accessibility", "None"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def create_toggle_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)