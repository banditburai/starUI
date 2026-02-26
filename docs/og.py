"""OG image templates for StarUI docs — rendered by star.og.

Each function returns an FT tree that star.og converts to Typst markup → PNG.
Editorial celestial observatory aesthetic: asymmetric layouts, extreme
typographic scale, bleeding text, observatory reticle marks, guide lines.

Dark mode (StarUI): navy→warm horizon, Playfair Display, orange accents
Light mode (StarHTML): lavender→peach→gold, dark navy, amber accents
"""

from pathlib import Path

from starhtml import Div, Svg, SvgPath
from star.og.compose import pos, text, dims, card, flex, nudge, fill

OG_FONTS = ["Playfair Display", "Cormorant Garamond", "Inter"]
OG_OUTPUT_DIR = Path(__file__).parent / "og_build"

# ── Project fonts ──
PF = "'Playfair Display',serif"
CG = "'Cormorant Garamond',serif"
IN = "'Inter',sans-serif"

# ── Project palette ──
AMBER = "#92400E"
ORANGE = "#FB923C"
NAVY = "#1e293b"
SLATE = "#64748B"
MUTED = "#94A3B8"

# ── Project theme gradients ──
DARK_ANGLED = "linear-gradient(135deg, #0B1221 0%, #1e293b 50%, #3e4c5f 75%, #8c5e45 100%)"
DARK_RADIAL = "radial-gradient(circle at 50% 100%, #8c5e45 0%, #3e4c5f 25%, #1e293b 50%, #0B1221 100%)"
DARK_VERTICAL = "linear-gradient(180deg, #8c5e45 0%, #6b5550 15%, #4e4d58 25%, #3e4c5f 35%, #2d3d50 45%, #1e293b 58%, #162234 72%, #101c2b 85%, #0B1221 100%)"
LIGHT_ANGLED = "linear-gradient(135deg, #dfe8f3 0%, #e2dff0 25%, #f0e4e0 55%, #f5dbc4 80%, #edc9a0 100%)"


# ── Project-level element helpers ──

def _reticles(color, size=20, inset=40, char="+"):
    """Corner marks at four card corners."""
    s = text(IN, size, weight=200, color=color) + " line-height:1;"
    return [
        Div(char, style=s + pos(top=inset, left=inset)),
        Div(char, style=s + pos(top=inset, right=inset)),
        Div(char, style=s + pos(bottom=inset, left=inset)),
        Div(char, style=s + pos(bottom=inset, right=inset)),
    ]

def _guide(axis, offset, color):
    """Full-width/height guide line."""
    if axis == "v":
        return Div(style=f"position:absolute; left:{offset}px; top:0; width:1px; height:100%; background:{color};")
    return Div(style=f"position:absolute; left:0; top:{offset}px; width:100%; height:1px; background:{color};")

def _accent_label(label, color=AMBER, line_width=50, size=13, thickness=1.5):
    """Accent line + uppercase label. Spread into a flex container."""
    return [
        Div(style=f"width:{line_width}px; height:{thickness}px; background-color:{color};"),
        Div(label, style=text(IN, size, spacing="0.18em", color=color, lh=1)),
    ]

def _icon(d, sz, color=AMBER):
    """SVG icon from a path d string."""
    return Svg(SvgPath(d=d, fill=color), viewBox="0 0 24 24", style=f"width:{sz}px; height:{sz}px;")

def _watermark(d, sz=400, *, color=NAVY, opacity=0.08, rotate=12, top=10, right=10, z=5):
    """Ghosted SVG background watermark."""
    return Div(
        Svg(SvgPath(d=d, fill=color, opacity=str(opacity)), viewBox="0 0 24 24", style=f"width:{sz}px; height:{sz}px;"),
        style=f"{pos(top=top, right=right, z=z)} {dims(sz, sz)} transform:rotate({rotate}deg);",
    )

# ── SVG paths ──
_STAR_SVG_D = "M12 2L14 10L22 12L14 14L12 22L10 14L2 12L10 10Z"

