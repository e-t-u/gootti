#!/usr/bin/env python3
"""
Build derived font binaries (OTF, TTF, PFB, AFM) from gootti.sfd using FontForge.
"""

import os
import shutil
import subprocess
import fontforge

def build_fonts(sfd_path="gootti.sfd", install_user_fonts=True):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sfd_file = os.path.join(base_dir, sfd_path)
    
    print(f"Opening {sfd_file}...")
    f = fontforge.open(sfd_file)
    
    otf_path = os.path.join(base_dir, "gootti.otf")
    ttf_path = os.path.join(base_dir, "gootti.ttf")
    pfb_path = os.path.join(base_dir, "gootti.pfb")
    
    print(f"Generating {otf_path}...")
    f.generate(otf_path)
    
    print(f"Generating {ttf_path}...")
    f.generate(ttf_path)
    
    print(f"Generating {pfb_path} (and AFM)...")
    f.generate(pfb_path)
    
    f.close()
    print("Derived fonts generated successfully.")
    
    if install_user_fonts:
        user_fonts_dir = os.path.expanduser("~/.local/share/fonts/gootti")
        os.makedirs(user_fonts_dir, exist_ok=True)
        for ext in ("otf", "ttf", "pfb", "afm"):
            src = os.path.join(base_dir, f"gootti.{ext}")
            if os.path.exists(src):
                shutil.copy(src, user_fonts_dir)
        subprocess.run(["fc-cache", "-f", user_fonts_dir], check=False)
        print(f"Copied fonts to {user_fonts_dir} and refreshed font cache.")

if __name__ == "__main__":
    build_fonts()
