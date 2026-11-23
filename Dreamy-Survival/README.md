# Dreamy Survival 🌿

Cozy Vanilla+ / cottagecore resource-pack starter for Minecraft Bedrock on Android.

## Generated texture batches
- **Blocks (30):** grass, dirt, stone, cobblestone, mossy cobblestone, wood, leaves, sand, sandstone, gravel, bricks, glass, clay, snow, ores, wool, terracotta, obsidian.
- **Nature (50):** flower sprites, tall-flower accents, saplings, azalea, mushrooms, fungi, and crop growth-stage sprites.
- **Items (14):** apples, golden apples, bread, carrots, potatoes, beetroot, berries, honey bottle, gems, ingots, coal, and sticks.
- **Mobs (12):** soft starter texture sheets for cow, sheep, pig, chicken, wolf, cat, fox, bee, horse, rabbit, turtle, and blue axolotl.
- **Armor (12):** six material palettes with two atlas layers each. Bedrock terrain/item atlas registration files and a custom pack icon are included.
- Custom pack icon and automated `.mcpack` build.

## Build validation
The generator checks the manifest and atlas JSON, verifies every registered texture exists, opens each PNG, and tests the final ZIP archive before the workflow uploads it.

## Build
1. Open the repository's **Actions** tab.
2. Select **Build Dreamy Survival Bedrock Pack**.
3. Press **Run workflow**.
4. Download the **Dreamy-Survival-mcpack** artifact from the completed run.
5. On Android, open the downloaded `.mcpack` with Minecraft and activate it in the world's Resource Packs.

## Compatibility note
This is an expanding custom texture collection, not yet a complete replacement of every vanilla texture. Mob and armor atlas overrides are starter assets and may need UV/name adjustments in Minecraft Bedrock 26.62; verify them in-game before treating them as finished replacements. The existing Android game project is kept untouched.
