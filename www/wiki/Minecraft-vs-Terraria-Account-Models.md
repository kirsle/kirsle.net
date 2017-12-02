# Minecraft vs Terraria Account Models

A comparison of the account/player models between Minecraft and Terraria and some ideas for things that could be done in my own game of that nature.

## Minecraft: Central Account System

Minecraft uses a centralized account system. When the game launcher starts up, it pings the Minecraft Central Account Server (CAS) to authenticate your player username and password and the client gets a session token from CAS.

When logging into a multiplayer server, your client sends your username and the session token to the server. The server can then send that information to CAS and verify that you are indeed who you say you are.

If the CAS goes down for good, players who already have the game can still play it forever in local "offline mode" (single player), including opening their game for LAN play. Server owners can continue running servers by switching them into offline mode, which removes any user authentication (better remove your list of operators because impersonation becomes possible!)

**Advantages:**

* Servers can have whitelists and operator lists based on name, and nobody can impersonate an admin user.

**Disadvantages:**

* If the CAS goes down, nobody can log into any servers (unless those servers switch to offline mode).

## Terraria: No CAS

With Terraria, once you've bought and downloaded the game, the company could disappear completely and not impact the players at all. There is no CAS which means no authentication with online multiplayer.

**Advantages:**

* Obviously, no phoning home and no central servers to depend on.
* Company can go under without affecting players at all.

**Disadvantages:**

* No central authority to vouch for player identities, which means servers can't keep admin lists based on names. Authentication has to be done in-game, after joining the server, by using custom server commands like `/login` and a server-specific password, etc.

## Player Models

In Minecraft, players are merely avatars with a name and a skin. Every world you join (including multiplayer worlds) start you with a clean slate: no inventory, no armor, no weapons, etc., and you only get one avatar per (paid) Mojang account. This is good for Minecraft because there's not a whole lot of *content* to the game (for example, armor options: Leather, Iron, Gold, Diamond.. and that's it). If you could keep your enchanted diamond armor between worlds the game would be pretty boring.

In Terraria, player avatars are their own separate entity from worlds, and an avatar has its own inventory and stats that are stored with the avatar. When switching from world to world, your avatar's inventory is kept intact. This even applies to joining multiplayer servers (although a lot of servers in the wild run on a custom server program that enforces server-side inventory).

In single player this lets you have a "New Game Plus" type experience, where you could play on one world until the end-game, and then start a brand new one and keep all your high level armor and weapons. There is a metric ton of content in Terraria and some of it is very difficult to get, so being able to keep it forever once you've obtained it is nice.

The down side is obvious: griefing on multiplayer. You could beef up your avatar on single player (or simply use an offline inventory edit hack) and then join multiplayer with a bunch of noobs and wreck up the place with your high level gear.

## Network Protocols

As if Terraria letting you join multiplayer using your local player avatars wasn't ripe enough for abuse, the network protocol trusts the client way too much. For example, the multiplayer server has no authority to tell a client *what the client's HP is*, among pretty much everything else. A hacked client can simply deny that it took damage. The server is a dumb proxy layer to enable clients to communicate but it does nothing to prevent cheating.

The advantage is that this is easy to program. The server doesn't need to run any game logic, just provide channels of communication for the clients to exchange game state information. The disadvantage obviously are the cheaters. I think on the whole, though, this makes it so Terraria is designed to be played with smaller groups of trusted friends rather than running public open-to-the-world servers with hundreds or thousands of connected players.

Minecraft on the other hand does most of the rule enforcements, physics calculations, etc. on the server side. The client mostly just communicates what actions they're taking and where they're walking to. The client does do some predictive processing, for example if you break a block the client will send to the server that the block was broken, but instead of waiting for the acknowledgement, it will render the block broken on the client. In case of lag or the server disagreeing that the block was broken, the client puts it back where it belongs.

This model is more tricky to develop and prone to bugs and lag-related glitching, but goes a long way toward thwarting hackers.

## My Ideas

If I were to make a game in the style of Minecraft/Terraria, I would go with some kind of hybrid approach:

### Central Account System

I would have one of these, like Minecraft. But to alleviate potential downtime of the CAS server, I would implement long-lived session tokens.

Briefly, a client should only *have* to communicate with the CAS server one time per computer/install of the game. It would be given a long-lived session token, with a public and private component.

When authenticating with a multiplayer server it would send the player's name and the public session key, which the server could verify with the CAS. This part would work just like in Minecraft. But additionally, the server can remember the result of this transaction so that the same player can join later even if the CAS is down at that time.

Now the issue would be the possibility of a hacker intercepting the session token and then impersonating the user. To solve that, the multiplayer server can verify the client by asking it to sign a random challenge by using its private session key (which only the client would have).

The player could de-authenticate old sessions through the CAS's website, in case their computer crashed completely and they couldn't delete the old session keys from it first. This would be akin to revoking a GPG key.

To handle the case of keys being compromised (read: stolen), multiplayer servers could periodically check with the CAS server to find any information about keys that had been revoked by the user. If the CAS was unreachable, the server would try again some other time.

And to handle the case that the CAS servers go down permanently, never to return: I would plan to release a patch that removes the authentication requirement from the game.

### Player Avatars

I like Terraria's approach of inventories coming with the avatars to multiplayer servers. I would design the game for the use case of having small groups of trusted friends to play online with.

However, I would also build features into the vanilla multiplayer server to enforce server-side inventory. It would be off by default.

### Network Protocol

I would probably go with a "simple proxy" model for the server, at least to start out with, because it's simpler. Again, the target use case would be for servers to be small and trusted. Additional monitoring code could always be added to the server to passively watch what's happening between players and apply heuristics to detect cheating (for example, making sure players can't travel too fast to detect teleport hacks, or see if a client is denying that their HP is being dropped, etc.)