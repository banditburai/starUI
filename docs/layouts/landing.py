import random

from starhtml import *
from starhtml.plugins import scroll
from layouts.header import DocsHeader
from layouts.base import HeaderConfig


def _landing_styles() -> FT:
    return Style("""
        /* ══════════════════════════════════════
           STARUI LANDING — Sunrise / Sunset
           Dark (default): navy→warm horizon, white text
           Light: cool dawn gradient, dark text
           ══════════════════════════════════════ */

        /* ── Landing page body font ── */
        .landing-page {
            font-family: 'Inter', sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* ── Font utilities ── */
        .font-display { font-family: 'Playfair Display', serif; }
        .font-serif-body { font-family: 'Cormorant Garamond', serif; }

        /* ── Hero headline — enormous with tight leading ── */
        .hero-headline {
            font-size: clamp(2.5rem, 2rem + 5.5vw, 9rem);
            line-height: 0.85;
            letter-spacing: -0.03em;
        }
        .hero-subline {
            font-size: 0.618em;   /* 1/phi — golden ratio to headline */
            letter-spacing: 0.02em;
        }

        /* ── Star mark — breathing ornament ── */
        @keyframes star-breathe {
            0%, 100% { opacity: 0.4; }
            50% { opacity: 1; }
        }
        .star-mark {
            animation: star-breathe 4s ease-in-out infinite;
        }

        /* ── Hero grid — two-column at 768px+, progressive widening ── */
        @media (min-width: 768px) {
            .hero-grid-phi {
                grid-template-columns: 1.2fr 1fr;
                gap: 12px;
                align-items: end;
            }
        }
        @media (min-width: 960px) {
            .hero-grid-phi {
                grid-template-columns: 1.2fr 1fr;
                gap: 16px;
                align-items: end;
            }
        }
        @media (min-width: 1280px) {
            .hero-grid-phi {
                grid-template-columns: 1.3fr 1fr;
                gap: 24px;
            }
        }

        /* ── Observatory arc — phi-ratio bezier from headline to card ── */
        .hero-arc {
            position: absolute;
            left: 50%;
            top: 12%;
            transform: translateX(-50%);
            width: min(1100px, 92vw);
            aspect-ratio: 55 / 34;
            pointer-events: none;
            z-index: 0;
            overflow: visible;
        }
        .hero-arc .arc-line {
            stroke-width: 1;
        }
        .hero-arc .arc-star {
            fill: #FB923C;
            filter: drop-shadow(0 0 5px rgba(251, 146, 60, 0.6));
        }
        .hero-arc .arc-star-halo {
            fill: #FB923C;
            filter: drop-shadow(0 0 22px rgba(251, 146, 60, 1.0))
                    drop-shadow(0 0 8px rgba(255, 200, 100, 0.8));
        }
        [data-theme="light"] .hero-arc .arc-line {
            filter: brightness(0.85) saturate(1.3);
        }
        [data-theme="light"] .hero-arc .arc-star {
            fill: #d4700a;
            filter: drop-shadow(0 0 5px rgba(212, 112, 10, 0.5));
        }
        [data-theme="light"] .hero-arc .arc-star-halo {
            fill: #d4700a;
            filter: drop-shadow(0 0 18px rgba(212, 112, 10, 0.8))
                    drop-shadow(0 0 6px rgba(240, 180, 80, 0.6));
        }
        @media (min-width: 960px) {
            .hero-arc { top: 6%; width: min(1050px, 90vw); }
        }
        @media (max-width: 959px) {
            .hero-arc { width: min(600px, 95vw); top: 8%; }
        }

        /* ── Fixed sky gradient ── */
        /* Default = dark mode (observatory_dawn_blue original) */
        .dawn-sky {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            transition: background 0.6s ease;
            background: linear-gradient(to bottom,
                #0B1221 0%,
                #1e293b 40%,
                #3e4c5f 70%,
                #8c5e45 100%);
        }

        /* Light = cool pre-dawn sky: blue-gray zenith → lavender → rose → warm gold horizon */
        [data-theme="light"] .dawn-sky {
            background: linear-gradient(180deg,
                #dfe8f3 0%,
                #e2dff0 25%,
                #f0e4e0 55%,
                #f5dbc4 80%,
                #edc9a0 100%);
        }

        /* ── Scroll-driven warm overlay ── */
        /* Fades in as user scrolls — dramatically warmer than base */
        .dawn-sky-warm {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            opacity: 0;
            background: linear-gradient(to bottom,
                rgba(26, 16, 24, 0.0) 0%,
                rgba(74, 32, 16, 0.35) 35%,
                rgba(160, 80, 32, 0.45) 65%,
                rgba(208, 104, 32, 0.5) 100%);
        }

        /* Light: gentle sunrise warmth — top stays transparent to preserve cool zenith */
        [data-theme="light"] .dawn-sky-warm {
            background: linear-gradient(180deg,
                rgba(245, 228, 210, 0.0) 0%,
                rgba(248, 215, 175, 0.4) 30%,
                rgba(245, 195, 130, 0.5) 60%,
                rgba(235, 175, 100, 0.6) 100%);
        }

        /* ── Star field ── */
        .star {
            position: absolute;
            border-radius: 50%;
            background: #fff;
            pointer-events: none;
            opacity: 0;
            box-shadow: 0 0 3px rgba(255, 255, 255, 0.8);
            animation: twinkle var(--dur, 3s) ease-in-out infinite;
            animation-delay: var(--delay, 0s);
        }

        /* Light: hide star dots entirely — cross-marks carry the atmosphere */
        [data-theme="light"] .star {
            display: none;
        }

        @keyframes twinkle {
            0% { opacity: 0; transform: scale(0.5); }
            50% { opacity: var(--max-opacity, 0.7); transform: scale(1); }
            100% { opacity: 0; transform: scale(0.5); }
        }

        /* ── Flashing crosses ── */
        .cross-mark {
            position: absolute;
            width: var(--size, 10px);
            height: var(--size, 10px);
            pointer-events: none;
            animation: cross-flash var(--dur, 8s) ease-in-out infinite;
            animation-delay: var(--delay, 0s);
        }

        .cross-mark::before, .cross-mark::after {
            content: '';
            position: absolute;
            background: #FB923C;
            opacity: 0.5;
        }

        .cross-mark::before {
            left: 50%; top: 0; width: 1px; height: 100%;
            transform: translateX(-50%);
        }

        .cross-mark::after {
            top: 50%; left: 0; width: 100%; height: 1px;
            transform: translateY(-50%);
        }

        /* Light: cross-marks are the atmospheric effect — slowly rotating, breathing.
           Two color temperatures: warm amber (default) and cool white (odd children).
           White ones sparkle on the cool upper gradient, amber ones glow on the warm lower. */
        [data-theme="light"] .cross-mark {
            animation: reticle-breathe var(--dur, 8s) ease-in-out infinite;
            animation-delay: var(--delay, 0s);
            width: calc(var(--size, 10px) * 1.3);
            height: calc(var(--size, 10px) * 1.3);
        }
        /* Default: warm amber arms */
        [data-theme="light"] .cross-mark::before,
        [data-theme="light"] .cross-mark::after {
            background: rgba(180, 135, 70, 0.55);
            opacity: 1;
        }
        /* Odd crosses: cool white — reads as glinting light on the blue-lavender sky */
        [data-theme="light"] .cross-mark:nth-child(odd)::before,
        [data-theme="light"] .cross-mark:nth-child(odd)::after {
            background: rgba(255, 255, 255, 0.7);
        }

        @keyframes reticle-breathe {
            0%   { opacity: 0.12; transform: rotate(0deg); }
            30%  { opacity: 0.45; transform: rotate(5deg); }
            50%  { opacity: 0.6;  transform: rotate(8deg); }
            70%  { opacity: 0.4;  transform: rotate(11deg); }
            100% { opacity: 0.12; transform: rotate(15deg); }
        }

        @keyframes cross-flash {
            0%, 90%, 100% { opacity: 0; }
            5%, 8% { opacity: 0.9; }
        }

        /* ── Film grain overlay ── */
        .grain-overlay {
            position: fixed;
            inset: 0;
            opacity: 0.02;
            pointer-events: none;
            z-index: 100;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        }

        [data-theme="light"] .grain-overlay {
            opacity: 0.06;
            mix-blend-mode: multiply;
        }

        /* ── Mobile layout (<768px — single column) ── */
        @media (max-width: 767px) {
            .hero-section-mobile {
                min-height: auto !important;
                align-items: flex-start !important;
                padding-top: 5rem !important;
                padding-bottom: 3rem !important;
            }
            /* Override grid → flex so negative margins collapse space */
            .hero-grid-phi {
                display: flex !important;
                flex-direction: column;
                gap: 0;
            }
            /* Pull right column up — flat value avoids drift from headline shrink.
               max() eases to 0 below ~417px for very small screens. */
            .hero-right-col {
                margin-top: max(-6rem, calc(-20vw + 2rem));
            }
        }

        /* ── Small device performance (<960px) ── */
        @media (max-width: 959px) {
            /* Grain: lighter touch */
            .grain-overlay {
                opacity: 0.015;
            }
            /* Parallax: disabled */
            #starfield-fixed {
                transform: none !important;
            }
            /* Mystic cards: opaque fallback (saves compositing) */
            .mystic-card {
                backdrop-filter: none;
                -webkit-backdrop-filter: none;
                background: rgba(15, 23, 42, 0.92);
            }
        }
        /* Light mode opaque fallbacks */
        @media (max-width: 959px) {
            [data-theme="light"] .mystic-card {
                backdrop-filter: none;
                -webkit-backdrop-filter: none;
                background: rgba(255, 255, 255, 0.92);
            }
        }

        /* ── Glass morphism panels ── */
        .mystic-card {
            background: rgba(15, 23, 42, 0.35);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1);
        }

        .mystic-card:hover {
            border-color: #FB923C;
            box-shadow: 0 20px 40px -10px rgba(154, 52, 18, 0.25);
            transform: translateY(-4px);
            background: rgba(15, 23, 42, 0.5);
        }

        [data-theme="light"] .mystic-card {
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(140, 130, 150, 0.15);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 4px 20px -4px rgba(100, 80, 60, 0.08);
        }

        [data-theme="light"] .mystic-card:hover {
            border-color: #c87a3e;
            box-shadow: 0 20px 40px -10px rgba(200, 122, 62, 0.18);
            background: rgba(255, 255, 255, 0.8);
        }

        /* ── Card preview interiors ── */
        /* Light mode: softer background so previews don't punch dark holes */
        [data-theme="light"] .card-preview {
            background: #e8e4ee;
            border-color: rgba(100, 90, 120, 0.1);
        }

        /* ── Terminal code block (always dark) ── */
        .terminal-window {
            background: #020617;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 0 1px #000, 0 20px 50px -10px rgba(0, 0, 0, 0.7);
        }

        [data-theme="light"] .terminal-window {
            background: #1e293b;
            border: 1px solid rgba(140, 120, 90, 0.45);
            border-radius: 4px;
            box-shadow:
                0 1px 2px 0 rgba(60, 40, 15, 0.08),
                0 4px 20px rgba(80, 55, 20, 0.14);
        }

        /* ── Showcase card — floating celestial artifact, activated by star arc ── */
        .showcase-card {
            --card-rotate: -8deg;
            /* Indicator color tokens (themed via custom properties) */
            --indicator-active: #FB923C;
            --indicator-dim: #475569;
            --indicator-active-bg: rgba(251,146,60,0.08);
            --indicator-active-border: rgba(251,146,60,0.3);
            --indicator-dim-bg: rgba(100,116,139,0.08);
            --indicator-dim-border: rgba(71,85,105,0.3);
            position: relative;
            width: 260px;
            border-radius: 6px;
            transform: rotate(var(--card-rotate));

            /* Glassmorphism: frosted dark glass */
            background: rgba(8, 14, 32, 0.72);
            backdrop-filter: blur(20px) saturate(0.7);
            -webkit-backdrop-filter: blur(20px) saturate(0.7);

            /* Orange ring — visible from entrance */
            border: 1px solid rgba(251, 146, 60, 0.25);

            /* Float shadow + champagne glow (distinct from orange accent) */
            box-shadow:
                0 0 24px 2px rgba(255, 225, 180, 0.2),
                0 0 48px 4px rgba(255, 200, 140, 0.08),
                0 8px 32px -8px rgba(0, 0, 0, 0.5),
                0 0 0 0.5px rgba(251, 146, 60, 0.15);

            /* Powered-down state: desaturated, dimmed */
            filter: saturate(0.5) brightness(0.85);

            /* Activation ignite — star reaches card ~75% through arc
               arc_begin(0.3) + arc_dur(1.4) * 0.75 ≈ 1.35s → 1.4s */
            animation: card-ignite 1.4s cubic-bezier(0.22, 1, 0.36, 1) 1.4s both;

            transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
            z-index: 20;
        }

        /* Localized grain texture on the card itself */
        .showcase-card::before {
            content: '';
            position: absolute;
            inset: 0;
            opacity: 0.12;
            pointer-events: none;
            border-radius: inherit;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
            mix-blend-mode: overlay;
            z-index: 1;
        }

        /* Radial glow aura behind the card — blooms on activation */
        .showcase-card::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 180%;
            height: 180%;
            transform: translate(-50%, -50%);
            background: radial-gradient(ellipse at center,
                rgba(255, 225, 180, 0.0) 0%,
                rgba(255, 225, 180, 0.0) 100%);
            border-radius: 50%;
            pointer-events: none;
            z-index: -1;
            animation: aura-bloom 1.4s cubic-bezier(0.22, 1, 0.36, 1) 1.4s both;
        }

        /* ── Dark mode ignite: dormant → flash → warm glow ── */
        /* Uses individual `scale` property so it doesn't conflict with
           per-breakpoint `transform: rotate(var(--card-rotate))` */
        @keyframes card-ignite {
            0% {
                filter: saturate(0.5) brightness(0.85);
                border-color: rgba(251, 146, 60, 0.25);
                box-shadow:
                    0 0 24px 2px rgba(255, 225, 180, 0.2),
                    0 0 48px 4px rgba(255, 200, 140, 0.08),
                    0 8px 32px -8px rgba(0, 0, 0, 0.5),
                    0 0 0 0.5px rgba(251, 146, 60, 0.15);
                scale: 1;
            }
            25% {
                /* Star impact — scale punch + white-hot glow */
                filter: saturate(1.3) brightness(1.15);
                border-color: rgba(251, 146, 60, 0.5);
                box-shadow:
                    0 0 40px 4px rgba(255, 235, 200, 0.4),
                    0 0 80px 8px rgba(255, 210, 160, 0.18),
                    0 8px 32px -8px rgba(0, 0, 0, 0.4),
                    inset 0 0 20px rgba(255, 230, 190, 0.08);
                scale: 1.03;
            }
            50% {
                /* Overshoot warmth — settling */
                filter: saturate(1.1) brightness(1.05);
                border-color: rgba(251, 146, 60, 0.35);
                box-shadow:
                    0 0 24px 2px rgba(255, 225, 180, 0.22),
                    0 0 48px 4px rgba(255, 200, 140, 0.1),
                    0 8px 32px -8px rgba(0, 0, 0, 0.35);
                scale: 1;
            }
            100% {
                /* Settle — warm and alive, not screaming */
                filter: saturate(1) brightness(1);
                border-color: rgba(251, 146, 60, 0.25);
                box-shadow:
                    0 0 18px 1px rgba(255, 225, 180, 0.14),
                    0 0 40px 2px rgba(255, 200, 140, 0.06),
                    0 8px 32px -8px rgba(0, 0, 0, 0.35),
                    0 0 0 0.5px rgba(251, 146, 60, 0.2);
                scale: 1;
            }
        }

        @keyframes aura-bloom {
            0%   {
                background: radial-gradient(ellipse at center,
                    rgba(255, 225, 180, 0.0) 0%,
                    rgba(255, 225, 180, 0.0) 100%);
            }
            30%  {
                background: radial-gradient(ellipse at center,
                    rgba(255, 225, 180, 0.14) 0%,
                    rgba(255, 200, 140, 0.0) 70%);
            }
            100% {
                background: radial-gradient(ellipse at center,
                    rgba(255, 225, 180, 0.05) 0%,
                    rgba(255, 200, 140, 0.0) 70%);
            }
        }

        /* ── Pulse ring — emanates from card on star impact ── */
        .showcase-pulse-ring {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            border: 1.5px solid rgba(255, 225, 180, 0.6);
            transform: translate(-50%, -50%);
            pointer-events: none;
            opacity: 0;
            z-index: -1;
            animation: pulse-expand 1s cubic-bezier(0.22, 1, 0.36, 1) 1.4s both;
        }

        @keyframes pulse-expand {
            0%   { width: 0;     height: 0;     opacity: 0.8; border-color: rgba(255, 225, 180, 0.8); }
            60%  { width: 120px; height: 120px; opacity: 0.3; border-color: rgba(255, 210, 160, 0.3); }
            100% { width: 180px; height: 180px; opacity: 0;   border-color: rgba(255, 210, 160, 0); }
        }

        /* ── Energy flash — directional light burst inside card ── */
        .showcase-flash {
            position: absolute;
            inset: 0;
            border-radius: 6px;
            pointer-events: none;
            opacity: 0;
            z-index: 10;
            animation: energy-flash 0.6s ease-out 1.4s both;
        }

        @keyframes energy-flash {
            0%  {
                opacity: 0;
                background: radial-gradient(
                    ellipse at 80% 30%,
                    rgba(255, 245, 220, 0.6) 0%,
                    rgba(255, 210, 160, 0.2) 40%,
                    transparent 70%
                );
            }
            30% { opacity: 1; }
            100% {
                opacity: 0;
                background: radial-gradient(
                    ellipse at 50% 50%,
                    rgba(255, 225, 180, 0.1) 0%,
                    transparent 60%
                );
            }
        }

        /* ── Light mode showcase card — warm brass instrument on cool dawn ── */
        /* Material warmth, not light emission. The card itself warms up. */
        [data-theme="light"] .showcase-card {
            /* Themed indicator tokens */
            --indicator-active: #9A4E1C;
            --indicator-dim: #a8a095;
            --indicator-active-bg: rgba(154,78,28,0.10);
            --indicator-active-border: rgba(154,78,28,0.30);
            --indicator-dim-bg: rgba(148,137,122,0.08);
            --indicator-dim-border: rgba(148,137,122,0.20);
            /* Opaque, cool-ish white when dormant — warms up on ignite */
            background: rgba(245, 243, 240, 1.0);
            backdrop-filter: none;
            -webkit-backdrop-filter: none;
            /* Muted border when off — warm-neutral, not orange */
            border: 1px solid rgba(170, 160, 150, 0.25);
            /* Tight lift shadow only — no outward emission */
            box-shadow:
                0 1px 8px -2px rgba(80, 70, 60, 0.12),
                0 0 0 1px rgba(170, 160, 150, 0.10);
            /* Override dark mode's base filter — cool overlay handles desaturation */
            filter: none;
            animation-name: card-ignite-light;
        }
        [data-theme="light"] .showcase-card::before {
            opacity: 0.05;
            mix-blend-mode: multiply;
        }
        /* Light mode: no aura halo — warmth lives IN the card, not around it */
        [data-theme="light"] .showcase-card::after {
            display: none;
        }
        /* Card text: warm brown tones like engraved brass */
        [data-theme="light"] .showcase-card .showcase-card-title {
            color: #5a4838;
        }
        [data-theme="light"] .showcase-card p {
            color: #5a4d3e;
        }
        [data-theme="light"] .showcase-card .text-\\[9px\\] {
            color: #5a4838;
        }
        /* ── Aperture slider — brass observatory dial ── */
        .aperture-slider {
            -webkit-appearance: none;
            appearance: none;
            height: 4px;
            border-radius: 2px;
            background: linear-gradient(90deg, #1e293b 0%, #334155 100%);
            outline: none;
            cursor: pointer;
            position: relative;
            z-index: 2;
        }
        .aperture-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #FB923C;
            cursor: pointer;
            box-shadow: 0 0 8px rgba(251, 146, 60, 0.5), 0 1px 3px rgba(0,0,0,0.4);
        }
        .aperture-slider::-moz-range-thumb {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #FB923C;
            cursor: pointer;
            border: none;
            box-shadow: 0 0 8px rgba(251, 146, 60, 0.5), 0 1px 3px rgba(0,0,0,0.4);
        }
        [data-theme="light"] .aperture-slider {
            background: linear-gradient(90deg, #d8cfc0 0%, #c8b9a4 100%);
        }
        [data-theme="light"] .aperture-slider::-webkit-slider-thumb {
            background: #8B6D4C;
            box-shadow: 0 1px 4px rgba(80, 55, 20, 0.3), 0 0 0 2px rgba(139, 109, 76, 0.12);
        }
        [data-theme="light"] .aperture-slider::-moz-range-thumb {
            background: #8B6D4C;
            box-shadow: 0 1px 4px rgba(80, 55, 20, 0.3), 0 0 0 2px rgba(139, 109, 76, 0.12);
        }
        /* Light: pulse ring — warm-neutral, not orange */
        [data-theme="light"] .showcase-pulse-ring {
            border-color: rgba(165, 140, 100, 0.5);
            border-width: 1.5px;
            box-shadow: none;
            animation-name: pulse-expand-light;
        }

        @keyframes pulse-expand-light {
            0%   {
                width: 0; height: 0;
                opacity: 0.7;
                border-color: rgba(165, 140, 100, 0.6);
                box-shadow: none;
            }
            60%  {
                width: 130px; height: 130px;
                opacity: 0.25;
                border-color: rgba(165, 140, 100, 0.25);
                box-shadow: none;
            }
            100% {
                width: 200px; height: 200px;
                opacity: 0;
                border-color: rgba(165, 140, 100, 0);
                box-shadow: none;
            }
        }
        [data-theme="light"] .showcase-flash {
            animation-name: energy-flash-light;
        }

        @keyframes card-ignite-light {
            /* Filter is handled by the .aperture-cool overlay (reacts to slider).
               This animation only handles bg, border, shadow, scale. */
            0% {
                background: rgba(245, 243, 240, 1.0);
                border-color: rgba(170, 160, 150, 0.25);
                box-shadow:
                    0 1px 8px -2px rgba(80, 70, 60, 0.12),
                    0 0 0 1px rgba(170, 160, 150, 0.10);
                scale: 1;
            }
            25% {
                background: rgba(255, 248, 235, 1.0);
                border-color: rgba(175, 140, 100, 0.45);
                box-shadow:
                    inset 0 1px 6px 0 rgba(230, 180, 100, 0.30),
                    inset 0 0 20px 0 rgba(220, 165, 80, 0.10),
                    0 4px 16px -4px rgba(80, 55, 20, 0.22),
                    0 1px 3px 0 rgba(80, 55, 20, 0.12);
                scale: 1.03;
            }
            50% {
                background: rgba(255, 250, 240, 1.0);
                border-color: rgba(170, 145, 115, 0.38);
                box-shadow:
                    inset 0 1px 3px 0 rgba(225, 175, 95, 0.20),
                    inset 0 0 12px 0 rgba(215, 160, 75, 0.06),
                    0 3px 14px -4px rgba(80, 55, 20, 0.20),
                    0 1px 3px 0 rgba(80, 55, 20, 0.10);
                scale: 1;
            }
            100% {
                background: rgba(255, 250, 240, 1.0);
                border-color: rgba(165, 145, 120, 0.38);
                box-shadow:
                    inset 0 1px 0 0 rgba(255, 240, 210, 0.5),
                    inset 0 -1px 0 0 rgba(170, 150, 120, 0.12),
                    0 4px 16px -4px rgba(80, 55, 20, 0.22),
                    0 1px 3px 0 rgba(80, 55, 20, 0.12),
                    0 0 0 1px rgba(165, 145, 120, 0.12);
                scale: 1;
            }
        }

        @keyframes energy-flash-light {
            0%  {
                opacity: 0;
                background: radial-gradient(
                    ellipse at 75% 30%,
                    rgba(255, 235, 200, 0.85) 0%,
                    rgba(200, 145, 60, 0.4) 35%,
                    rgba(180, 120, 50, 0.15) 60%,
                    transparent 75%
                );
            }
            25% {
                /* Peak flash — fully opaque, warm amber washes across the card */
                opacity: 1;
            }
            50% {
                opacity: 0.5;
                background: radial-gradient(
                    ellipse at 55% 45%,
                    rgba(220, 170, 90, 0.3) 0%,
                    rgba(200, 145, 60, 0.1) 50%,
                    transparent 70%
                );
            }
            100% {
                opacity: 0;
                background: radial-gradient(
                    ellipse at 50% 50%,
                    rgba(200, 145, 60, 0.05) 0%,
                    transparent 60%
                );
            }
        }


        /* ── Aperture reactive glow overlay ── */
        /* Dark: champagne radiance emanates from card */
        .aperture-glow {
            box-shadow:
                0 0 50px 8px rgba(255, 225, 180, 0.4),
                0 0 100px 16px rgba(255, 200, 140, 0.18),
                0 0 150px 24px rgba(255, 200, 140, 0.06);
        }
        /* Light: direct warmth — no blend mode tricks.
           Warm border ring + warm atmospheric shadow + surface tint.
           At aperture 0 (opacity 0): invisible. At 100 (opacity 1): clearly warm. */
        [data-theme="light"] .aperture-glow {
            background: rgba(210, 170, 110, 0.15);
            border: 1.5px solid rgba(175, 130, 65, 0.45);
            border-radius: inherit;
            box-shadow:
                0 0 20px 4px rgba(175, 130, 60, 0.16),
                0 8px 28px -6px rgba(120, 80, 30, 0.24),
                0 1px 4px 0 rgba(100, 65, 20, 0.10);
        }

        /* ── Aperture cool overlay — desaturates card at low aperture ── */
        /* Fades OUT as aperture rises: opacity = 1 - (aperture/100).
           At 0%: fully visible = card looks gray/dormant.
           At 100%: invisible = card shows full warm color.
           Dark mode: hidden (glow system handles everything). */
        .aperture-cool {
            display: none;
        }
        [data-theme="light"] .aperture-cool {
            display: block;
            backdrop-filter: grayscale(0.4) brightness(0.90) saturate(0.5);
            -webkit-backdrop-filter: grayscale(0.4) brightness(0.90) saturate(0.5);
        }

        /* ── Star ornament before QUICKSTART label ── */
        .showcase-label {
            position: relative;
        }
        .showcase-label::before {
            content: '';
            position: absolute;
            left: -16px;
            top: 2px;
            width: 10px;
            height: 10px;
            background: #FB923C;
            clip-path: polygon(50% 0%, 60% 40%, 100% 50%, 60% 60%, 50% 100%, 40% 60%, 0% 50%, 40% 40%);
            opacity: 0.7;
            animation: star-breathe 4s ease-in-out infinite;
        }

        /* ── Light mode: QUICKSTART label system ── */
        /* Cool slate on warm bg = hue contrast (mirrors orange-on-navy in dark mode) */
        [data-theme="light"] .showcase-label .text-sunset {
            color: #3e4255;
        }
        [data-theme="light"] .showcase-label::before {
            background: #3e4255;
            opacity: 0.85;
            animation: star-breathe-light 4s ease-in-out infinite;
        }
        @keyframes star-breathe-light {
            0%, 100% { opacity: 0.55; }
            50% { opacity: 0.9; }
        }
        [data-theme="light"] .showcase-label .showcase-divider-line {
            background: linear-gradient(90deg,
                rgba(62, 66, 85, 0.35) 0%,
                rgba(62, 66, 85, 0.12) 60%,
                transparent 100%) !important;
            opacity: 1;
        }
        [data-theme="light"] .showcase-label {
            margin-bottom: 1.25rem;
        }

        /* ── Card overlays terminal via terminal-group ── */
        .showcase-terminal-group {
            position: relative;
        }

        /* ── Two-column+ (768px+) — card overlaps terminal upper-right ── */
        /* Rule: card may overlap terminal's right ~60%, never the left 40% where text lives */
        /* Overlap at all two-column widths — terminal text is left-aligned, right side is empty */
        @media (min-width: 768px) {
            .showcase-card {
                --card-rotate: 7deg;
                position: absolute;
                top: -50px;
                left: 40%;
                right: -4px;
                width: auto;
                max-width: 300px;
                transform: rotate(var(--card-rotate));
                transform-origin: bottom right;
                animation: card-arc-in 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.4s both,
                           card-ignite 1.4s cubic-bezier(0.22, 1, 0.36, 1) 1.4s both;
            }
            [data-theme="light"] .showcase-card {
                animation: card-arc-in 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.4s both,
                           card-ignite-light 1.4s cubic-bezier(0.22, 1, 0.36, 1) 1.4s both;
            }
        }
        /* ── Mid-range (960px+) — card can sit a bit lower, more room ── */
        @media (min-width: 960px) {
            .showcase-card {
                top: -40px;
            }
        }
        /* ── Large desktop (1280px+) — wider card, more tilt ── */
        @media (min-width: 1280px) {
            .showcase-card {
                --card-rotate: 8deg;
                top: -35px;
                left: 35%;
                right: 0;
                max-width: 340px;
                transform: rotate(var(--card-rotate));
            }
        }

        /* ── Mobile (<768px): single-column, stacked, simplified celestial ── */
        @media (max-width: 767px) {
            .showcase-float-wrapper {
                display: flex;
                flex-direction: column;
                align-items: stretch;
                position: relative;
                transform: rotate(-1.5deg);
                max-width: min(440px, 90vw);
                margin-left: auto;
                margin-right: max(1.5rem, 8vw);
                margin-top: 1rem;
            }
            .showcase-card {
                --card-rotate: 8deg;
                position: absolute;
                bottom: calc(100% - 12px);
                right: -2.5rem;
                width: min(270px, 75%);
                max-width: 300px;
                transform: rotate(var(--card-rotate));
                transform-origin: bottom right;
                filter: saturate(0.5) brightness(0.85);
                animation: card-arc-in 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.4s both,
                           card-ignite 1.4s cubic-bezier(0.22, 1, 0.36, 1) 1.4s both;
            }
            .showcase-card::after { animation: none; }
            .showcase-pulse-ring { display: none; }
            .showcase-flash { display: none; }
            .showcase-float-wrapper .showcase-label {
                margin-bottom: 0.5rem;
            }
            .showcase-float-wrapper .terminal-window {
                font-size: 12px;
                padding: 1rem;
            }
            /* Light mode mobile: same animations as desktop */
            [data-theme="light"] .showcase-card {
                animation: card-arc-in 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.4s both,
                           card-ignite-light 1.4s cubic-bezier(0.22, 1, 0.36, 1) 1.4s both;
            }
        }

        /* ── Card arc-in — sweeps card into position along arc ── */
        /* Uses var(--card-rotate) so the final rotation matches each breakpoint */
        @keyframes card-arc-in {
            0%   { transform: rotate(calc(var(--card-rotate) - 16deg)) translate(50px, -40px) scale(0.85); opacity: 0; }
            60%  { transform: rotate(calc(var(--card-rotate) - 2deg)) translate(5px, -4px) scale(1.01); opacity: 1; }
            100% { transform: rotate(var(--card-rotate)) translate(0, 0) scale(1); opacity: 1; }
        }
        /* ── Reduced motion ── */
        @media (prefers-reduced-motion: reduce) {
            .star, .cross-mark, .star-mark { animation: none !important; }
            .star { opacity: 0.5; }
            [data-theme="light"] .cross-mark {
                opacity: 0.2;
                animation: none !important;
            }
            .cross-mark { opacity: 0; }
            .star-mark { opacity: 0.7; }
            .hero-arc .arc-star-group { display: none; }
            .showcase-card { animation: none !important; transform: rotate(var(--card-rotate)); filter: none; }
            .showcase-card::before, .showcase-card::after { animation: none !important; }
            .showcase-pulse-ring, .showcase-flash { animation: none !important; display: none; }

            [data-motion] { transition: none !important; }
            .dawn-sky, .dawn-sky-warm { transition: none !important; }
            .mystic-card { transition: none !important; }
            .btn-star { transition: none !important; }
            svg[class*="animate-pulse"] { animation: none !important; }
            #starfield-fixed { transform: none !important; }
        }

        /* ── Landing text utilities ── */
        /* Dark mode (default): light text on dark bg */
        .text-moon { color: #F8FAFC; }
        .text-moon-dim { color: #94A3B8; }
        .text-sunset { color: #FB923C; }

        /* Light mode: dark text on cool dawn bg */
        [data-theme="light"] .text-moon { color: #1e293b; }
        [data-theme="light"] .text-moon-dim { color: #475569; }
        [data-theme="light"] .text-sunset { color: #92400e; }

        /* ── CTA button ── */
        /* Dark mode: light border/text */
        .btn-star {
            border: 1px solid #F8FAFC;
            color: #F8FAFC;
            background: rgba(255, 255, 255, 0.05);
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-size: 0.7rem;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
        }

        .btn-star:hover {
            background: #F8FAFC;
            color: #0f172a;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
        }

        /* Light mode: dark border/text with frost backing */
        [data-theme="light"] .btn-star {
            border-color: #1e293b;
            color: #1e293b;
            background: rgba(255, 255, 255, 0.3);
        }

        [data-theme="light"] .btn-star:hover {
            background: #1e293b;
            color: #f8fafc;
            box-shadow: 0 0 20px rgba(30, 41, 59, 0.15);
        }

        /* ── CTA button outline variant ── */
        .btn-star-outline {
            border: 1px solid rgba(248, 250, 252, 0.3);
            color: #94A3B8;
            background: transparent;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-size: 0.7rem;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
        }

        .btn-star-outline:hover {
            border-color: #F8FAFC;
            color: #F8FAFC;
            background: rgba(255, 255, 255, 0.05);
        }

        [data-theme="light"] .btn-star-outline {
            border-color: rgba(30, 41, 59, 0.25);
            color: #475569;
            background: transparent;
        }

        [data-theme="light"] .btn-star-outline:hover {
            border-color: #1e293b;
            color: #1e293b;
            background: rgba(30, 41, 59, 0.05);
        }

        /* ── Landing header transparent variant ── */
        .landing-header {
            background: transparent !important;
            border-color: transparent !important;
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
        }

        .landing-header header {
            background: transparent !important;
            border-color: transparent !important;
        }

        .landing-header a,
        .landing-header button,
        .landing-header span {
            color: #F8FAFC;
        }

        .landing-header a:hover,
        .landing-header button:hover {
            color: #FB923C;
        }

        [data-theme="light"] .landing-header a,
        [data-theme="light"] .landing-header button,
        [data-theme="light"] .landing-header span {
            color: #1e293b;
        }

        [data-theme="light"] .landing-header a:hover,
        [data-theme="light"] .landing-header button:hover {
            color: #d4700a;
        }

        /* ── Editor panel (code block in mystic-card, no hover bounce) ── */
        .editor-panel:hover {
            transform: none;
            box-shadow: none;
        }
        [data-theme="light"] .editor-panel:hover {
            transform: none;
        }

        /* ── FIG. 01 input focus ── */
        .fig01-input:focus {
            border-color: rgba(251, 146, 60, 0.5);
            box-shadow: 0 0 0 2px rgba(251, 146, 60, 0.1);
        }
        [data-theme="light"] .fig01-input:focus {
            border-color: rgba(200, 122, 62, 0.5);
            box-shadow: 0 0 0 2px rgba(200, 122, 62, 0.1);
        }

        /* ── Component explorer ── */
        .showcase-preview {
            background: rgba(15, 23, 42, 0.35);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);

            /* Override theme tokens so StarUI components blend with
               the glass panel. BOTH bare and --color-* prefixed vars
               are needed: @theme inline makes Tailwind utilities
               resolve via bare vars (--popover), while the universal
               * { border-color } rule uses --color-border. */
            --card: rgba(255, 255, 255, 0.04);
            --card-foreground: rgba(248, 250, 252, 0.9);
            --popover: rgba(255, 255, 255, 0.04);
            --popover-foreground: rgba(248, 250, 252, 0.9);
            --foreground: rgba(248, 250, 252, 0.9);
            --background: transparent;
            --primary: oklch(0.97 0.002 250);
            --primary-foreground: oklch(0.10 0.01 250);
            --secondary: oklch(0.20 0.005 260);
            --secondary-foreground: rgba(248, 250, 252, 0.9);
            --muted: oklch(0.20 0.005 260);
            --muted-foreground: rgba(148, 163, 184, 0.7);
            --accent: oklch(0.20 0.005 260);
            --accent-foreground: rgba(248, 250, 252, 0.9);
            --border: rgba(255, 255, 255, 0.06);
            --input: rgba(255, 255, 255, 0.10);
            --ring: oklch(0.75 0.14 55);
            --destructive: oklch(0.55 0.22 27);
            --destructive-foreground: oklch(0.97 0 0);
            /* Prefixed duplicates for universal border-color rule */
            --color-border: rgba(255, 255, 255, 0.06);
            --color-input: rgba(255, 255, 255, 0.10);
        }
        [data-theme="light"] .showcase-preview {
            background: rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(140, 130, 150, 0.15);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);

            --card: white;
            --card-foreground: rgba(30, 41, 59, 0.9);
            --popover: white;
            --popover-foreground: rgba(30, 41, 59, 0.9);
            --foreground: rgba(30, 41, 59, 0.9);
            --background: white;
            --primary: oklch(0.22 0.01 255);
            --primary-foreground: oklch(0.97 0 0);
            --secondary: oklch(0.96 0 0);
            --secondary-foreground: rgba(30, 41, 59, 0.9);
            --muted: oklch(0.96 0 0);
            --muted-foreground: rgba(100, 116, 139, 0.7);
            --accent: oklch(0.96 0 0);
            --accent-foreground: rgba(30, 41, 59, 0.9);
            --border: rgba(0, 0, 0, 0.12);
            --input: oklch(0.90 0 0);
            --ring: oklch(0.55 0.14 55);
            --destructive: oklch(0.55 0.22 27);
            --destructive-foreground: oklch(0.97 0 0);
            /* Prefixed duplicates for universal border-color rule */
            --color-border: rgba(0, 0, 0, 0.12);
            --color-input: oklch(0.90 0 0);
        }

        /* Mini primitives — used by FIG. 01 preview + explorer sidebar */
        .mini-text { color: rgba(248, 250, 252, 0.9); }
        [data-theme="light"] .mini-text { color: rgba(30, 41, 59, 0.9); }

        .mini-text-dim { color: rgba(148, 163, 184, 0.7); }
        [data-theme="light"] .mini-text-dim { color: rgba(100, 116, 139, 0.7); }

        .mini-bg-secondary { background: rgba(255, 255, 255, 0.08); }
        [data-theme="light"] .mini-bg-secondary { background: rgba(0, 0, 0, 0.05); }

        .mini-border { border-color: rgba(255, 255, 255, 0.12) !important; }
        [data-theme="light"] .mini-border { border-color: rgba(0, 0, 0, 0.12) !important; }

        .mini-surface {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        [data-theme="light"] .mini-surface {
            background: white;
            border: 1px solid rgba(0, 0, 0, 0.08);
        }

        /* ── Python watermark in Why StarUI ── */
        .python-watermark {
            opacity: 0.12;
            z-index: 0;
            transition: opacity 0.5s ease;
        }
        [data-theme="light"] .python-watermark {
            opacity: 0.09;
            filter: hue-rotate(-15deg) saturate(0.6);
        }

        /* ── Why StarUI section — contrast + structure ── */

        /* Background scrim — anchors text contrast over variable gradient */
        .why-starui-section {
            background: linear-gradient(180deg,
                transparent 0%,
                rgba(11, 18, 33, 0.15) 12%,
                rgba(11, 18, 33, 0.18) 50%,
                rgba(11, 18, 33, 0.15) 88%,
                transparent 100%);
        }
        [data-theme="light"] .why-starui-section {
            background: linear-gradient(180deg,
                transparent 0%,
                rgba(255, 255, 255, 0.12) 12%,
                rgba(255, 255, 255, 0.15) 50%,
                rgba(255, 255, 255, 0.12) 88%,
                transparent 100%);
        }

        /* Vertical divider — gradient accent line (sunset→transparent) */
        @media (min-width: 768px) {
            .why-starui-left {
                border-right: 1px solid;
                border-image: linear-gradient(to bottom,
                    rgba(251, 146, 60, 0.35) 0%,
                    rgba(251, 146, 60, 0.10) 70%,
                    transparent 100%) 1;
            }
            [data-theme="light"] .why-starui-left {
                border-image: linear-gradient(to bottom,
                    rgba(146, 64, 14, 0.30) 0%,
                    rgba(146, 64, 14, 0.08) 70%,
                    transparent 100%) 1;
            }
        }

        /* Principle description left accent — themed */
        .principle-accent {
            border-left: 1px solid rgba(251, 146, 60, 0.12);
        }
        [data-theme="light"] .principle-accent {
            border-left: 1px solid rgba(120, 100, 80, 0.22);
        }

        /* Principle row hairline separators */
        .principle-row + .principle-row {
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 2.5rem;
        }
        [data-theme="light"] .principle-row + .principle-row {
            border-top: 1px solid rgba(120, 100, 80, 0.10);
        }

        /* ── Constellation section (FIG. 03) — contrast scrim ── */
        .constellation-section {
            background: linear-gradient(180deg,
                transparent 0%,
                rgba(11, 18, 33, 0.12) 12%,
                rgba(11, 18, 33, 0.15) 50%,
                rgba(11, 18, 33, 0.12) 88%,
                transparent 100%);
        }
        [data-theme="light"] .constellation-section {
            background: linear-gradient(180deg,
                transparent 0%,
                rgba(255, 255, 255, 0.10) 12%,
                rgba(255, 255, 255, 0.12) 50%,
                rgba(255, 255, 255, 0.10) 88%,
                transparent 100%);
        }

        /* ── CTA section — contrast scrim (warmest gradient zone) ── */
        .cta-section {
            background: linear-gradient(180deg,
                transparent 0%,
                rgba(11, 18, 33, 0.20) 15%,
                rgba(11, 18, 33, 0.25) 50%,
                rgba(11, 18, 33, 0.20) 85%,
                transparent 100%);
        }
        [data-theme="light"] .cta-section {
            background: linear-gradient(180deg,
                transparent 0%,
                rgba(255, 255, 255, 0.15) 15%,
                rgba(255, 255, 255, 0.20) 50%,
                rgba(255, 255, 255, 0.15) 85%,
                transparent 100%);
        }

        /* ── Section border ── */
        .section-border-top {
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        [data-theme="light"] .section-border-top {
            border-top-color: rgba(120, 100, 80, 0.18);
        }

        /* ── Header star mark hover rotation ── */
        .star-mark-header {
            transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1);
        }
        .star-mark-header:hover,
        a:hover .star-mark-header {
            transform: rotate(90deg);
        }

        /* ── Footer: Observation Log ── */
        .obs-log-repo {
            display: flex;
            align-items: baseline;
            gap: 0.75rem;
        }
        .obs-log-repo-name {
            font-family: 'Playfair Display', serif;
            font-size: 1.1rem;
        }
        .obs-log-repo-desc {
            font-family: 'Cormorant Garamond', serif;
            font-style: italic;
            font-size: 0.95rem;
        }
        .obs-log-dash {
            flex-shrink: 0;
            width: 2rem;
            height: 1px;
            background: currentColor;
            opacity: 0.2;
        }
    """)


