from starhtml import *
from components.utils import cn
from .code_block import CodeBlock

SCROLLBAR_STYLE = "scrollbar-width: thin;"


def _cli_installation_section(cli_command: str) -> FT:
    return Div(
        H3("CLI", cls="text-lg font-semibold"),
        P("Install the component using the StarUI CLI:", cls="mb-3 text-sm text-muted-foreground"),
        CodeBlock(cli_command, language="bash", cls="mt-2", center_button=True),
        cls="space-y-3"
    )


def _manual_installation_section(manual_files: list[dict[str, str]]) -> FT:
    return Div(
        H3("Manual Installation", cls="mt-6 text-lg font-semibold"),
        P("Copy the following code to your project:", cls="mb-3 text-sm text-muted-foreground"),
        *[
            Div(
                P(file["path"], cls="mb-2 font-mono text-sm text-muted-foreground"),
                CodeBlock(file["content"], language=file.get("language", "python"), cls="overflow-x-auto", style=SCROLLBAR_STYLE),
                cls="mb-4"
            )
            for file in manual_files
        ],
        cls="space-y-3"
    )


def _dependencies_section(dependencies: list[str]) -> FT:
    return Div(
        H3("Dependencies", cls="mt-6 text-lg font-semibold"),
        P("This component requires the following dependencies:", cls="mb-3 text-sm text-muted-foreground"),
        CodeBlock("\n".join(dependencies), language="bash", cls="overflow-x-auto", style=SCROLLBAR_STYLE),
        cls="space-y-3"
    )


def InstallationSection(
    cli_command: str | None = None,
    manual_files: list[dict[str, str]] | None = None,
    dependencies: list[str] | None = None,
    cls: str = "",
    **attrs
) -> FT:
    sections = [H2("Installation", cls="text-2xl font-bold tracking-tight")]

    if cli_command:
        sections.append(_cli_installation_section(cli_command))

    if manual_files:
        sections.append(_manual_installation_section(manual_files))

    if dependencies:
        sections.append(_dependencies_section(dependencies))

    return Div(*sections, cls=cn("space-y-6", cls), **attrs)