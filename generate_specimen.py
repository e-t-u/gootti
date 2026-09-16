#!/usr/bin/env python3
"""
Generate vector PDF and high-res PNG specimen test sheets for the Gootti font.
"""

import os
import shutil
import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

def render_specimen(pdf_path, png_path, sample_abc_path=None):
    width_pt = 842   # A4 landscape width (595 x 842 pt)
    height_pt = 595  # A4 landscape height
    
    # 1. Render Vector PDF
    surface = cairo.PDFSurface(pdf_path, width_pt, height_pt)
    cr = cairo.Context(surface)
    draw_content(cr, width_pt, height_pt)
    surface.show_page()
    surface.finish()
    print(f"Generated vector PDF: {pdf_path}")
    
    # 2. Render High-Res PNG (1684x1190 at 2x scale / ~144 DPI)
    scale = 2.0
    img_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width_pt * scale), int(height_pt * scale))
    img_cr = cairo.Context(img_surface)
    img_cr.scale(scale, scale)
    draw_content(img_cr, width_pt, height_pt)
    img_surface.write_to_png(png_path)
    print(f"Generated PNG specimen: {png_path}")
    
    if sample_abc_path:
        shutil.copyfile(png_path, sample_abc_path)
        print(f"Updated repository sample: {sample_abc_path}")

def draw_content(cr, width, height):
    # Background
    cr.set_source_rgb(0.99, 0.99, 0.99)
    cr.paint()
    
    margin_x = 45
    y = 28
    
    # Header sans font
    cr.set_source_rgb(0.2, 0.2, 0.2)
    layout = PangoCairo.create_layout(cr)
    sans_desc = Pango.FontDescription('Sans 8')
    layout.set_font_description(sans_desc)
    layout.set_text("GOOTTI (GOTHIC HANDWRITING FONT) — TEST SPECIMEN | POSTSCRIPT / OPENTYPE / TRUETYPE (EM-SIZE: 1000)", -1)
    cr.move_to(margin_x, y)
    PangoCairo.show_layout(cr, layout)
    y += 16
    
    # Rule
    cr.set_source_rgb(0.8, 0.8, 0.8)
    cr.set_line_width(0.5)
    cr.move_to(margin_x, y)
    cr.line_to(width - margin_x, y)
    cr.stroke()
    y += 14
    
    def section_header(title):
        nonlocal y
        cr.set_source_rgb(0.45, 0.45, 0.45)
        layout.set_font_description(Pango.FontDescription('Sans Bold 7'))
        layout.set_text(title, -1)
        cr.move_to(margin_x, y)
        PangoCairo.show_layout(cr, layout)
        y += 10

    # Section 1: Clean Capitals
    section_header("1. CLEAN CAPITALS (A, B, C, D, E, F)")
    cr.set_source_rgb(0.05, 0.05, 0.05)
    layout.set_font_description(Pango.FontDescription('gootti 32'))
    layout.set_text("A     B     C     D     E     F", -1)
    cr.move_to(margin_x, y)
    PangoCairo.show_layout(cr, layout)
    y += 42

    # Section 2: Cursive Connections
    section_header("2. CURSIVE CAPITAL CONNECTIONS")
    layout.set_font_description(Pango.FontDescription('gootti 20'))
    
    lines_s2 = [
        "Aa  Ab  Ac  Ad  Ae  Af        Ba  Bb  Bc  Bd  Be  Bf",
        "Ca  Cb  Cc  Cd  Ce  Cf        Da  Db  Dc  Dd  De  Df",
        "Ea  Eb  Ec  Ed  Ee  Ef        Fa  Fb  Fc  Fd  Fe  Ff"
    ]
    for line in lines_s2:
        layout.set_text(line, -1)
        cr.move_to(margin_x, y)
        PangoCairo.show_layout(cr, layout)
        y += 24
    y += 6

    # Section 3: Lowercase
    section_header("3. LOWERCASE ALPHABET (a–z)")
    layout.set_font_description(Pango.FontDescription('gootti 21'))
    layout.set_text("a b c d e f g h i j k l m   /   n o p q r s t u v w x y z", -1)
    cr.move_to(margin_x, y)
    PangoCairo.show_layout(cr, layout)
    y += 44

    # Section 4: Historical Names
    section_header("4. HISTORICAL NORDIC & GERMAN NAMES (CAPITALS A–F)")
    layout.set_font_description(Pango.FontDescription('gootti 20'))
    lines_s4 = [
        "Adam  Albert  Bernhard  Carl  David  Daniel  Elias  Erik",
        "Fabian  Franz  Fredric  Anna  Beata  Brita  Cecilia  Catharina",
        "Dorothea  Elisabeth  Fredrika"
    ]
    for line in lines_s4:
        layout.set_text(line, -1)
        cr.move_to(margin_x, y)
        PangoCairo.show_layout(cr, layout)
        y += 24
    y += 6

    # Section 5: Running script samples
    section_header("5. CHURCH RECORD SAMPLES & PANGRAMS")
    layout.set_font_description(Pango.FontDescription('gootti 20'))
    lines_s5 = [
        "Anno domini kastetut ja syntyneet lapset Daniel Elias Fredrik",
        "syntynyt kastettu kuollut vihitty haudattu kirkonkirja",
        "David and Franz saw the quick brown fox jump over a lazy dog"
    ]
    for line in lines_s5:
        layout.set_text(line, -1)
        cr.move_to(margin_x, y)
        PangoCairo.show_layout(cr, layout)
        y += 24
    y += 8

    # Section 6: Size waterfall
    section_header("6. WATERFALL HIERARCHY")
    for size in [19, 15, 12]:
        layout.set_font_description(Pango.FontDescription(f'gootti {size}'))
        layout.set_text(f"Carl Erik went back to fetch five dozen jugs of liquid wax ({size} pt)", -1)
        cr.move_to(margin_x, y)
        PangoCairo.show_layout(cr, layout)
        y += int(size * 1.35)

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf = os.path.join(base_dir, 'test_specimen.pdf')
    png = os.path.join(base_dir, 'test_specimen.png')
    sample = os.path.join(base_dir, 'sample_abc.png')
    render_specimen(pdf, png, sample)
