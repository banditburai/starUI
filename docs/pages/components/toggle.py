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

from starhtml import Div, P, Icon, Span, H3, Code, Audio
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, ds_ref, ds_style
)
from starui.registry.components.toggle import Toggle
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.separator import Separator
from starui.registry.components.progress import Progress
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate toggle examples using ComponentPreview with tabs."""
    
    # Basic toggle
    yield ComponentPreview(
        Div(
            Toggle(
                Icon("lucide:bold", cls="h-4 w-4"),
                variant="outline",
                signal="bold_toggle"
            ),
            P(
                "Bold is ",
                Span(ds_text("$bold_toggle ? 'ON' : 'OFF'"), cls="font-mono"),
                cls="text-sm text-muted-foreground mt-2"
            ),
            cls="flex flex-col items-center"
        ),
        '''Toggle(
    Icon("lucide:bold", cls="h-4 w-4"),
    variant="outline",
    signal="bold_toggle"
)''',
        title="Basic Toggle",
        description="Simple toggle button with icon"
    )
    
    # Feature toggles
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Feature Flags"),
                CardDescription("Enable experimental features")
            ),
            CardContent(
                Div(
                    Div(
                        Toggle(
                            Icon("lucide:flask-conical", cls="h-4 w-4 mr-2", ds_class=ds_class(**{"text-orange-500": "$experimental"})),
                            Span("Experimental Mode"),
                            variant="outline",
                            signal="experimental"
                        ),
                        P("Enable beta features", cls="text-sm text-muted-foreground mt-1"),
                        cls="space-y-1"
                    ),
                    Div(
                        Toggle(
                            Icon("lucide:bug", cls="h-4 w-4 mr-2", ds_class=ds_class(**{"text-red-500": "$debug"})),
                            Span("Debug Mode"),
                            variant="outline",
                            signal="debug"
                        ),
                        P("Show debug information", cls="text-sm text-muted-foreground mt-1"),
                        cls="space-y-1"
                    ),
                    Div(
                        Toggle(
                            Icon("lucide:zap", cls="h-4 w-4 mr-2", ds_class=ds_class(**{"text-yellow-500": "$performance"})),
                            Span("Performance Mode"),
                            variant="outline",
                            signal="performance",
                            pressed=True
                        ),
                        P("Optimize for speed", cls="text-sm text-muted-foreground mt-1"),
                        cls="space-y-1"
                    ),
                    Separator(cls="my-4"),
                    Div(
                        Badge(
                            ds_text("[$experimental && 'Experimental', $debug && 'Debug', $performance && 'Performance'].filter(Boolean).join(' • ') || 'Standard Mode'"),
                            variant="secondary",
                            cls="w-full justify-center min-w-[200px]"
                        ),
                        cls="text-center"
                    ),
                    ds_signals(experimental=False, debug=False, performance=True),
                    cls="space-y-3"
                )
            ),
            cls="w-80"
        ),
        '''Card(
    CardContent(
        Toggle(
            Icon("lucide:flask"), "Experimental Mode",
            variant="outline",
            signal="experimental"
        ),
        Toggle(
            Icon("lucide:bug"), "Debug Mode",
            variant="outline",
            signal="debug"
        ),
        Toggle(
            Icon("lucide:zap"), "Performance Mode",
            variant="outline",
            signal="performance",
            pressed=True
        ),
        Badge(
            ds_text("active modes"),
            variant="secondary"
        )
    )
)''',
        title="Feature Toggles",
        description="Enable/disable features with descriptive toggles"
    )
    
    # Size variations
    yield ComponentPreview(
        Div(
            Div(
                H3("Small", cls="text-sm font-medium mb-2"),
                Toggle(
                    Icon("lucide:star", cls="h-3 w-3"),
                    variant="outline",
                    size="sm",
                    signal="star_sm"
                ),
                Toggle(
                    Icon("lucide:heart", cls="h-3 w-3"),
                    Span("Like", cls="text-xs"),
                    variant="outline",
                    size="sm",
                    signal="heart_sm"
                ),
                cls="space-y-2"
            ),
            Div(
                H3("Default", cls="text-sm font-medium mb-2"),
                Toggle(
                    Icon("lucide:star", cls="h-4 w-4"),
                    variant="outline",
                    signal="star_default"
                ),
                Toggle(
                    Icon("lucide:heart", cls="h-4 w-4"),
                    Span("Like"),
                    variant="outline",
                    signal="heart_default"
                ),
                cls="space-y-2"
            ),
            Div(
                H3("Large", cls="text-sm font-medium mb-2"),
                Toggle(
                    Icon("lucide:star", cls="h-5 w-5"),
                    variant="outline",
                    size="lg",
                    signal="star_lg"
                ),
                Toggle(
                    Icon("lucide:heart", cls="h-5 w-5"),
                    Span("Like", cls="text-lg"),
                    variant="outline",
                    size="lg",
                    signal="heart_lg"
                ),
                cls="space-y-2"
            ),
            cls="flex gap-8 justify-center"
        ),
        '''// Size variations
Toggle(Icon("lucide:star"), variant="outline", size="sm")
Toggle(Icon("lucide:heart"), "Like", variant="outline", size="sm")

Toggle(Icon("lucide:star"), variant="outline")  // default size
Toggle(Icon("lucide:heart"), "Like", variant="outline")

Toggle(Icon("lucide:star"), variant="outline", size="lg")
Toggle(Icon("lucide:heart"), "Like", variant="outline", size="lg")''',
        title="Size Variations",
        description="Small, default, and large toggle sizes"
    )
    
    # Social interaction toggles
    yield ComponentPreview(
        Card(
            CardContent(
                Div(
                    Div(
                        Icon("lucide:image", cls="h-48 w-full text-muted-foreground/20"),
                        cls="bg-muted rounded-md flex items-center justify-center mb-4"
                    ),
                    P("Beautiful sunset over the mountains", cls="font-medium mb-2"),
                    P("Posted 2 hours ago", cls="text-sm text-muted-foreground mb-4"),
                    Div(
                        Toggle(
                            Icon("lucide:heart", cls="h-4 w-4 mr-1"),
                            Span(ds_text("$liked ? '124' : '123'"), cls="text-sm"),
                            variant="outline",
                            signal="liked",
                            aria_label="Like post"
                        ),
                        Toggle(
                            Icon("lucide:message-circle", cls="h-4 w-4 mr-1"),
                            Span(ds_text("$comment ? '9' : '8'"), cls="text-sm"),
                            variant="outline",
                            signal="comment",
                            aria_label="Comment"
                        ),
                        Toggle(
                            Icon("lucide:bookmark", cls="h-4 w-4"),
                            variant="outline",
                            signal="saved",
                            aria_label="Save post"
                        ),
                        Toggle(
                            Icon("lucide:share-2", cls="h-4 w-4"),
                            variant="outline",
                            signal="share",
                            aria_label="Share post"
                        ),
                        cls="flex gap-2"
                    ),
                    Div(
                        P(
                            ds_show("$liked"),
                            Icon("lucide:heart", cls="h-4 w-4 mr-2 text-red-500"),
                            "You liked this",
                            cls="text-xs text-muted-foreground flex items-center"
                        ),
                        P(
                            ds_show("$saved"),
                            Icon("lucide:bookmark", cls="h-4 w-4 mr-2"),
                            "Saved to collection",
                            cls="text-xs text-muted-foreground flex items-center"
                        ),
                        cls="mt-2 space-y-1 min-h-[32px]"
                    ),
                    ds_signals(liked=False, comment=False, saved=False, share=False)
                )
            ),
            cls="max-w-sm"
        ),
        '''// Social media post interactions
Card(
    CardContent(
        // Post content
        Div(
            Toggle(
                Icon("lucide:heart"),
                Span(ds_text("$liked ? '124' : '123'")),
                variant="outline",
                signal="liked"
            ),
            Toggle(Icon("lucide:message-circle"), "8", variant="outline"),
            Toggle(Icon("lucide:bookmark"), variant="outline", signal="saved"),
            Toggle(Icon("lucide:share-2"), variant="outline"),
            cls="flex gap-2"
        ),
        P(ds_show("$liked"), Icon("lucide:heart"), "You liked this"),
        P(ds_show("$saved"), Icon("lucide:bookmark"), "Saved")
    )
)''',
        title="Social Interactions",
        description="Like, comment, save, and share toggles"
    )
    
    # Music player controls with HTML5 Audio
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Now Playing"),
                CardDescription("Sunset Dreams - Ambient Mix")
            ),
            CardContent(
                Div(
                    # Realistic timer system for demo purposes
                    ds_effect("""
                        // Clean up any existing timer
                        if (window.musicTimer) {
                            clearInterval(window.musicTimer);
                            window.musicTimer = null;
                        }
                        
                        // Start timer when playing
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
                                    // Song completed
                                    clearInterval(window.musicTimer);
                                    if ($repeat) {
                                        $current_time = 0;  // Reset to beginning
                                        $song_progress = 0;
                                    } else {
                                        $playing = false;
                                    }
                                }
                            }, 1000);
                        }
                    """),
                    
                    # Progress bar
                    Progress(
                        signal="song_progress", 
                        cls="h-2"
                    ),
                    
                    # Time display
                    P(
                        ds_text("Math.floor($current_time / 60) + ':' + String($current_time % 60).padStart(2, '0') + ' / ' + Math.floor($total_time / 60) + ':' + String($total_time % 60).padStart(2, '0')"), 
                        cls="text-xs text-muted-foreground mt-2 text-center"
                    ),
                    
                    # Control buttons
                    Div(
                        Toggle(
                            Icon("lucide:shuffle", cls="h-4 w-4"),
                            variant="outline",
                            size="sm",
                            signal="shuffle",
                            aria_label="Shuffle"
                        ),
                        Button(
                            Icon("lucide:skip-back", cls="h-4 w-4"),
                            ds_on_click("$current_time = 0; $song_progress = 0; $playing = false"),
                            variant="outline",
                            size="sm",
                            aria_label="Previous Song"
                        ),
                        Toggle(
                            Span(Icon("lucide:play", cls="h-5 w-5"), ds_show("!$playing")),
                            Span(Icon("lucide:pause", cls="h-5 w-5"), ds_show("$playing")),
                            variant="outline",
                            signal="playing",
                            pressed=True,  # Start playing
                            aria_label="Play/Pause"
                        ),
                        Button(
                            Icon("lucide:skip-forward", cls="h-4 w-4"),
                            ds_on_click("$current_time = 0; $song_progress = 0; $playing = false"),
                            variant="outline",
                            size="sm",
                            aria_label="Next Song"
                        ),
                        Toggle(
                            Icon("lucide:repeat", cls="h-4 w-4"),
                            variant="outline",
                            size="sm",
                            signal="repeat",
                            pressed=True,
                            aria_label="Repeat"
                        ),
                        cls="flex items-center justify-center gap-2 mt-4"
                    ),
                    
                    # Status badges
                    Div(
                        Badge(
                            ds_text("$shuffle ? 'Shuffle ON' : 'Shuffle OFF'"),
                            variant="outline",
                            cls="text-xs"
                        ),
                        Badge(
                            ds_text("$repeat ? 'Repeat ON' : 'Repeat OFF'"),
                            variant="outline",
                            cls="text-xs"
                        ),
                        cls="flex justify-center gap-2 mt-3"
                    ),
                    
                    # Audio control effect - handles play/pause based on $playing state
                    Div(
                        ds_effect("""
                            const audio = $audioPlayer;
                            if (!audio) return;
                            
                            if ($playing && audio.paused) {
                                console.log('Playing audio...');
                                audio.play().catch(e => {
                                    console.warn('Audio play failed:', e);
                                    $playing = false;
                                });
                            } else if (!$playing && !audio.paused) {
                                console.log('Pausing audio...');
                                audio.pause();
                            }
                        """)
                    ),
                    
                    
                    ds_signals(
                        shuffle=False, 
                        playing=True,   # Start playing for demo
                        repeat=True,
                        current_time=83,   # Start at 1:23 (83 seconds)
                        total_time=296,    # 4:56 total (296 seconds)
                        song_progress=28  # 83/296 = ~28%
                    )
                )
            ),
            cls="max-w-sm"
        ),
        '''// Simulated Music Player with Toggle Controls
Card(
    CardContent(
        // Progress bar synced with timer
        Progress(signal="song_progress", cls="h-2"),
        
        // Time display
        P(ds_text("Math.floor($current_time / 60) + ':' + String($current_time % 60).padStart(2, '0') + ' / 4:56'")),
        ),
        
        // Control buttons
        Div(
            Toggle(Icon("lucide:shuffle"), size="sm", signal="shuffle"),
            Button(Icon("lucide:skip-back"), ds_on_click="audio.currentTime = 0"),
            Toggle(
                Span(Icon("lucide:play"), ds_show="!$playing"),
                Span(Icon("lucide:pause"), ds_show="$playing"),
                signal="playing"
            ),
            Button(Icon("lucide:skip-forward"), ds_on_click="audio.currentTime += 10"),
            Toggle(Icon("lucide:repeat"), size="sm", signal="repeat"),
            cls="flex items-center justify-center gap-2"
        ),
        
        // Audio control effect
        Div(ds_effect="// Play/pause audio based on $playing state")
    )
)''',
        title="Music Player Simulation",
        description="Simulated music player with realistic timer and toggle controls"
    )
    
    # Disabled states
    yield ComponentPreview(
        Div(
            Div(
                H3("Enabled", cls="text-sm font-medium mb-2"),
                Div(
                    Toggle(
                        Icon("lucide:wifi", cls="h-4 w-4"),
                        variant="outline",
                        signal="wifi_enabled"
                    ),
                    Toggle(
                        Icon("lucide:bluetooth", cls="h-4 w-4"),
                        "Bluetooth",
                        variant="outline",
                        signal="bluetooth_enabled"
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
                        disabled=True,
                        signal="wifi_disabled"
                    ),
                    Toggle(
                        Icon("lucide:bluetooth", cls="h-4 w-4"),
                        "Bluetooth",
                        variant="outline",
                        disabled=True,
                        pressed=True,
                        signal="bluetooth_disabled"
                    ),
                    cls="flex gap-2"
                )
            ),
            cls="space-y-4"
        ),
        '''// Disabled states
Toggle(Icon("lucide:wifi"), variant="outline")  // Enabled
Toggle(Icon("lucide:bluetooth"), "Bluetooth", variant="outline")

Toggle(Icon("lucide:wifi"), variant="outline", disabled=True)  // Disabled
Toggle(
    Icon("lucide:bluetooth"), "Bluetooth",
    variant="outline",
    disabled=True,
    pressed=True  // Disabled in pressed state
)''',
        title="Disabled States",
        description="Disabled toggles in different states"
    )


def create_toggle_docs():
    """Create toggle documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "variant",
                "type": "Literal['default', 'outline']",
                "default": "'default'",
                "description": "Visual style variant"
            },
            {
                "name": "size",
                "type": "Literal['default', 'sm', 'lg']",
                "default": "'default'",
                "description": "Size of the toggle button"
            },
            {
                "name": "pressed",
                "type": "bool",
                "default": "False",
                "description": "Initial pressed state"
            },
            {
                "name": "signal",
                "type": "str",
                "default": "auto-generated",
                "description": "Datastar signal name for state management"
            },
            {
                "name": "disabled",
                "type": "bool",
                "default": "False",
                "description": "Whether the toggle is disabled"
            },
            {
                "name": "aria_label",
                "type": "str | None",
                "default": "None",
                "description": "Accessibility label for screen readers"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes"
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            Toggle(
                Icon("lucide:bold", cls="h-4 w-4"),
                Span("Bold"),
                variant="outline",
                signal="hero_toggle"
            ),
            P(
                "Toggle is ",
                Span(ds_text("$hero_toggle ? 'pressed' : 'not pressed'"), cls="font-mono"),
                cls="text-sm text-muted-foreground mt-2"
            ),
            cls="flex flex-col items-center"
        ),
        '''Toggle(
    Icon("lucide:bold", cls="h-4 w-4"),
    Span("Bold"),
    variant="outline",
    signal="hero_toggle"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add toggle",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="toggle"
    )