"""
Constellation component definitions for landing page.
Each component has metadata for scroll-driven animation.
"""

from starui.registry.components.card import Card
from starui.registry.components.button import Button
from starui.registry.components.input import Input
from starui.registry.components.calendar import Calendar
from starui.registry.components.dialog import Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription
from starhtml import Div, P

def get_constellation_components():
    """
    Returns list of components to display in constellation.

    Format:
    {
        'id': 'unique-id',
        'component': FT element,
        'scroll_trigger': 0.25,  # Percentage of scroll to trigger (0-1)
        'position': {'left': '10%', 'top': '20%'},  # CSS positioning
        'name': 'Component Name',
        'code': 'from starui import ...'
    }
    """
    return [
        {
            'id': 'constellation-card',
            'component': Card(
                Div(
                    Input(placeholder="Search...", cls="mb-3"),
                    Button("Submit", variant="default"),
                    cls="p-6 space-y-3"
                ),
                cls="w-80 gradient-border"
            ),
            'scroll_trigger': 0.25,
            'position': {'left': '10%', 'top': '30%'},
            'name': 'Card',
            'code': '''from starui import Card, Button, Input

Card(
    Input(placeholder="Search..."),
    Button("Submit")
)'''
        },
        {
            'id': 'constellation-calendar',
            'component': Calendar(cls="gradient-border"),
            'scroll_trigger': 0.50,
            'position': {'right': '10%', 'top': '25%'},
            'name': 'Calendar',
            'code': '''from starui import Calendar

Calendar()'''
        },
        {
            'id': 'constellation-dialog',
            'component': Div(
                Dialog(
                    DialogContent(
                        DialogHeader(
                            DialogTitle("Welcome to StarUI"),
                            DialogDescription("Beautiful components for Python developers.")
                        ),
                        P("This is a preview of the Dialog component.", cls="text-sm text-muted-foreground"),
                    ),
                    data_show="true",  # Force visible for preview
                    cls="gradient-border"
                ),
                cls="relative"
            ),
            'scroll_trigger': 0.75,
            'position': {'left': '50%', 'top': '60%', 'transform': 'translateX(-50%)'},
            'name': 'Dialog',
            'code': '''from starui import Dialog, DialogContent

Dialog(
    DialogContent(
        DialogTitle("Title"),
        DialogDescription("Description")
    )
)'''
        }
    ]
