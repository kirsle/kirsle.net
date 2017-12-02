# Minecraft Clone

Just a brain dump on my ideas for a Minecraft-style game.

# Minimum Requirements

The game should fix all of the shortcomings of Minecraft and do everything better. See [blog post](https://www.kirsle.net/blog/entry/minecraft-clones). Briefly:

* Cubic chunks (16x16x16 instead of 16x16x256) allowing for infinitely tall and deep worlds in addition to infinitely wide worlds.
* Better chunk saving: only save modified blocks to disk. The game should always re-generate chunks and apply changes on top. The chunk header would include the terrain algorithm version used, so on drastic algorithm changes, old chunks can still use the old algorithm.

# Terrain Generation Milestones

Terrain generation will probably be the most difficult part. Briefly, these would be the major milestones in terrain:

## Superflat (infinite)

A superflat world would probably be the first world type, as it would be the easiest to generate. It would work exactly like in Minecraft. Since getting the cubic chunk system and other fundamental design goals sorted out will be the top priority in the beginning, an infinitely generating superflat world would be ideal early on. It could also be used to test the chunk saving format (e.g. initially, nothing should be saved to disk until you start placing and destroying blocks) and the world could easily scale infinitely in all directions, since no special terrain algorithms are needed.

## Limited World (MVP)

This is the minimum viable product/the goal for terrain generation for a first "official" release of the game.

The world would be similar in principal to how Terraria does it. The world would be generated *in advance* of starting the game, and the terrain generation algorithm would fully populate *and save* all chunks up front. This will take some time but that's acceptable as the world will only be generated once and all blocks saved to disk.

The world would still be large (like Terraria), and all essential terrain features would be included. The algorithm would be deterministic (one seed value would always generate the same world), but it would eliminate a TON of complexity surrounding using a procedurally generated infinitely large world algorithm. If the game has e.g. a stronghold like in Minecraft or a dungeon like in Terraria, it would be sure to be generated inside of the limited world size.

Mechanic ideas for world generation:

* Do it in multiple phases. During world set-up, we have all the time in the world (to be fair, Terraria takes its time generating a Large world type, too).
    * Phase 1 could be simple topography using a Perlin noise height map
    * Phase 2 could be biome assignments (find a noise + contrast algorithm that creates a "bubbly" texture, and assign each enclosed bubble a random but deterministic biome style). It would be a priority that every biome exists in at least one place, since the world is limited, so some manual overriding (deterministically) can be added to ensure this.
        * The cubic chunk system would allow for altitude-dependent biomes, but it could be kept simple initially and have Minecraft style biomes, where a biome applies to the full vertical height.
        * Some height specific biomes would be generated on a second pass, for some special ones i.e. Sky Islands and Mushroom Caves.
    * Phase 3 could be generating cave systems and ravines and such, possibly in multiple passes.
    * Phase 4 would be structures of varying kinds (stronghold/dungeon, loot structures, etc.)

The point is that the *finite* world size means terrain generation can be made simpler, as the game never has to query "which blocks should be at this random chunk?" and worry about getting a consistent response to that question.

## Infinite World

If I find a way to procedurally generate an infinitely large world (particularly one that plays nice with the cubic chunk system; easier said than done), it would act as an extension of the Limited World type. For example, all *essential* structures (stronghold/dungeon) would still probably generate within a certain radius of the spawn point. This is consistent with how Minecraft does it, anyway.

Some challenges to this:

* Like in Minecraft, the game should be able to ask for any random chunk in the world, and get a consistent response every time as to what blocks should be in that chunk.
* For basic terrain generation based on noise algorithms, this may be easy if the mathematical functions could accept X/Y/Z coordinates and return a fast answer.
* For more complicated things, i.e. cave systems it may be more complicated.

# Random Feature Ideas

This is getting way ahead of myself, but a list of nice-to-have's in a Minecraft inspired game:

* Features to borrow from Terraria:
    * Tree felling: break the trunk and the whole tree "explodes" as dropped log items, instead of you needing to mine every. individual. block.
    * Their crafting system is better than Minecraft's. In Terraria, your "crafting menu" just lists all possible things you can craft, *based on your current inventory and what types of crafting stations you are standing adjacent to.* This helps with in-game discovery of available recipes while still keeping an air of mystery by not showing the player up front that they can build a crafting table and an ender chest.
    * Once momentum picks up, add content, content, and more content! Terraria has a million billion types of weapons and armor and all kinds of other things, to the point that in Terraria, your player character is separate from your world and you can keep your inventory between worlds.