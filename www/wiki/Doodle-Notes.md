# Ideas

## Table of Contents

* [Major Milestones](#major-milestones)
* [File Formats](#file-formats)
* [Text Console](#text-console)
* [Doodads](#doodads)

# Major Milestones

The major milestones of the game are roughly:

* Prototype: make a simple SDL painting program that does nothing special.
* Simple Platformer: be able to toggle between "edit mode" and "play mode"
    and control a character who can walk around your level and bump into the
    solid geometry you've drawn (no objects yet, just the basics here).
* Add Doodads (buttons, doors, the player character themself, enemies, ...)
    * Share a lot in common with map drawings, in that they're hand-drawn, will
      share a similar file format.
    * Available doodads can be dragged/dropped into maps.
    * The player character should be a Doodad under the hood to keep it from
      becoming too special (read: easier to make the game multiplayer in the
      future by putting a "networked user" in control of a doodad instead of
      the keyboard/mouse).
* **Version 1:** Single Player Campaign and Editor. This is the minimum
    feature set for a first public release of the game. Required features:
    * The game should ship with a single-player "campaign mode" of pre-made maps
      that link to one another in sequence. i.e. 100 levels that the player can
      play through in a certain order.
    * It must include the level editor feature so players can create and share
      their own maps.
    * Dev tools may be clunky to use at this stage; i.e. players creating custom
      Doodads will need to use external tools outside the game (i.e. code editors
      to program the JavaScript logic of the doodad), but everything should be
      available and possible for modders to extend the game with custom features.
    * Game should have a good mixture of doodads and features: doors, buttons,
      switches, etc. and make a usable single player experience.
    * World sizes might be limited in dimension.
* **Version 2:** Multiplayer Collaborative World Builder. This is a
    "pie in the sky" long-term vision for the game, to make it multiplayer,
    hopefully addicting, and possibly slightly Minecraft-like. Some ideas:
    * Players can self-host their own multiplayer servers to draw worlds with
      friends.
    * A new server would initialize as a blank white level with maybe a single
      platform (a line) for players to spawn on.
    * Gameplay is a mixture of players drawing the world and playing on it.
      * i.e.: one player could be drawing himself a castle and, as he's drawing,
        another player could be walking on the lines being laid down, etc.
    * World size should be infinite.
    * Besides creative mode, other game modes should be explored eventually...
      * Automatically-spawning enemy doodads that you have to fight?
      * Procedurally generated default maps? Having a blank white canvas is
        sorta like Superflat worlds in Minecraft, whereas normal Minecraft worlds
        come with randomly generated terrain to start from.
      * Find a way to incorporate drawing into a survival mode game? i.e. instead
        of a "Creative Mode" style, "unlimited ink to draw as much as you want,"
        have some natural limiter where players have to spend time in Play Mode
        to be able to change the map.

# File Formats

* The file formats should eventually have a **Protocol Buffers** binary
    representation before we go live. JSON support shall remain, but the
    production application will not _write_ JSON files, only read them.
    (This way we can ship drawings in the git repo as text files).

## Common Drawing Files

* A common base format should be shared between Levels and Doodads. You should
    be able to use the Editor mode and draw a map *or* draw a doodad like a
    button. The drawing data should be a common structure between Level and
    Doodad files.
* The drawing is separated between a **Palette** and the **Pixels**
    themselves. The Pixels reference the Palette values and their X,Y
    coordinate.
* The _color_ and the _behavior_ of the palette are decoupled.
    * In the base game, all the solid lines you draw may be black and red
      lines are fire, but these aren't hard and fast rules. You could hack a
      custom map file that makes black lines fire and red lines water if
      you wanted.
    * The Palette in the map file stores the attributes and colors of each
      distinct type of pixel used in the map. Here it says "color 0 is
      black and is solid", "color 1 is red and is fire and is not solid",
      etc.
    * A mod tool could be written to produce a full-color pixel art level
      that still behaves and follows the normal rules of the Doodle game
      with regards to geometry and collisions.
* Ideas for pixel attributes:
    * Brush: what shape brush to draw the pixel with.
    * Solid: can't collide with other solid pixels.
    * Fire: applies fire damage to doodads that intersect with it.
    * Water: If a doodad passes through a blue pixel, they toggle their
      underwater physics. This way pools can be entered from ANY side (top,
      bottom, sides) and the physics should toggle on and off.
    * Slippery: when a doodad is standing on a slippery pixel, do some extra
      checks to find a slope and slide the doodad down it. Makes the pixels
      act like ice.
* Standard palette:
    * The base game's map editor will tend toward hand-drawn style, at least
      at first.
    * Black lines are solid.
    * Dashed black lines are slippery.
    * Red lines are fire.
    * Blue lines are water.
    * Light grey lines are decoration (non solid, background geometry)
    * May make it possible to choose arbitrary colors separately from the
      type of pixel. A palette manager UX would be great.

## Level Files

* In the level file, store the `pixelHistory` as the definitive source
    of pixels rather than the grid of pixels. Let the grid be populated when
    the level is being inflated. The grid should have `json:"-"` so it doesn't
    serialize to the JSON.
    *  This makes it possible to animate levels as they load -- by
       fast-tracing the original lines that the mapper drew, watching them draw
       the map before you play it.
    * Makes the file _slightly_ lighter weight because a lot of lines will have
      delta positions in the pixelHistory so we don't need to store the middle
      pixels.
* It should have space to store copies of any custom Doodads that the user
    wants to export with the level file itself, for easy sharing.
* It should have space to store a custom background image.

# Text Console

* Create a rudimentary dev console for entering text commands in-game. It
    will be helpful until we get a proper UI developed.
    * The `~` key would open the console.
    * Draw the console on the bottom of the screen. Show maybe 6 lines of
      output history (a `[]string` slice) and the command prompt on the
      bottom.
* Ideas for console commands:
    * `save <filename.json>` to save the drawing to disk.
    * `open <filename.json>`
    * `clear` to clear the drawing.
* Make the console scriptable so it can be used as a prompt, in the mean
    time before we get a UI.
    * Example: the key binding `Ctrl-S` would be used to save the current
      drawing, and we want to ask the user for a file name. There is no UI
      toolkit yet to draw a popup window or anything.
    * It could be like `console.Prompt("Filename:")` and it would force open
      the text console (if it wasn't already open) and the command prompt would
      have that question... and have a callback command to run, like
      `save <filename.json>` using their answer.

# Doodads

Doodads will be the draggable, droppable, scriptable assets that make the
mazes interactive.

* They'll need to store multiple frames, for animations or varying states.
    Example: door opening, button being pressed, switch toggled on or off.
* They'll need a scripting engine to make them interactive. Authoring the
    scripts can be done externally of the game itself.
* The built-in doodads should be scripted the same way as custom doodads,
    dogfooding the system.
* Custom doodads will be allowed to bundle with a level file for easy
    shipping.
    * Installing new doodads from a level file could be possible too.
* Doodads within a level file all have a unique ID, probably just an
    integer. Could be just their array index even.

Some ideas for doodad attributes:

* Name (string)
* Frames (drawings, like levels)

Doodad instances in level files would have these attributes:

* ID (int)
* X,Y coordinates
* Target (optional int; doodad ID):
    * For buttons and switches and things. The target would be another
      doodad that can be interacted with.
    * Self-contained doodads, like trapdoors, won't have a Target.
* Powered (bool)
    * Default `false` and most things won't care.
    * A Button would be default `false` until pressed, then it's `true`
    * A Switch is `true` if On or `false` if Off
    * A Door is `true` if Open and `false` if Closed
    * So when a switch is turned on and it opens a door by pushing a `true`
      state to the door... this is the underlying system.

## Scripting

* Probably use Otto for a pure Go JavaScript runtime, to avoid a whole world
    of hurt.
* Be able to register basic event callbacks like:
    * On load (to initialize any state if needed)
    * On visible (for when we support scrolling levels)
    * On collision with another doodad or the player character
    * On interaction (player hits a "Use" button, as if to toggle a switch)
* Doodads should be able to pass each other messages by ID.
    * Example: a Button should be able to tell a Door to open because the
      button has been pressed by another doodad or the player character.

Some ideas for API features that should be available to scripts:

* Change the direction and strength of gravity (i.e. Antigravity Boots).
* Teleport the player doodad to an absolute or relative coordinate.
* Summon additional doodads at some coordinate.
* Add and remove items from the player's inventory.

## Ideas for Doodads

Some specific ideas for doodads that should be in the maze game, and what
sorts of scripting features they might need:

* Items (class)
    * A class of doodad that is "picked up" when touched by the player
      character and placed into their inventory.
    * Scriptable hooks can still apply, callback ideas:
      * On enter inventory
      * On leave inventory
    * Example: Gravity Boots could be scripted to invert the global gravity
      when the item enters your inventory until you drop the boots.
    * Some attribute ideas:
      * Undroppable: player can't remove the item from their inventory.
    * Item ideas to start with:
      * Keys to open doors (these would just be mere collectables)
      * Antigravity Boots (scripted to mess with gravity)
* Buttons
    * At least 2 frames: pressed and not pressed.
    * Needs to associate with a door or something that works with buttons.
    * On collision with a doodad or player character: send a notification to
      its associated Door that it should open. (`Powered: true`)
    * When collision ends, button and its door become unpowered.
* Sticky Buttons
    * Buttons that only become `true` once. They stick "On" when activated
      for the first time.
    * Once pressed they can't be unpressed. However, there's nothing stopping
      a switch from targeting a sticky button, so when the switch is turned off
      the sticky button turns off too.
* Switches
    * Like a button. On=`true` and Off=`false`
    * 2 frames for the On and Off position.
    * On "use" by the player, toggle the switch and notify the door of the new
      boolean value.
      * It would invert the value of the target, not just make it match the
        value of the switch. i.e. if the switch is `false` and the door is
        already open (`true`), making the switch `true` closes the door.
* Powered Doors
    * Can only be opened when powered.
    * 2 frames of animation: open and closed.
    * A switch or button must target the door as a way to open/close it.
* Locked Doors
    * Requires a key item to be in the player's inventory.
    * On collision with the player: if they have the key, the door toggles to
      its `true` powered state (open) and stays open.
    * The door takes the key from the player's inventory when opened.
* Trapdoors
    * One-way doors that close behind you.
    * Can be placed horizontally: a doodad falling from above should cause
      the door to swing open (provided it's a downward-only door) and fall
      through.
    * Can be placed vertically and acts as a one-way door.
    * Needs several frames of animation.