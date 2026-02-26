#!/usr/bin/env python3
"""Test file for shiny button using NotStr wrapper."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from starhtml import *
import registry_loader


app, rt = star_app(
    live=True,
    hdrs=(
        theme_script(use_data_theme=True),
        Script(src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"),
        Style("""
@theme {
    --color-primary: oklch(20.5% 0 0);
}
        """)
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(
        cls="min-h-screen bg-background text-foreground flex items-center justify-center",
    ),
)


@rt("/")
def index():
    """Test page for button."""
    return Div(
        H1("Button Test", cls="text-3xl font-bold mb-8"),        
        NotStr("""
<!-- From Uiverse.io by mRcOol7 -->
<button
  class="group cursor-pointer outline-none hover:rotate-90 duration-300"
  title="Add New"
>
  <svg
    class="stroke-teal-500 fill-none group-hover:fill-teal-800 group-active:stroke-teal-200 group-active:fill-teal-600 group-active:duration-0 duration-300"
    viewBox="0 0 24 24"
    height="50px"
    width="50px"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      stroke-width="1.5"
      d="M12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22Z"
    ></path>
    <path stroke-width="1.5" d="M8 12H16"></path>
    <path stroke-width="1.5" d="M12 16V8"></path>
  </svg>
</button>

<div class="mt-8" data-signals-x="100" data-init="const duration = 3000; const pauseDuration = 1000; let animationStart = Date.now(); const animate = () => { const elapsed = Date.now() - animationStart; if (elapsed < duration) { const progress = elapsed / duration; $x = Math.round(100 - (progress * 200)); requestAnimationFrame(animate); } else { $x = -100; setTimeout(() => { animationStart = Date.now(); animate(); }, pauseDuration); } }; setTimeout(animate, pauseDuration);">
  <h2 class="text-2xl font-bold mb-4">Shiny Button</h2>

  <button
    class="relative cursor-pointer rounded-lg border border-gray-300 px-6 py-2 font-medium transition-shadow duration-300 ease-in-out hover:shadow"
    tabindex="0"
    data-style="{'--x': $x + '%'}"
  >
    <span
      class="relative block size-full text-sm tracking-wide uppercase text-gray-700"
      style="-webkit-mask-image: linear-gradient(-75deg, #000 calc(var(--x) + 20%), rgba(0,0,0,0.3) calc(var(--x) + 30%), #000 calc(var(--x) + 100%)); mask-image: linear-gradient(-75deg, #000 calc(var(--x) + 20%), rgba(0,0,0,0.3) calc(var(--x) + 30%), #000 calc(var(--x) + 100%));"
    >
      Shiny Button
    </span>
    <span
      class="absolute inset-0 z-10 block rounded-[inherit] p-px pointer-events-none"
      style="mask: linear-gradient(#000, #000) content-box exclude, linear-gradient(#000, #000); -webkit-mask: linear-gradient(#000, #000) content-box exclude, linear-gradient(#000, #000); background-image: linear-gradient(-75deg, rgba(255,255,255,0.1) calc(var(--x) + 20%), rgba(255,255,255,0.5) calc(var(--x) + 25%), rgba(255,255,255,0.1) calc(var(--x) + 100%));"
    />
</div>
        """),

        cls="flex flex-col items-center"
    )


serve()
