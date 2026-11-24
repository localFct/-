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


# Second visual batch: transparent flower sprites, seedlings, crops, mushrooms, and item icons.
BLOCK_TEX = OUT / "textures" / "blocks"
ITEM_TEX = OUT / "textures" / "items"
BLOCK_TEX.mkdir(parents=True, exist_ok=True)
ITEM_TEX.mkdir(parents=True, exist_ok=True)

FLOWERS = {
    "dandelion": ((245,205,89,255),(255,238,153,255)),
    "poppy": ((191,83,91,255),(238,137,130,255)),
    "blue_orchid": ((117,155,220,255),(190,208,246,255)),
    "allium": ((177,135,205,255),(222,190,232,255)),
    "azure_bluet": ((218,207,183,255),(249,239,215,255)),
    "red_tulip": ((190,82,91,255),(238,141,133,255)),
    "orange_tulip": ((232,145,79,255),(250,196,122,255)),
    "white_tulip": ((232,226,207,255),(255,251,234,255)),
    "pink_tulip": ((224,151,174,255),(250,203,211,255)),
    "oxeye_daisy": ((239,232,213,255),(255,255,245,255)),
    "cornflower": ((92,137,202,255),(162,192,232,255)),
    "lily_of_the_valley": ((244,239,222,255),(255,255,247,255)),
}
for idx,(name,(petal,shine)) in enumerate(FLOWERS.items()):
    im=Image.new("RGBA",(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.line((8,8,8,15),fill=(75,130,75,255),width=1)
    d.point((7,12),fill=(105,160,91,255)); d.point((9,13),fill=(105,160,91,255))
    for xy in ((7,4),(9,4),(6,6),(8,6),(10,6),(7,8),(9,8)):
        d.point(xy,fill=petal)
    d.point((8,6),fill=shine)
    d.point((7,5),fill=shine)
    im.save(BLOCK_TEX/f"{name}.png",optimize=True)

# Tall flowers receive small, distinct transparent sprites; their silhouettes remain legible.
for name,petal in {
    "sunflower_front":(245,197,74,255),"lilac":(173,137,202,255),
    "rose_bush":(194,91,112,255),"peony":(226,151,174,255)
}.items():
    im=Image.new("RGBA",(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.line((8,5,8,15),fill=(73,128,71,255))
    d.ellipse((4,1,11,8),fill=petal)
    d.point((7,3),fill=(255,226,170,255)); d.point((10,5),fill=(255,226,170,255))
    d.point((5,10),fill=(108,159,91,255)); d.point((10,12),fill=(108,159,91,255))
    im.save(BLOCK_TEX/f"{name}.png",optimize=True)

# Saplings, sprouts, and mushrooms are transparent sprites.
for name,leaf in {
    "oak_sapling":(112,157,91,255),"spruce_sapling":(73,119,83,255),
    "birch_sapling":(153,180,105,255),"jungle_sapling":(91,151,91,255),
    "acacia_sapling":(177,157,92,255),"dark_oak_sapling":(74,112,70,255),
    "mangrove_propagule":(128,151,87,255),"cherry_sapling":(224,157,183,255),
    "azalea":(111,155,92,255),"flowering_azalea":(194,139,172,255),
    "brown_mushroom":(153,112,82,255),"red_mushroom":(194,86,88,255),
    "crimson_fungus":(151,73,91,255),"warped_fungus":(70,156,148,255),
}.items():
    im=Image.new("RGBA",(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
    if "mushroom" in name or "fungus" in name:
        d.rectangle((7,8,9,15),fill=(222,203,163,255))
        d.ellipse((3,3,12,10),fill=leaf)
        d.point((6,5),fill=(247,226,188,255))
    else:
        d.line((8,7,8,15),fill=(91,119,70,255),width=1)
        d.ellipse((4,2,10,9),fill=leaf)
        d.point((6,4),fill=(190,211,139,255))
        d.point((10,7),fill=(190,211,139,255))
    im.save(BLOCK_TEX/f"{name}.png",optimize=True)

# Crop growth stages: each stage visibly fills a little more of the tile.
for crop,green in {"wheat":(181,166,91,255),"carrots":(105,158,84,255),
                   "potatoes":(116,153,87,255),"beetroots":(132,157,87,255)}.items():
    for stage in range(8 if crop=="wheat" else 4):
        im=Image.new("RGBA",(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
        h=3+stage*1 if crop=="wheat" else 3+stage*3
        for stalk_x in (5,8,11):
            d.line((stalk_x,15,stalk_x,max(2,15-h)),fill=green,width=1)
            if stage>0:
                y=max(3,15-h//2)
                d.polygon([(stalk_x,y),(stalk_x-3,y-2),(stalk_x-1,y+1)],fill=(112,164,91,255))
                d.polygon([(stalk_x,y+2),(stalk_x+3,y),(stalk_x+1,y+3)],fill=(132,177,99,255))
        if crop=="wheat" and stage>=5:
            for stalk_x in (5,8,11):
                d.line((stalk_x,max(1,15-h),stalk_x-1,max(0,13-h)),fill=(220,194,112,255))
        im.save(BLOCK_TEX/f"{crop}_stage_{stage}.png",optimize=True)

# Soft, readable item icons (simple vanilla-sized pixel art).
ITEMS = {
 "apple": ((193,91,86,255),(236,148,111,255)),
 "golden_apple": ((221,177,79,255),(250,222,137,255)),
 "bread": ((194,145,87,255),(236,197,132,255)),
 "carrot": ((224,137,72,255),(116,160,82,255)),
 "potato": ((183,151,101,255),(220,190,135,255)),
 "beetroot": ((160,77,91,255),(205,119,126,255)),
 "sweet_berries": ((174,74,100,255),(226,130,145,255)),
 "honey_bottle": ((220,170,76,255),(250,221,143,255)),
 "diamond": ((93,190,177,255),(174,235,216,255)),
 "emerald": ((81,175,112,255),(153,224,158,255)),
 "iron_ingot": ((166,176,166,255),(224,231,213,255)),
 "gold_ingot": ((218,176,77,255),(250,224,137,255)),
 "coal": ((65,69,68,255),(118,123,113,255)),
 "stick": ((148,107,68,255),(197,153,100,255)),
}
for idx,(name,(base,light)) in enumerate(ITEMS.items()):
    im=Image.new("RGBA",(16,16),(0,0,0,0)); d=ImageDraw.Draw(im)
    if name in ("stick","carrot"):
        d.line((3,13,12,3),fill=base,width=3); d.line((4,12,12,4),fill=light,width=1)
        if name=="carrot":
            d.line((5,10,2,7),fill=(104,157,82,255),width=1)
            d.line((6,9,8,5),fill=(104,157,82,255),width=1)
    elif name=="honey_bottle":
        d.rectangle((5,3,10,5),fill=light); d.rectangle((4,6,11,13),fill=base)
        d.rectangle((5,8,10,11),fill=light); d.point((7,7),fill=(255,245,194,255))
    else:
        d.polygon([(8,1),(13,4),(14,10),(9,14),(3,12),(2,5)],fill=base)
        d.line((4,5,8,2),fill=light,width=2); d.point((10,8),fill=light)
    im.save(ITEM_TEX/f"{name}.png",optimize=True)

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


# Third batch: starter mob sheets, UV-mapped animal additions, and armor atlases.
# Existing starter sheets are retained; new animal textures use the vanilla Bedrock paths
# and model UV dimensions. Visual appearance still requires in-game verification.
ENTITY_DIR = OUT / "textures" / "entity"
ARMOR_DIR = OUT / "textures" / "models" / "armor"
ENTITY_DIR.mkdir(parents=True, exist_ok=True)
ARMOR_DIR.mkdir(parents=True, exist_ok=True)

MOB_PALETTES = {
    "cow/cow": ((116,91,76,255),(235,222,194,255),(87,67,58,255)),
    "sheep/sheep": ((224,218,197,255),(194,210,178,255),(246,238,218,255)),
    "pig/pig": ((221,160,157,255),(244,194,185,255),(180,112,119,255)),
    "chicken": ((239,230,203,255),(215,180,112,255),(192,111,91,255)),
    "wolf/wolf": ((157,160,146,255),(195,191,166,255),(104,119,111,255)),
    "cat/ocelot": ((205,164,105,255),(239,218,169,255),(112,92,72,255)),
    "fox/fox": ((205,125,79,255),(245,222,187,255),(105,81,69,255)),
    "bee/bee": ((224,178,77,255),(246,225,155,255),(84,78,67,255)),
    "horse/horse": ((132,101,78,255),(195,158,116,255),(78,66,59,255)),
    "rabbit/rabbit": ((205,183,151,255),(239,225,197,255),(139,117,99,255)),
    "turtle/turtle": ((91,132,94,255),(157,174,112,255),(64,97,76,255)),
    "axolotl_blue": ((133,172,190,255),(202,222,218,255),(92,128,151,255)),
}
for index,(name,(base,light,shade)) in enumerate(MOB_PALETTES.items()):
    rng = random.Random(7800+index)
    im = Image.new("RGBA",(64,32),base)
    px = im.load()
    for y in range(32):
        for x in range(64):
            if rng.random() < 0.12: px[x,y] = light
            elif rng.random() < 0.08: px[x,y] = shade
    d = ImageDraw.Draw(im)
    for x,y in ((5,5),(14,10),(25,4),(38,12),(51,7),(58,22),(19,25),(44,27)):
        d.point((x,y),fill=light)
    target = ENTITY_DIR/(name+".png")
    target.parent.mkdir(parents=True, exist_ok=True)
    im.save(target, optimize=True)


def draw_uv_box(im, uv, size, base, light, shade, back=None, seed=0):
    """Paint a Bedrock cuboid's six faces in its standard 64x64 UV atlas."""
    u,v = uv
    x,y,z = size
    d = ImageDraw.Draw(im)
    back = back or shade
    faces = [
        ((u+z, v, u+z+x-1, v+z-1), light),
        ((u+z+x, v, u+2*z+x-1, v+z-1), shade),
        ((u, v+z, u+z-1, v+z+y-1), shade),
        ((u+z, v+z, u+z+x-1, v+z+y-1), base),
        ((u+z+x, v+z, u+2*z+x-1, v+z+y-1), shade),
        ((u+2*z+x, v+z, u+2*z+2*x-1, v+z+y-1), back),
    ]
    for box,color in faces:
        d.rectangle(box, fill=color)
    rng = random.Random(9100 + u*1000 + v*17 + sum(size) + seed)
    px = im.load()
    for yy in range(max(0,v), min(im.height, v+z+y)):
        for xx in range(max(0,u), min(im.width, u+2*z+2*x)):
            if px[xx,yy][3] and rng.random() < 0.025:
                c = px[xx,yy]
                px[xx,yy] = (min(255,c[0]+4), min(255,c[1]+4), min(255,c[2]+4), c[3])


# Cow: 64x64 UV atlas matching geometry.cow.v2; warm cream coat and quiet cocoa patches.
cow = Image.new("RGBA",(64,64),(0,0,0,0))
cow_cream = (229,219,198,255)
cow_light = (244,235,216,255)
cow_shade = (196,181,155,255)
cow_spot = (137,111,85,255)
cow_spot_light = (163,137,108,255)
cow_spot_shade = (106,84,66,255)
draw_uv_box(cow,(18,4),(12,18,10),cow_cream,cow_light,cow_shade)
draw_uv_box(cow,(0,0),(8,8,6),cow_cream,cow_light,cow_shade)
draw_uv_box(cow,(1,33),(6,3,1),(118,91,72,255),(153,122,95,255),(87,66,53,255))
draw_uv_box(cow,(22,0),(1,3,1),cow_spot,cow_spot_light,cow_spot_shade)
draw_uv_box(cow,(0,16),(4,12,4),cow_cream,cow_light,cow_shade)
cd = ImageDraw.Draw(cow)
cd.ellipse((29,17,34,22),fill=cow_spot)
cd.ellipse((35,25,39,29),fill=cow_spot_light)
cd.ellipse((19,19,24,25),fill=cow_spot)
cd.ellipse((52,17,57,23),fill=cow_spot)
cd.rectangle((8,8,9,9),fill=cow_spot)
cd.rectangle((11,8,12,9),fill=cow_spot)
cd.rectangle((3,11,4,12),fill=cow_spot_shade)
cd.rectangle((4,29,7,31),fill=cow_spot_shade)
(ENTITY_DIR/"cow").mkdir(parents=True,exist_ok=True)
cow.save(ENTITY_DIR/"cow"/"cow_v2.png",optimize=True)


# Panda: vanilla 64x64 UV layout; cream fur, charcoal limbs, and small readable eye patches.
panda = Image.new("RGBA",(64,64),(0,0,0,0))
panda_cream = (232,224,207,255)
panda_light = (246,239,224,255)
panda_shade = (199,190,173,255)
panda_dark = (57,59,57,255)
panda_dark_light = (82,84,79,255)
panda_dark_shade = (39,42,42,255)
draw_uv_box(panda,(0,25),(19,26,13),panda_cream,panda_light,panda_shade)
draw_uv_box(panda,(0,6),(13,10,9),panda_cream,panda_light,panda_shade)
draw_uv_box(panda,(45,16),(7,5,2),panda_dark,panda_dark_light,panda_dark_shade)
draw_uv_box(panda,(52,25),(5,4,1),panda_dark,panda_dark_light,panda_dark_shade)
draw_uv_box(panda,(40,0),(6,9,6),panda_dark,panda_dark_light,panda_dark_shade)
pd = ImageDraw.Draw(panda)
pd.ellipse((10,17,14,22),fill=panda_dark)
pd.ellipse((17,17,21,22),fill=panda_dark)
pd.point((12,19),fill=panda_light)
pd.point((19,19),fill=panda_light)
pd.rectangle((14,40,17,63),fill=panda_dark)
pd.rectangle((28,40,31,63),fill=panda_dark)
pd.rectangle((1,40,4,62),fill=panda_dark_shade)
pd.rectangle((40,40,43,62),fill=panda_dark_shade)
pd.rectangle((49,20,50,21),fill=(31,34,34,255))
(ENTITY_DIR/"panda").mkdir(parents=True,exist_ok=True)
panda.save(ENTITY_DIR/"panda"/"panda.png",optimize=True)


# Goat: 64x64 UV layout; soft oat-coloured coat, darker hooves, and muted horn detail.
goat = Image.new("RGBA",(64,64),(0,0,0,0))
goat_wool = (213,199,171,255)
goat_light = (237,226,203,255)
goat_shade = (175,158,132,255)
goat_leg = (176,153,119,255)
goat_leg_light = (199,180,148,255)
goat_leg_shade = (137,116,91,255)
goat_horn = (104,83,65,255)
goat_horn_light = (145,118,91,255)
goat_horn_shade = (75,62,51,255)
draw_uv_box(goat,(1,1),(9,11,16),goat_wool,goat_light,goat_shade)
draw_uv_box(goat,(0,28),(11,14,11),goat_wool,goat_light,goat_shade)
draw_uv_box(goat,(34,46),(5,7,10),goat_wool,goat_light,goat_shade)
draw_uv_box(goat,(2,61),(3,2,1),goat_leg,goat_leg_light,goat_leg_shade)
draw_uv_box(goat,(12,55),(2,7,2),goat_horn,goat_horn_light,goat_horn_shade)
for uv,size in (((36,29),(3,6,3)),((49,29),(3,6,3)),((49,2),(3,10,3)),((35,2),(3,10,3))):
    draw_uv_box(goat,uv,size,goat_leg,goat_leg_light,goat_leg_shade)
gd = ImageDraw.Draw(goat)
gd.point((46,60),fill=(122,92,78,255))
for x,y in ((39,36),(52,36),(52,10),(38,10)):
    gd.line((x,y,x+2,y),fill=goat_horn,width=1)
(ENTITY_DIR/"goat").mkdir(parents=True,exist_ok=True)
goat.save(ENTITY_DIR/"goat"/"goat.png",optimize=True)


# Player armor: UV-aware 64x32 atlases with distinct material tones and restrained seams.
armor_palettes = {
    "leather": ((151,112,83,255),(196,157,119,255),(105,83,69,255)),
    "chainmail": ((153,169,160,255),(211,221,203,255),(104,124,119,255)),
    "iron": ((177,187,176,255),(231,234,215,255),(126,144,139,255)),
    "gold": ((207,171,83,255),(247,222,142,255),(151,119,61,255)),
    "diamond": ((108,184,168,255),(187,229,208,255),(69,133,129,255)),
    "netherite": ((105,96,105,255),(158,143,143,255),(68,66,78,255)),
}
armor_accents = {
    "leather": (231,207,165,255),
    "chainmail": (226,231,211,255),
    "iron": (205,185,143,255),
    "gold": (255,235,171,255),
    "diamond": (218,244,224,255),
    "netherite": (190,169,164,255),
}

def make_armor_atlas(material, base, light, shade, accent, layer):
    im = Image.new("RGBA",(64,32),(0,0,0,0))
    d = ImageDraw.Draw(im)
    if layer == "1":
        # Head/helmet and outer helmet UV islands.
        d.rectangle((0,0,31,15),fill=base)
        d.rectangle((32,0,63,15),fill=shade)
        d.rectangle((7,7,24,15),fill=base)
        d.rectangle((8,8,15,15),fill=light)
        d.rectangle((16,8,23,15),fill=shade)
        d.line((8,7,23,7),fill=light)
        d.line((15,8,15,15),fill=accent)
        # Torso front panel, shoulder seams, and side plates.
        d.rectangle((16,16,39,31),fill=base)
        d.rectangle((20,19,27,29),fill=light)
        d.rectangle((28,19,35,29),fill=shade)
        d.line((20,18,35,18),fill=light)
        d.line((27,20,27,30),fill=accent)
        d.line((17,17,17,30),fill=shade)
        d.line((38,17,38,30),fill=light)
        # Arm and boot islands.
        d.rectangle((40,16,55,31),fill=shade)
        d.rectangle((44,19,47,30),fill=base)
        d.line((44,18,47,18),fill=light)
        d.rectangle((0,16,15,31),fill=base)
        d.rectangle((4,20,7,29),fill=shade)
        d.rectangle((4,28,7,30),fill=accent)
        d.line((0,19,15,19),fill=light)
        # Fine pixel rivets.
        for x,y in ((10,10),(21,10),(24,23),(31,23),(45,23),(6,23),(6,26)):
            d.point((x,y),fill=accent)
    else:
        # Layer 2 is used for leggings; keep only the leg UV island opaque.
        d.rectangle((0,16,15,31),fill=base)
        d.rectangle((4,20,7,27),fill=light)
        d.rectangle((4,25,7,27),fill=shade)
        d.rectangle((4,28,7,30),fill=accent)
        d.line((0,19,15,19),fill=light)
        d.line((8,20,8,29),fill=shade)
        for x,y in ((5,22),(6,22),(5,26),(6,26)):
            d.point((x,y),fill=accent)
    return im

for material,(base,light,shade) in armor_palettes.items():
    for layer in ("1","2"):
        make_armor_atlas(material,base,light,shade,armor_accents[material],layer).save(
            ARMOR_DIR/f"{material}_{layer}.png",optimize=True
        )


# Wolf armor: vanilla 64x64 geometry UV, sage enamel plates and soft brass rivets.
wolf_armor = Image.new("RGBA",(64,64),(0,0,0,0))
armor_sage = (111,143,112,255)
armor_sage_light = (164,187,145,255)
armor_sage_shade = (75,104,82,255)
armor_brass = (213,181,111,255)
draw_uv_box(wolf_armor,(0,0),(6,6,4),armor_sage,armor_sage_light,armor_sage_shade)
draw_uv_box(wolf_armor,(18,14),(6,9,6),armor_sage,armor_sage_light,armor_sage_shade)
draw_uv_box(wolf_armor,(21,0),(8,6,7),armor_sage,armor_sage_light,armor_sage_shade)
draw_uv_box(wolf_armor,(0,18),(2,8,2),armor_sage_shade,armor_sage,armor_sage_shade)
draw_uv_box(wolf_armor,(52,5),(2,8,2),armor_sage,armor_sage_light,armor_sage_shade)
wd = ImageDraw.Draw(wolf_armor)
wd.rectangle((30,8,33,11),fill=armor_brass)
wd.line((24,23,29,23),fill=armor_brass,width=1)
wd.point((5,6),fill=armor_brass)
wd.point((55,9),fill=armor_brass)
(ENTITY_DIR/"wolf").mkdir(parents=True,exist_ok=True)
wolf_armor.save(ENTITY_DIR/"wolf"/"wolf_armor.png",optimize=True)
# Register the generated block and item images in Bedrock atlases.
terrain = {"resource_pack_name":"Dreamy Survival","texture_name":"atlas.terrain","padding":8,"num_mip_levels":4,"texture_data":{}}
for p in sorted((OUT/"textures"/"blocks").glob("*.png")):
    key = p.stem
    terrain["texture_data"][key] = {"textures": f"textures/blocks/{key}"}
(OUT/"textures"/"terrain_texture.json").write_text(json.dumps(terrain,indent=2),encoding="utf-8")

items_atlas = {"resource_pack_name":"Dreamy Survival","texture_name":"atlas.items","texture_data":{}}
for p in sorted((OUT/"textures"/"items").glob("*.png")):
    key = p.stem
    items_atlas["texture_data"][key] = {"textures": f"textures/items/{key}"}
(OUT/"textures"/"item_texture.json").write_text(json.dumps(items_atlas,indent=2),encoding="utf-8")

# Rebuild archive after all generated assets and atlas definitions have been written.
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for p in OUT.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(OUT).as_posix())
print(f"Repacked {archive}; added {len(MOB_PALETTES)} mob texture sheets and {len(armor_palettes)*2} armor atlas images.")

# Validate the generated pack before publishing the .mcpack artifact.
def validate_pack():
    manifest_path = OUT / "manifest.json"
    terrain_path = OUT / "textures" / "terrain_texture.json"
    items_path = OUT / "textures" / "item_texture.json"
    for required in (manifest_path, terrain_path, items_path, OUT / "pack_icon.png"):
        if not required.is_file():
            raise FileNotFoundError(f"Required pack file is missing: {required.relative_to(OUT)}")

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    terrain_data = json.loads(terrain_path.read_text(encoding="utf-8"))
    items_data = json.loads(items_path.read_text(encoding="utf-8"))
    if manifest_data.get("format_version") != 2 or not manifest_data.get("header", {}).get("uuid"):
        raise ValueError("manifest.json is missing a valid resource-pack header")
    for atlas_name, atlas_data, folder in (
        ("terrain", terrain_data, "blocks"),
        ("items", items_data, "items"),
    ):
        entries = atlas_data.get("texture_data", {})
        if not entries:
            raise ValueError(f"{atlas_name} texture atlas is empty")
        for key, entry in entries.items():
            texture = entry.get("textures")
            paths = texture if isinstance(texture, list) else [texture]
            for texture_path in paths:
                if not isinstance(texture_path, str) or not (OUT / f"{texture_path}.png").is_file():
                    raise FileNotFoundError(f"Atlas entry {key!r} points to missing texture: {texture_path!r}")

    png_files = list(OUT.rglob("*.png"))
    if not png_files:
        raise ValueError("No PNG textures were generated")
    for png in png_files:
        with Image.open(png) as image:
            image.verify()

    expected_sizes = {
        "textures/entity/cow/cow_v2.png": (64, 64),
        "textures/entity/panda/panda.png": (64, 64),
        "textures/entity/goat/goat.png": (64, 64),
        "textures/entity/wolf/wolf_armor.png": (64, 64),
    }
    for material in ("leather", "chainmail", "iron", "gold", "diamond", "netherite"):
        expected_sizes[f"textures/models/armor/{material}_1.png"] = (64, 32)
        expected_sizes[f"textures/models/armor/{material}_2.png"] = (64, 32)
    for relative_path, expected_size in expected_sizes.items():
        with Image.open(OUT / relative_path) as image:
            if image.size != expected_size:
                raise ValueError(f"Unexpected texture dimensions for {relative_path}: {image.size}, expected {expected_size}")

    with zipfile.ZipFile(archive, "r") as z:
        bad_member = z.testzip()
        if bad_member:
            raise ValueError(f"Corrupt file in .mcpack archive: {bad_member}")
        names = set(z.namelist())
        for required in ("manifest.json", "pack_icon.png", "textures/terrain_texture.json", "textures/item_texture.json"):
            if required not in names:
                raise ValueError(f".mcpack is missing required entry: {required}")
        expected_names = {p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
        if names != expected_names:
            raise ValueError("Archive contents do not match generated pack files")

    print(
        f"Validated .mcpack: {len(png_files)} PNG files, "
        f"{len(terrain_data['texture_data'])} terrain entries, "
        f"{len(items_data['texture_data'])} item entries."
    )


validate_pack()