def _generate_starfield() -> tuple:
    rng = random.Random(42)
    stars, crosses = [], []

    for i in range(150):
        # responsive: 0-79 always, 80-119 md+, 120-149 lg+
        extra = " hidden lg:block" if i >= 120 else (" hidden md:block" if i >= 80 else "")
        size = rng.random() * 2 + 1
        max_opacity = rng.random() * 0.7 + 0.3
        stars.append(Div(
            cls=f"star{extra}",
            style=(
                f"width:{size:.1f}px;height:{size:.1f}px;"
                f"left:{rng.random() * 100:.1f}%;top:{rng.random() * 100:.1f}%;"
                f"--dur:{rng.random() * 3 + 2:.1f}s;--delay:{rng.random() * 5:.1f}s;"
                f"--max-opacity:{max_opacity:.2f}"
            ),
        ))

    for i in range(50):
        # responsive: 0-19 always, 20-34 md+, 35-49 lg+
        extra = " hidden lg:block" if i >= 35 else (" hidden md:block" if i >= 20 else "")
        crosses.append(Div(
            cls=f"cross-mark{extra}",
            style=(
                f"left:{rng.random() * 100:.1f}%;top:{rng.random() * 100:.1f}%;"
                f"--size:{rng.randint(6, 13)}px;"
                f"--dur:{rng.random() * 6 + 5:.1f}s;--delay:{rng.random() * 10:.1f}s"
            ),
        ))

    return (*stars, *crosses)


def LandingLayout(
    *content,
    header: HeaderConfig | None = None,
) -> FT:
    header = header or HeaderConfig()

    return Div(
        _landing_styles(),
        # Fixed sky gradient background
        Div(cls="dawn-sky", aria_hidden="true"),
        # Scroll-driven warm overlay (opacity 0→1 as user scrolls)
        Div(
            cls="dawn-sky-warm",
            aria_hidden="true",
            data_scroll="",
            data_style_opacity=scroll.page_progress * 1.5 / 100,
        ),
        # Fixed star field (server-rendered, parallax)
        Div(
            *_generate_starfield(),
            id="starfield-fixed",
            cls="fixed inset-0 pointer-events-none z-[1]",
            aria_hidden="true",
            data_style_transform="translateY(" + scroll.y * -0.05 + "px)",
            data_style_opacity="$aperture / 100",
        ),
        # (geo-circles removed — the hero arc SVG is the sole decorative dome)
        # Film grain
        Div(cls="grain-overlay", aria_hidden="true"),
        # Header
        Div(DocsHeader(header), cls="landing-header relative z-50"),
        # Content
        Main(*content, cls="relative z-10"),
        cls="landing-page flex min-h-screen flex-col relative",
    )
