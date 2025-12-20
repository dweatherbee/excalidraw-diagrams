#!/usr/bin/env python3
"""
Export Excalidraw diagrams to SVG/PNG.

Usage:
    python export_diagram.py input.excalidraw output.svg
    python export_diagram.py input.excalidraw output.png
    python export_diagram.py input.excalidraw  # outputs input.svg

Requires: npm (uses npx excalidraw_export)
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def check_npm():
    """Check if npm/npx is available."""
    return shutil.which("npx") is not None


def export_to_svg(input_path: str, output_path: str = None) -> str:
    """
    Export an Excalidraw file to SVG.

    Args:
        input_path: Path to .excalidraw file
        output_path: Path for output SVG (optional, defaults to input.svg)

    Returns:
        Path to the created SVG file
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        output_path = input_path.with_suffix('.svg')
    else:
        output_path = Path(output_path)

    # excalidraw_export adds .excalidraw.svg, we'll rename after
    temp_output = input_path.with_suffix('.excalidraw.svg')

    # Run excalidraw_export via npx
    try:
        result = subprocess.run(
            ["npx", "excalidraw_export", str(input_path), str(output_path)],
            capture_output=True,
            text=True,
            timeout=60
        )

        # The tool creates file.excalidraw.svg, rename if needed
        if temp_output.exists() and temp_output != output_path:
            shutil.move(str(temp_output), str(output_path))

        if output_path.exists():
            return str(output_path)
        else:
            raise RuntimeError(f"Export failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        raise RuntimeError("Export timed out")
    except FileNotFoundError:
        raise RuntimeError("npx not found. Install Node.js to use export feature.")


def export_to_png(input_path: str, output_path: str = None, scale: float = 2.0) -> str:
    """
    Export an Excalidraw file to PNG.

    First exports to SVG, then converts to PNG using available tools.

    Args:
        input_path: Path to .excalidraw file
        output_path: Path for output PNG (optional)
        scale: Scale factor for PNG (default 2x for retina)

    Returns:
        Path to the created PNG file
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.with_suffix('.png')
    else:
        output_path = Path(output_path)

    # First export to SVG
    svg_path = input_path.with_suffix('.svg')
    export_to_svg(str(input_path), str(svg_path))

    # Try to convert SVG to PNG using available tools
    converters = [
        # rsvg-convert (librsvg) - best quality
        lambda: subprocess.run(
            ["rsvg-convert", "-z", str(scale), "-o", str(output_path), str(svg_path)],
            capture_output=True, check=True
        ),
        # ImageMagick convert
        lambda: subprocess.run(
            ["convert", "-density", str(int(72 * scale)), str(svg_path), str(output_path)],
            capture_output=True, check=True
        ),
        # Inkscape
        lambda: subprocess.run(
            ["inkscape", str(svg_path), f"--export-filename={output_path}",
             f"--export-dpi={int(96 * scale)}"],
            capture_output=True, check=True
        ),
    ]

    for converter in converters:
        try:
            converter()
            if output_path.exists():
                return str(output_path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    # If no converter worked, return SVG path
    print(f"Warning: Could not convert to PNG. SVG available at: {svg_path}", file=sys.stderr)
    return str(svg_path)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not check_npm():
        print("Error: npx not found. Install Node.js to use export feature.", file=sys.stderr)
        sys.exit(1)

    try:
        if output_file and output_file.endswith('.png'):
            result = export_to_png(input_file, output_file)
        else:
            result = export_to_svg(input_file, output_file)

        print(f"Exported: {result}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
