"""StarHTML app starter template."""

from pathlib import Path

from ..config import ProjectConfig

APP_TEMPLATE = """\
from starhtml import *
from starui import ThemeToggle

styles = Link(rel="stylesheet", href="{css_path}", type="text/css")

app, rt = star_app(
    hdrs=(
        theme_script(use_data_theme=True),
        styles,
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground")
)

@rt("/")
def get():
    return Div(
        Div(ThemeToggle(), cls="absolute top-4 right-4"),
        Div(
            H1("Nothing to see here yet...", cls="text-2xl font-bold mb-2 text-foreground"),
            P("But your StarHTML app is running!", cls="text-base text-muted-foreground"),
            P("Theme toggle in top right →", cls="text-sm text-muted-foreground mt-4"),
            cls="text-center"
        ),
        cls="min-h-screen flex items-center justify-center relative"
    )

if __name__ == "__main__":
    serve(port=8000)
"""


def generate_app_starter(config: ProjectConfig | None = None, **_) -> str:
    """Generate StarHTML app starter with theme system."""
    if config is None:
        config = ProjectConfig(
            project_root=Path.cwd(),
            css_output=Path("starui.css"),
            component_dir=Path("components/ui"),
        )

    css_path = str(config.css_output)
    if not css_path.startswith("/"):
        css_path = "/" + css_path

    return APP_TEMPLATE.format(css_path=css_path)
