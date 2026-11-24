# Dreamy Survival 🌿

Cozy Vanilla+ / cottagecore resource-pack starter for Minecraft Bedrock on Android.

## Generated texture batches
- **Blocks (30):** grass, dirt, stone, cobblestone, mossy cobblestone, wood, leaves, sand, sandstone, gravel, bricks, glass, clay, snow, ores, wool, terracotta, obsidian.
- **Nature (50):** flower sprites, tall-flower accents, saplings, azalea, mushrooms, fungi, and crop growth-stage sprites.
- **Items (14):** apples, golden apples, bread, carrots, potatoes, beetroot, berries, honey bottle, gems, ingots, coal, and sticks.
- **Mobs (15):** 12 starter texture sheets plus UV-sized cow, panda, and goat textures placed at their vanilla Bedrock texture paths.
- **Armor (13):** six player-armor material palettes (two 64×32 UV atlas layers each) plus a 64×64 wolf-armor texture with sage enamel and brass accents.
- Custom pack icon and automated `.mcpack` build.

## Build validation
The generator checks the manifest and atlas JSON, verifies every registered texture exists, opens each PNG, checks the dimensions of the new mob and armor atlases, and tests the final ZIP archive before the workflow uploads it.

## Build
1. Open the repository's **Actions** tab.
2. Select **Build Dreamy Survival Bedrock Pack**.
3. Press **Run workflow**.
4. Download the **Dreamy-Survival-mcpack** artifact from the completed run.
5. On Android, open the downloaded `.mcpack` with Minecraft and activate it in the world's Resource Packs.

## Compatibility note
This is an expanding custom texture collection, not a complete replacement of every vanilla texture. The new cow, panda, goat, player-armor, and wolf-armor images follow the corresponding Bedrock texture paths and documented UV dimensions, but their appearance still needs in-game verification in Minecraft Bedrock 1.26.62. The older starter mob sheets are retained as experimental assets and are not claimed as confirmed vanilla overrides. The existing Android game project is kept untouched.
