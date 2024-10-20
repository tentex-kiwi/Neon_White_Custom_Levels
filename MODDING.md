# Neon White Level Modding Guide

Welcome to your go-to-guide on modding levels in Neon White!

## Prerequisites

1. **Make a copy of your current save data**
   - You probably don't want to lose all your current save data, so you should back it up.
   - Save data can be found at `H:\Users\<USER>\AppData\LocalLow\Little Flag Software, LLC\`, where `H` is the drive you use and `<USER>` is your local user on the computer.
   - A quick way to get here is `windows key + r` and typing in `%appdata%`, then going up a level.
2. **Make a copy of the levels without modifications**
   - The levels are read independent of your save, so if you mod the levels they will still be modded even if you start a new game
     - **IF** you do need to get the default levels back, verify game file integrity through steam.
   - levels can be found in the location of the game's download.
   - The path might look something like `H:\SteamLibrary\steamapps\common\Neon White\Neon White_Data\` where `H` is the drive you use.
3. **Download AssetBundleExtractor**
   - **WARNING** I cannot vouch for the safety of this project, download at **YOUR OWN RISK**
   - [link to project](https://github.com/SeriousCache/UABE/releases/tag/v3.0-beta1)
   - Used to open and modify the level files.
4. **NeonLite/Speedometer**
   - To be able to modify where a present is in a level, a set of coordinates is needed.
   - This project uses the speedometer found in NeonLite, but any in-game speedometer should work.
   - access to the player's (x, y, z) coordinates is what is specifically needed, and speedometers should have this information
     - If the (x, y, z) coordinates are not visible, look in the mod's settings to allow advanced information.
5. **Project dependencies**

- This project has several dependencies that are needed for the code to run
  - Python
  - [numpy](https://numpy.org/) (pip install numpy)
  - [scipy](https://scipy.org/) (python -m pip install scipy)

## Modifying Levels

## Using Scripts

The provided script `coord_finder.py` provides some useful utility. `coordinates.py` provides manually collected data on every level in the game, including:

- mapping from fileName to in game level name
- **relative** coordinates of every present in the editor
  - this data was collected before I realized it's not really needed or used
- in game coordinates for the presents in every level
- coordinates and rotation of the parents of every present in the game

`coord_finder.py` can be used to find the new editor coordinates needed in the section below on moving assets in the editor.
`coord_finder.py` takes an optional command line argument `--output` followed by a filename for easy output. (i.e. `python coord_finder.py --output output.txt`)
`coord_finder.py` **requires** modders to update `custom_present_coordinates` in `coordinates.py`
`coord_finder.py` goes through every level/custom coordinate in `custom_present_coordinates` and determines the coordinates needed in the editor to make the asset appear at that location in game.

## In Editor

### Disabling Assets

- Assets can be disabled by setting the is_Active flag to false
- Setting an asset to false will cause it to not spawn
- An enemy who has been disabled will not count towards the total demon count for the level
  - For example, if there are normally 17 demons in a level and 3 are set to inactive, the modded level will only show and require 14 demons to be slain to beat the level.

### Adding Assets

- There has been no testing on how to add assets.
  - If someone figures out how to do this through AssetBundleExtractor or another method, they should try to update this repository.

### Moving Assets

- Moving assets was the original goal of this project. Everything else was a byproduct of trying to solve this.
- To move an asset, let's first understand how any asset gets it's location in Unity.
  - The location of an asset in Neon white is determined by 3 factors
    1. The location of the parent asset(s)
    2. the rotation of the parent asset(s)
    - note that the rotation is a quaternion (x, y, z, w) (where w is the rotation)
    - This is not the same as 3d rotation and the rotation (w value) CANNOT be ignored
    3. The location of the asset
  - To calculate the location of an asset (assuming it has a single parent)
    - Take the parent's location, and add the asset's location (augmented by the parent's rotation)
- Thus if we want to move an asset to a new location (x', y', z') in game, we need:
  1. The coordinates (x', y', z')
  2. The coordinates (ex, ey, ez) of the parent in the editor
  3. the rotation (rx, ry, rz, rw) of the parent in the editor
  - note that if there is no parent, then the location is (0, 0, 0) and the rotation is (0, 0, 0, 1)

## F.A.Q.

- Can I delete an asset?
  - I was able to successfully delete an asset once (a card spawn) instead of setting it to false. Another time it crashed my game when I tried to delete an asset in a different level. Proceed at your own risk.
- Why are the coordinates not exact?
  - I didn't feel like writing down all the digits. I'm sure you could calculate this using the parent's position, rotation, and the asset's position, but it would have required me to gather all the locations for all the parent assets in every level and that was too much work.
  - Also when copying over some of the data I rounded numbers. I tried to stay accurate to 3 decimal places, but there could be small errors.
- Your method for moving assets doesn't work for my asset!
  - I only tested this with presents. It's entirely possible there are cases I never ran into that my method won't work for such as assets with a grandparent
  - Some levels have might have multiple present assets and I may have only recorded the first one I saw.
- What happens if I change the rotation of a parent?
  - the rotation affects all the children.

## Future Ambissions

- I'd love to add the ability to have an in-game editor as part of neonlite
- The ability to add presents to levels that dont have them (boss levels)
- the ability to use presents in the levels with coins
- add other assets to levels (i.e. more enemies)

## Random Info

- Some levels (straightaway) have 2 presents. I don't know why, I don't know where the second one is. Haven't played around with it at all.
- Some levels (pop) have no presents. There is one in the game, but I can't find the asset in AssetBundleExtractor.
- Most levels have Spawn_Collectible_Card_Item_LoreCollectibleSmall, but a few (Shocker, Marathon) have Spawn_Collectible instead
  - Maybe these are the earliest levels to have collectibles and the asset was later renamed?

## Questions

- Reach out to the #modding community in the Neon White Speedrunning Discord!
- Reach out to tentex on discord