_PYTHON_LOGO_D = (
    "M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5"
    "l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77"
    "l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06"
    "H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88"
    "-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1"
    ".32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26"
    ".31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33"
    "-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41"
    "-.09-.41.09zm13.09 3.95l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04"
    ".05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05"
    "-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2"
    "-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3"
    "-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46"
    ".26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14"
    ".5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01z"
    "m-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41"
    "-.23-.33-.33-.23-.41-.08-.41.08z"
)


_DARK_RET_COLOR = "rgba(248,250,252,0.15)"
_LIGHT_RET_COLOR = "rgba(30,41,59,0.12)"
_DARK_GUIDE_COLOR = "rgba(248,250,252,0.06)"
_LIGHT_GUIDE_COLOR = "rgba(30,41,59,0.06)"


def starui_og():
    """Dark mode — observatory glass panel with star mark.

    Middle-ground composition from reference observatory designs:
    radial-gradient background with warm upward glow, editorial headline
    left, glass panel with centered star mark and data rows right,
    translucent sphere depth element center.
    """
    GLASS_BG = "rgba(11,18,33,0.4)"
    GLASS_B = "rgba(255,255,255,0.1)"

    # ── Panel geometry (flat-positioned for reliable rendering) ──
    PR, PT = 60, 115       # panel right/top offsets
    PW, PH = 320, 400      # panel dimensions
    PP = 28                 # panel padding
    CL = 1200 - PR - PW + PP   # content left x = 848
    CR = PR + PP                # content right offset = 88
    CT = PT + PP                # content top = 143
    CB = PT + PH - PP           # content bottom = 487
    CW = PW - 2 * PP           # content width = 264

    # ── Sphere (background depth element) ──
    SX, SY = 620, 300
    SPHERE_SZ = 340

    sphere = Div(
        Svg(SvgPath(d=_STAR_SVG_D, fill="#F8FAFC", opacity="0.04"),
            viewBox="0 0 24 24", style="width:160px; height:160px;"),
        style=(
            pos(top=SY - SPHERE_SZ // 2, left=SX - SPHERE_SZ // 2, z=2)
            + dims(SPHERE_SZ, SPHERE_SZ)
            + " background:radial-gradient(circle at 30% 30%,"
            + " rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 40%, rgba(0,0,0,0) 70%);"
            + " border:1px solid rgba(248,250,252,0.05); border-radius:50%;"
        ),
    )

    # ── Glass panel (background rect — leaf shape) ──
    panel_bg = Div(
        style=(
            pos(top=PT, right=PR, z=12)
            + f"width:{PW}px; height:{PH}px;"
            + f" background:{GLASS_BG}; border:1px solid {GLASS_B};"
            + f" box-shadow:0 20px 40px rgba(0,0,0,0.15);"
        ),
    )

    # ── Panel header data row ──
    panel_h_l = Div("AZIMUTH",
        style=pos(top=CT, left=CL, z=14)
        + text(IN, 10, spacing="0.15em", color="#475569", uppercase=True))
    panel_h_r = Div("142.5\u00b0",
        style=pos(top=CT, right=CR, z=14)
        + text(IN, 10, spacing="0.15em", color=MUTED))
    panel_h_sep = Div(
        style=pos(top=CT + 24, left=CL, z=14)
        + f"width:{CW}px; height:1px; background:{GLASS_B};")

    # ── Star mark (centered in panel) ──
    STAR_SZ = 80
    STAR_X = CL + (CW - STAR_SZ) // 2
    STAR_Y = PT + (PH - STAR_SZ) // 2

    star_glow = Div(
        style=(
            pos(top=STAR_Y - 20, left=STAR_X - 20, z=13)
            + f"width:{STAR_SZ + 40}px; height:{STAR_SZ + 40}px;"
            + " background:radial-gradient(circle at 50% 50%,"
            + " rgba(248,250,252,0.04) 0%, rgba(0,0,0,0) 70%);"
            + " border-radius:50%;"
        ),
    )
    star_mark = Div(
        Svg(SvgPath(d=_STAR_SVG_D, fill="#F8FAFC", opacity="0.85"),
            viewBox="0 0 24 24", style=f"width:{STAR_SZ}px; height:{STAR_SZ}px;"),
        style=pos(top=STAR_Y, left=STAR_X, z=14) + dims(STAR_SZ, STAR_SZ),
    )

    # ── Panel footer data row ──
    panel_f_sep = Div(
        style=pos(top=CB - 24, left=CL, z=14)
        + f"width:{CW}px; height:1px; background:{GLASS_B};")
    panel_f_l = Div("SPECTRAL TYPE",
        style=pos(top=CB - 14, left=CL, z=14)
        + text(IN, 10, spacing="0.15em", color="#475569", uppercase=True))
    panel_f_r = Div("K-CLASS",
        style=pos(top=CB - 14, right=CR, z=14)
        + text(IN, 10, spacing="0.15em", color=MUTED))

    # ── Scattered small stars (visual texture like Design 2) ──
    star_sm_1 = Div(
        Svg(SvgPath(d=_STAR_SVG_D, fill="#F8FAFC", opacity="0.12"),
            viewBox="0 0 24 24", style="width:10px; height:10px;"),
        style=pos(top=200, left=530, z=3) + dims(10, 10),
    )
    star_sm_2 = Div(
        Svg(SvgPath(d=_STAR_SVG_D, fill=ORANGE, opacity="0.10"),
            viewBox="0 0 24 24", style="width:14px; height:14px;"),
        style=pos(bottom=180, right=400, z=3) + dims(14, 14),
    )

    # ── Glitch line (subtle horizontal accent from Design 2) ──
    glitch_line = Div(
        style=pos(top=315, left=0, z=4)
        + "width:1200px; height:1px; background:rgba(248,250,252,0.06);",
    )

    return Div(
        # ── Grid system ──
        _guide("v", 150, _DARK_GUIDE_COLOR),
        _guide("v", 1050, _DARK_GUIDE_COLOR),
        _guide("h", 115, _DARK_GUIDE_COLOR),
        _guide("h", 515, _DARK_GUIDE_COLOR),
        *_reticles(_DARK_RET_COLOR),
        # ── Header band ──
        Div(
            Div("Vol. 01", style=text(IN, 11, spacing="0.25em", color=SLATE, uppercase=True)),
            Div("Component Library", style=text(IN, 11, spacing="0.25em", color=SLATE, uppercase=True)),
            style=pos(top=50, left=180) + flex(gap=32),
        ),
        Div("STARUI", style=pos(top=50, right=60) + text(IN, 11, spacing="0.25em", color=SLATE, uppercase=True)),
        # ── Depth sphere + scattered stars ──
        sphere,
        star_sm_1, star_sm_2,
        glitch_line,
        # ── Headline block ──
        Div(
            Div(
                Div(_icon(_STAR_SVG_D, 14, ORANGE), style=dims(14, 14)),
                Div("Fig 1.0 \u2014 Architecture", style=text(IN, 10, spacing="0.2em", color=ORANGE, uppercase=True)),
                Div(style=f"width:50px; height:1px; background:{ORANGE}; opacity:0.6;"),
                style=flex(align="center", gap=10) + " margin-bottom:20px;",
            ),
            Div("Components", style=text(PF, 96, italic=True, weight=400, color="#F8FAFC", spacing="-0.02em")),
            Div("you own.", style=text(PF, 96, italic=True, weight=400, color="#F8FAFC", spacing="-0.02em") + " opacity:0.8; padding-left:60px;"),
            Div(
                "Tracing the invisible geometry of the interface.",
                style=text(CG, 24, italic=True, weight=300, color=MUTED) + " margin-top:36px;",
            ),
            style=pos(top=130, left=170, z=10),
        ),
        # ── Glass panel ──
        panel_bg,
        panel_h_l, panel_h_r, panel_h_sep,
        star_glow, star_mark,
        panel_f_sep, panel_f_l, panel_f_r,
        # ── Bottom bar ──
        Div(
            *_accent_label("OBSERVATORY"),
            style=pos(bottom=50, left=170) + flex(align="center", gap=8),
        ),
        Div("SYS.OBS.V.2.04",
            style=pos(bottom=50, right=60) + text(IN, 9, spacing="0.15em", color=SLATE, uppercase=True)),
        # ── Vertical guides (thin atmospheric lines) ──
        Div(style=pos(top=0, left=200, z=1) + "width:1px; height:630px; background:rgba(248,250,252,0.03);"),
        Div(style=pos(top=0, right=200, z=1) + "width:1px; height:630px; background:rgba(248,250,252,0.03);"),
        style=card(DARK_RADIAL),
    )


def _skel_command(top, left, w=300):
    """Command palette skeleton matching real component proportions.

    Spacing derived from the actual shadcn Command component:
    search (px-4 py-3.5), content (p-2), rows (px-3 py-2.5 gap-3),
    section headers (text-[11px] px-2 py-2), separator (mx-2 my-1).
    Scaled ~0.67x from the 448px max-w-md original.
    """
    BORDER = "rgba(255,255,255,0.10)"
    ACTIVE = "rgba(255,255,255,0.10)"
    BAR = "rgba(248,250,252,0.16)"
    BAR_DIM = "rgba(248,250,252,0.09)"
    ICON_C = "rgba(148,163,184,0.25)"
    KBD_BG = "rgba(255,255,255,0.07)"
    IC = 11
    CP = 8       # content area padding (p-2 scaled)
    RP = 10      # row left padding inside content (px-3 scaled)
    LP = CP + RP # total left pad from panel edge
    y = 0
    els = []

    # ── Search bar (px-4 py-3.5 → 11px pad, ~40px tall) ──
    SH = 40
    els.append(Div(style=pos(top=0, left=0) + f"width:{w}px; height:{SH}px;"
                    + f" border-bottom:1px solid {BORDER};"))
    els.append(Div(style=pos(top=14, left=12) + dims(IC, IC)
                    + f" border-radius:3px; background:{ICON_C};"))
    els.append(Div(style=pos(top=16, left=28) + dims(int(w * 0.42), 7)
                    + f" background:{BAR_DIM}; border-radius:3px;"))
    y = SH

    # ── Content area (p-2) ──
    y += CP

    # Suggestions header (text-[11px] px-2 py-2)
    els.append(Div(style=pos(top=y + 4, left=CP + 6) + dims(58, 5)
                    + f" background:{BAR_DIM}; border-radius:2px;"))
    y += 20

    # 3 suggestion rows (px-3 py-2.5, gap-3 between icon and text)
    ROW_H = 30
    row_labels = [0.24, 0.30, 0.22]  # text bar widths as fraction of w
    for i in range(3):
        # Active highlight on first row
        if i == 0:
            els.append(Div(style=pos(top=y, left=CP) + f"width:{w - CP * 2}px; height:{ROW_H}px;"
                            + f" border-radius:6px; background:{ACTIVE};"))
        # Icon (rounded-sm, not circle — matches lucide icon containers)
        iy = y + (ROW_H - IC) // 2
        els.append(Div(style=pos(top=iy, left=LP) + dims(IC, IC)
                        + f" border-radius:3px; background:{ICON_C};"))
        # Text bar
        bw = int(w * row_labels[i])
        ty = y + (ROW_H - 7) // 2
        els.append(Div(style=pos(top=ty, left=LP + IC + 8) + dims(bw, 7)
                        + f" background:{BAR if i == 0 else BAR_DIM}; border-radius:3px;"))
        y += ROW_H

    # Separator (h-px mx-2 my-1)
    y += 4
    els.append(Div(style=pos(top=y, left=CP + 6) + f"width:{w - (CP + 6) * 2}px; height:1px;"
                    + f" background:{BORDER};"))
    y += 8

    # Settings header
    els.append(Div(style=pos(top=y + 4, left=CP + 6) + dims(44, 5)
                    + f" background:{BAR_DIM}; border-radius:2px;"))
    y += 20

    # 2 settings rows with kbd shortcut badges
    settings_labels = [0.18, 0.15]
    for i in range(2):
        iy = y + (ROW_H - IC) // 2
        els.append(Div(style=pos(top=iy, left=LP) + dims(IC, IC)
                        + f" border-radius:3px; background:{ICON_C};"))
        bw = int(w * settings_labels[i])
        ty = y + (ROW_H - 7) // 2
        els.append(Div(style=pos(top=ty, left=LP + IC + 8) + dims(bw, 7)
                        + f" background:{BAR_DIM}; border-radius:3px;"))
        # Kbd badge (text-[10px] px-1.5 py-0.5 rounded)
        ky = y + (ROW_H - 14) // 2
        els.append(Div(style=pos(top=ky, right=LP) + dims(26, 14)
                        + f" background:{KBD_BG}; border-radius:3px;"
                        + f" border:1px solid {BORDER};"))
        y += ROW_H

    y += CP

    return Div(
        *els,
        style=(
            pos(top=top, left=left, z=5)
            + f"width:{w}px; height:{y}px;"
            + " background:rgba(15,23,42,0.72);"
            + " border:1px solid rgba(255,255,255,0.12);"
            + " border-radius:10px; overflow:hidden;"
        ),
    )


def starui_og_skeleton():
    """Dark mode — vertical typographic lockup with command palette skeleton.

    'star' above 'UI' left-aligned. Command palette emerges from behind
    the typography, its left edge tucked under the 'I' of 'UI' (lower z),
    extending rightward and bleeding off the right edge of the canvas.
    """
    _ret = text(IN, 22, weight=300, color=ORANGE) + " line-height:1;"
    INSET = 40

    STAR_TOP = 85
    STAR_LEFT = 230
    STAR_SIZE = 260

    UI_TOP = 255
    UI_LEFT = 230
    UI_SIZE = 390

    return Div(
        _skel_command(top=130, left=610, w=320),
        Div(
            Div("+", style=_ret),
            *_accent_label("PYTHON COMPONENT LIBRARY", color=ORANGE, line_width=55, size=16, thickness=2),
            style=pos(top=INSET, left=INSET) + flex(align="center", gap=12),
        ),
        Div("star", style=pos(top=STAR_TOP, left=STAR_LEFT)
            + text(CG, STAR_SIZE, italic=True, weight=500, color="#F8FAFC", spacing="-0.02em")),
        Div("UI",
            style=pos(top=UI_TOP, left=UI_LEFT, z=10)
            + text(PF, UI_SIZE, weight=400, color="#F8FAFC", spacing="-0.01em", nowrap=True)),
        style=card(DARK_VERTICAL),
    )


def starhtml_og():
    """Dawn sky — overscaled 'HTML' bleeds off bottom.

    All positions derived from the guide system + named anchors.
    Use nudge(dx, dy) on any element for manual visual refinement.
    """
    _ret = text(IN, 22, weight=300, color=AMBER) + " line-height:1;"

    # ── Guide system & anchors ──
    INSET = 40
    GUIDE_V = 170       # vertical guide x
    GUIDE_H = 95        # horizontal guide y
    CX = GUIDE_V + 20   # content left (past guide + breathing room)
    CY = GUIDE_H + 20   # content top (past guide + breathing room)

    # ── Element anchors ──
    HTML_TOP = 250       # where the HTML block starts
    HTML_LEFT = -230      # bleeds off left edge
    HTML_SIZE = 600      # font size for HTML text

    STAR_TOP = 80        # Star text vertical position
    STAR_LEFT = 225      # Star text horizontal position
    STAR_SIZE = 260      # Star font size
    STAR_ICON = 250      # Star icon size

    # Star icon: positioned relative to the Star text, then nudgeable
    ICON_TOP = STAR_TOP + 10
    ICON_LEFT = STAR_LEFT - STAR_ICON - 12  # to the left of "Star" text

    return Div(
        # Python watermark
        _watermark(_PYTHON_LOGO_D, 550, top=20, right=50),
        # Header: reticle + label (top-left corner)
        Div(
            Div("+", style=_ret),
            *_accent_label("PYTHON WEB FRAMEWORK", line_width=55, size=16, thickness=2),
            style=pos(top=INSET, left=INSET) + flex(align="center", gap=12),
        ),
        Div("star", style=pos(top=STAR_TOP, left=STAR_LEFT)
            + text(CG, STAR_SIZE, italic=True, weight=500, color=NAVY, spacing="-0.02em")),
        Div("HTML",
            style=pos(top=HTML_TOP, left=HTML_LEFT, z=10)
            + text(PF, HTML_SIZE, weight=350, color=NAVY, spacing="-0.02em", nowrap=True)),

        style=card(LIGHT_ANGLED),
    )


def components_og():
    """Dark observatory — component system architecture."""
    return Div(
        _guide("v", 150, _DARK_GUIDE_COLOR),
        _guide("h", 115, _DARK_GUIDE_COLOR),
        *_reticles(_DARK_RET_COLOR),
        # Header band
        Div(
            Div("Vol. 02", style=text(IN, 11, spacing="0.25em", color=SLATE, uppercase=True)),
            Div("System Architecture", style=text(IN, 11, spacing="0.25em", color=SLATE, uppercase=True)),
            style=pos(top=50, left=180) + flex(gap=32),
        ),
        Div("STARUI", style=pos(top=50, right=60) + text(IN, 11, spacing="0.25em", color=SLATE, uppercase=True)),
        # Annotation — past the guide intersection with breathing room
        Div(
            Div(_icon(_STAR_SVG_D, 14, ORANGE), style=dims(14, 14)),
            Div("Design Primitives", style=text(IN, 10, spacing="0.25em", color=ORANGE, uppercase=True)),
            Div(style=f"width:60px; height:1px; background:{ORANGE}; opacity:0.6;"),
            style=pos(top=120, left=170, z=10) + flex(align="center", gap=12),
        ),
        # Headline
        Div("The Architecture",
            style=pos(top=155, left=170, z=10) + text(PF, 96, italic=True, weight=400, color="#F8FAFC", spacing="-0.03em")),
        Div("of Void",
            style=pos(top=255, left=190, z=10) + text(PF, 96, italic=True, weight=400, color="#F8FAFC", spacing="-0.03em") + " opacity:0.8;"),
        # Subtitle
        Div("A comprehensive design system for deep-space interfaces.",
            style=pos(top=365, left=170, z=10) + text(CG, 22, italic=True, weight=300, color=MUTED)),
        # Glass panel
        Div(
            Div(
                Div("Status", style=text(IN, 10, spacing="0.25em", color=MUTED, uppercase=True)),
                Div(style="width:6px; height:6px; background:#10B981; border-radius:50%; box-shadow:0 0 8px #10B981;"),
                style=flex(justify="space-between", align="center") + " border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px;",
            ),
            Div(
                Div("Ver", style=text(IN, 10, spacing="0.25em", color="#475569", uppercase=True)),
                Div("2.4.0", style=text(IN, 10, spacing="0.25em", color=MUTED)),
                style=flex(justify="space-between"),
            ),
            Div(
                Div("Coords", style=text(IN, 10, spacing="0.25em", color="#475569", uppercase=True)),
                Div("12.00, 63.0", style=text(IN, 10, spacing="0.25em", color=MUTED)),
                style=flex(justify="space-between"),
            ),
            style=(
                pos(bottom=60, right=60)
                + " width:220px; padding:20px 28px;"
                + flex(direction="column", gap=10)
                + " background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);"
            ),
        ),
        style=card(DARK_ANGLED),
    )


OG_TEMPLATES = {
    # "starui": starui_og,    
    "starui": starui_og_skeleton,
    "starhtml": starhtml_og,
    # "components": components_og,
}
