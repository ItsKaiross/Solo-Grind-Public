"""Builds the animated GIFs and image strips used by public-readme.md.

Run from anywhere: python readme-assets/build_assets.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
PUB = ROOT.parent / "nextjs-frontend" / "public"
BG = (20, 18, 31, 255)


def flat(im, size=None):
    im = im.convert("RGBA")
    if size:
        im = im.resize(size, Image.NEAREST if im.width <= 256 else Image.LANCZOS)
    base = Image.new("RGBA", im.size, BG)
    base.alpha_composite(im)
    return base.convert("RGB")


def save_gif(frames, name, ms):
    frames[0].save(ROOT / name, save_all=True, append_images=frames[1:], duration=ms, loop=0, optimize=True)


def chibi_cell(path, row, col, cell=96):
    sheet = Image.open(path).convert("RGBA")
    w, h = sheet.width / 4, sheet.height / 8
    return sheet.crop((int(col * w), int(row * h), int((col + 1) * w), int((row + 1) * h))).resize((cell, cell), Image.LANCZOS)


def chibi_parade():
    names = ["pond-fisher", "rose-fashionista", "moonveil-ninja", "astral-sorcerer",
             "jade-pathfinder", "golden-brewmaster", "lunar-monk", "circuit-engineer-female"]
    cell = 112
    frames = []
    for f in range(4):
        canvas = Image.new("RGBA", (cell * len(names), cell), BG)
        for i, n in enumerate(names):
            canvas.alpha_composite(chibi_cell(PUB / "avatar" / "chibi" / f"{n}.png", 0, f, cell), (i * cell, 0))
        frames.append(canvas.convert("RGB"))
    save_gif(frames, "solvale-villagers.gif", 180)


def summon_parade():
    names = ["fire-wolf", "frost-fox", "leaf-panda", "spark-hare", "ghost-cat",
             "dawn-lion", "mind-octopus", "earth-golem", "dream-moth", "reef-shark"]
    cell = 96
    frames = []
    for step in ("down", "down-step"):
        canvas = Image.new("RGBA", (cell * len(names), cell), BG)
        for i, n in enumerate(names):
            im = Image.open(PUB / "summons" / "roster" / n / "stage-2" / f"{step}.png").convert("RGBA").resize((cell, cell), Image.NEAREST)
            canvas.alpha_composite(im, (i * cell, 0))
        frames.append(canvas.convert("RGB"))
    save_gif(frames, "solvale-summons.gif", 320)


def summon_evolution():
    cell = 160
    frames = []
    for stage in range(1, 6):
        for step in ("down", "down-step", "down", "down-step"):
            im = Image.open(PUB / "summons" / "roster" / "frost-fox" / f"stage-{stage}" / f"{step}.png")
            frames.append(flat(im, (cell, cell)))
    save_gif(frames, "summon-evolution.gif", 260)


def role_evolution():
    levels = [1, 10, 25, 50, 100]
    frames = []
    for role, g in (("hard-coder", "male"), ("athlete", "female"), ("musician", "male")):
        for lv in levels:
            im = Image.open(PUB / "images" / "avatars-v2" / role / g / f"level-{lv}_nobg.png").convert("RGBA")
            im.thumbnail((240, 300), Image.LANCZOS)
            canvas = Image.new("RGBA", (240, 300), BG)
            canvas.alpha_composite(im, ((240 - im.width) // 2, 300 - im.height))
            frames.append(canvas.convert("RGB"))
    save_gif(frames, "role-evolution.gif", 650)


def strip(folder, names, name, cell=180, suffix=".png"):
    canvas = Image.new("RGBA", (cell * len(names), cell), BG)
    for i, n in enumerate(names):
        im = Image.open(PUB / "images" / "shop" / folder / f"{n}{suffix}").convert("RGBA")
        im.thumbnail((cell, cell), Image.LANCZOS)
        canvas.alpha_composite(im, (i * cell + (cell - im.width) // 2, (cell - im.height) // 2))
    canvas.convert("RGB").save(ROOT / name, optimize=True)


if __name__ == "__main__":
    chibi_parade()
    summon_parade()
    summon_evolution()
    role_evolution()
    picks = ["celestial-gold", "crimson-inferno", "frost-crown", "neon-circuit", "emerald-grove", "amethyst-arcane"]
    strip("avatar-frames", picks, "cosmetic-frames.png", suffix="_nobg.png")
    strip("auras", picks, "cosmetic-auras.png", suffix="_nobg.png")
    strip("backgrounds", ["sakura-spirit", "cloud-sanctuary", "desert-oasis", "thunderfall-citadel", "ocean-relic"], "cosmetic-backgrounds.png", cell=220)
    print("done")
