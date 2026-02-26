from starhtml import *
from starhtml.plugins import in_view


def _repo_entry(name: str, description: str, href: str, delay: int = 0) -> FT:
    """Typographic repo row: name ─── description → arrow, entire row is a link."""
    return A(
        Span(name, cls="obs-log-repo-name text-foreground"),
        Span(cls="obs-log-dash"),
        Span(description, cls="obs-log-repo-desc text-muted-foreground"),
        Icon("lucide:arrow-up-right", width="14", height="14", cls="text-muted-foreground/60 flex-shrink-0"),
        href=href,
        target="_blank",
        rel="noopener noreferrer",
        cls="obs-log-repo w-fit hover:text-foreground transition-colors",
        data_motion=in_view(y=10, opacity=0, duration=400, delay=delay, spring="gentle"),
    )


def DocsFooter(cls="", **attrs) -> FT:
    return Footer(
        Div(
            # Repo entries
            Div(
                _repo_entry("starHTML", "Python web framework", "https://github.com/banditburai/starhtml"),
                _repo_entry("starUI", "Component library", "https://github.com/banditburai/starui", delay=50),
                _repo_entry("ko-fi", "Support the project", "https://ko-fi.com/promptsiren", delay=100),
                cls="space-y-3",
            ),
            # Copyright
            P(
                "\u00a9 2026 StarUI \u00b7 Apache 2.0",
                cls="text-[11px] font-mono text-muted-foreground/60 pt-6",
                data_motion=in_view(y=10, opacity=0, duration=400, delay=150, spring="gentle"),
            ),
            cls="px-6 pt-12 pb-16",
        ),
        cls=f"border-t border-border/40 {cls}",
        **attrs,
    )
