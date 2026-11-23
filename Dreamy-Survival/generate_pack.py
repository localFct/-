from pathlib import Path
from PIL import Image, ImageDraw
import json, zipfile, random, shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "build" / "Dreamy-Survival"
TEX = OUT / "textures" / "blocks"
TEX.mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "manifest.json", OUT / "manifest.json")

# Soft cottagecore palettes: base, shade, highlight, accent
PALETTES = {
 "grass_top": ((112,157,91),(83,128,75),(153,184,112),(190,199,126)),
 "grass_side": ((126,111,78),(91,113,68),(151,139,92),(103,151,83)),
 "dirt": ((132,103,75),(104,79,61),(158,126,91),(181,146,103)),
 "stone": ((139,145,139),(105,115,110),(174,177,162),(122,139,130)),
 "cobblestone": ((132,139,130),(91,103,97),(166,170,151),(113,130,117)),
 "mossy_cobblestone": ((112,139,105),(79,105,78),(151,166,119),(85,145,105)),
 "oak_planks": ((174,137,91),(132,97,64),(202,168,119),(154,116,75)),
 "spruce_planks": ((137,105,75),(100,73,53),(171,137,99),(119,87,61)),
 "birch_planks": ((211,196,151),(161,145,108),(235,222,183),(105,91,70)),
 "dark_oak_planks": ((105,79,61),(72,53,44),(137,105,77),(91,65,51)),
 "oak_log": ((157,119,76),(108,77,49),(191,151,99),(126,91,57)),
 "oak_leaves": ((92,139,82),(61,108,65),(133,170,99),(170,184,112)),
 "birch_leaves": ((125,158,91),(86,125,72),(163,184,112),(198,190,119)),
 "sand": ((218,204,153),(184,167,117),(237,225,184),(199,185,139)),
 "sandstone": ((207,186,137),(169,146,101),(231,213,166),(190,168,119)),
 "gravel": ((151,145,130),(111,108,99),(180,172,153),(130,137,127)),
 "bricks": ((171,111,91),(128,79,68),(198,140,111),(218,179,140)),
 "glass": ((179,211,202),(116,167,161),(224,239,222),(143,195,185)),
 "clay": ((157,169,163),(119,140,136),(187,192,177),(143,163,155)),
 "snow": ((221,232,226),(180,205,202),(247,249,235),(199,224,218)),
 "coal_ore": ((137,145,136),(65,72,69),(178,180,162),(60,65,63)),
 "iron_ore": ((144,146,134),(99,105,99),(183,177,154),(197,155,121)),
 "gold_ore": ((148,143,117),(94,99,86),(190,174,115),(231,190,81)),
 "diamond_ore": ((126,150,143),(78,105,102),(165,190,174),(107,211,190)),
 "emerald_ore": ((119,147,123),(72,103,82),(159,183,139),(83,194,126)),
 "lapis_ore": ((119,137,157),(73,91,119),(161,174,188),(77,119,194)),
 "redstone_ore": ((147,123,113),(93,78,75),(184,151,129),(205,95,83)),
 "obsidian": ((77,74,105),(45,46,72),(112,105,139),(127,111,166)),
 "white_wool": ((218,224,210),(178,190,181),(242,241,220),(200,215,202)),
 "terracotta": ((176,119,93),(131,83,69),(202,151,115),(154,99,79)),
}

def make_tile(name, colors, seed):
    base, shade, light, accent = colors
    rng = random.Random(seed)
    im = Image.new("RGB", (16,16), base)
    px = im.load()
    # Fine, restrained pixel grain for a hand-crafted vanilla-like finish
    for y in range(16):
        for x in range(16):
            if rng.random() < 0.18: px[x,y] = shade
            elif rng.random() < 0.12: px[x,y] = light
    d = ImageDraw.Draw(im)
    if "planks" in name:
        for y in (3,8,13):
            d.line((0,y,15,y), fill=shade)
            d.line((0,y+1,15,y+1), fill=light)
        for x,y in ((4,1),(11,5),(7,10),(2,14)):
            d.point((x,y), fill=accent)
    elif "ore" in name:
        for x,y in ((2,3),(9,2),(12,8),(5,11),(10,14)):
            d.rectangle((x,y,x+1,y+1), fill=accent)
            d.point((x,y+2 if y<13 else y-1), fill=light)
    elif "leaves" in name or name == "grass_top":
        for x,y in ((2,2),(7,4),(12,2),(4,9),(10,11),(14,14),(1,13)):
            d.point((x,y), fill=accent)
            if x+1<16: d.point((x+1,y), fill=light)
    elif name == "glass":
        d.rectangle((1,1,14,14), outline=light)
        d.line((2,3,5,1), fill=(238,247,232))
        d.line((10,14,14,10), fill=shade)
    elif name in ("stone","cobblestone","mossy_cobblestone","gravel"):
        for x,y in ((1,2),(8,1),(12,5),(4,8),(10,11),(2,14)):
            d.rectangle((x,y,x+2,y+1), fill=accent)
    elif name in ("oak_log",):
        d.rectangle((2,2,13,13), outline=shade)
        d.rectangle((4,4,11,11), outline=light)
        d.rectangle((6,6,9,9), fill=accent)
    elif name == "bricks":
        for y in (4,9,14): d.line((0,y,15,y), fill=shade)
        d.line((7,0,7,4), fill=shade); d.line((3,5,3,9), fill=shade); d.line((11,10,11,14), fill=shade)
    elif name == "snow":
        for x,y in ((2,3),(6,8),(12,4),(9,13)): d.point((x,y), fill=accent)
    else:
        for x,y in ((3,4),(11,2),(7,12)): d.point((x,y), fill=accent)
    im.save(TEX / f"{name}.png", optimize=True)

for i,(name,palette) in enumerate(PALETTES.items()):
    make_tile(name, palette, 2600+i)

# A tiny pack icon makes the pack easy to spot in the Bedrock menu.
icon = Image.new("RGBA",(128,128),(220,229,194,255))
d = ImageDraw.Draw(icon)
d.ellipse((22,20,106,104), fill=(117,157,94,255), outline=(78,119,74,255), width=5)
d.ellipse((55,34,74,53), fill=(231,207,144,255))
d.line((63,48,43,81), fill=(248,238,204,255), width=6)
d.line((63,48,87,79), fill=(248,238,204,255), width=6)
icon.save(OUT/"pack_icon.png")

# Zip the pack contents directly: changing the extension to .mcpack enables Android import.
archive = ROOT / "build" / "Dreamy-Survival.mcpack"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for p in OUT.rglob("*"):
        if p.is_file(): z.write(p, p.relative_to(OUT).as_posix())
print(f"Created {archive} with {len(PALETTES)} block textures")
