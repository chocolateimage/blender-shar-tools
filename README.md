# Hit & Run for Blender
A blender addon that adds various tools for working with P3D files from The Simpsons Hit & Run. 

This addon currently targets Blender 4.2 and is based on DonutTeam's blender-shar-tools.

The Pure3D classes within this repo are based very significantly upon [LuaP3DLib](https://github.com/Hampo/LuaP3DLib) and the [TypeScript Pure3D Library](https://github.com/donutteam/npm-pure3d).

## Installing
Download the repo with Git or click on "Code" -> "Download ZIP" at the top.  
Copy/move the "src" directory to:
- Windows: `~\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons`
- Linux: `~/.config/blender/4.2/scripts/addons`

Make sure to **replace the version number** with the latest one and **create the subdirectories** if they don't exist.  
You can rename the "src" directory if you want.

I may come up with a more intuitive guide for installing the addon.

## Usage

**Read before using:** You can find most panels, etc. in the category "Blender SHAR Tools" (press N to show categories on the right side)

### Create an new P3D file
In the panel "Management" press "Add P3D" then a new P3D collection will added to the scene collection.  
Make sure all P3D collections' name end with ".p3d"

### Importing a P3D file
"File" -> "Import" -> "Pure3D File (.p3d)".  
On the import window you can select what to import on the right side.

### Exporting a P3D collection
"File" -> "Export" -> "Pure3D file (.p3d)"  
**Important:** On the right side on the export window select what collection you want to export.

### How to create a static mesh
1. Create an object mesh like you usually do.
2. Move the object to the P3D collection's "Static Entities" subcollection
3. Assign an existing or new material
4. (Optional) Change SHAR shader properties in the "SHAR Shader Properties" (in the Material Properties, just scroll down)

### Materials/Shaders?
Change SHAR shader properties in the "SHAR Shader Properties" (in the Material Properties on an object, just scroll down)

Explanations of the properties:

#### Raw Texture Name
Instead of importing a texture into Blender you can type an existing texture name from SHAR into the field.

#### Terrain Type
Used when exporting intersects (see [Intersect Usage](#how-to-create-intersects))

#### What to know

- Don't worry about texture sizes, the addon will automatically fix sizes internally.

### How to create intersects
Intersects are generated at export from Static Entities that have "track" or "polySurfaceShape" in the name and have a terrain type set in the material.

Multi material objects are currently not supported.

## Issues

The "main" branch is being developed on, so make sure to update the addon first before reporting an issue.

## Contributing
This fork is ready to be contributed on, I myself don't know if you can make PRs to forks but you can try!

## License
[MIT](https://github.com/donutteam/blender-shar-tools/blob/main/LICENSE.md)