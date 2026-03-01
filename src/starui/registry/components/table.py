from typing import Any

from starhtml import (
    FT,
    Caption,
    Div,
    Table as HTMLTable,
    Tbody,
    Td,
    Tfoot,
    Th,
    Thead,
    Tr,
)

from .utils import cn


def Table(
    *children: Any,
    cls: str = "",
    wrapper_cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        HTMLTable(
            *children,
            data_slot="table",
            cls=cn("w-full caption-bottom text-sm", cls),
            **kwargs,
        ),
        data_slot="table-container",
        cls=cn("relative w-full overflow-x-auto", wrapper_cls),
    )


def TableHeader(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Thead(
        *children,
        data_slot="table-header",
        cls=cn("[&_tr]:border-b", cls),
        **kwargs,
    )


def TableBody(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Tbody(
        *children,
        data_slot="table-body",
        cls=cn("[&_tr:last-child]:border-0", cls),
        **kwargs,
    )


def TableFooter(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Tfoot(
        *children,
        data_slot="table-footer",
        cls=cn(
            "bg-muted/50 border-t font-medium [&>tr]:last:border-b-0", cls
        ),
        **kwargs,
    )


def TableRow(
    *children: Any,
    selected: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Tr(
        *children,
        data_slot="table-row",
        data_state="selected" if selected else None,
        cls=cn(
            "border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
            cls,
        ),
        **kwargs,
    )


def TableHead(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Th(
        *children,
        data_slot="table-head",
        cls=cn(
            "text-foreground h-10 px-2 text-left align-middle font-medium whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
            cls,
        ),
        **kwargs,
    )


def TableCell(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Td(
        *children,
        data_slot="table-cell",
        cls=cn(
            "p-2 align-middle whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
            cls,
        ),
        **kwargs,
    )


def TableCaption(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Caption(
        *children,
        data_slot="table-caption",
        cls=cn("mt-4 text-sm text-muted-foreground", cls),
        **kwargs,
    )
