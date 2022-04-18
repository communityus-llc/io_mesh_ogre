# io_mesh_ogre

This script imports/exports Ogre models into/from Blender.

- Based: https://www.lofigames.com/phpBB3/viewtopic.php?f=11&t=10732
- Based on the Torchlight Import/Export script by 'Dusho'

## Supported

```
* import/export of basic meshes
* import/export of skeleton
* import/export of animations
* import/export of vertex weights (ability to import characters and adjust rigs)
* import/export of vertex colour (RGB)
* import/export of vertex alpha (Uses second vertex colour layer called Alpha)
* import/export of shape keys
* Calculation of tangents and binormals for export
```

## Known issues

```
* imported materials will lose certain informations not applicable to Blender when exported
```

## Install

- Download Binary: https://github.com/HadesD/io_mesh_ogre/releases/tag/v0

## Changelogs

```
* v0.9.1   (13-Sep-2019) - Fixed importing skeletons
* v0.9.0   (07-May-2019) - Switched to Blender 2.80 API
* v0.8.15  (17-Jul-2019) - Added option to import normals
* v0.8.14  (14-May-2019) - Fixed blender deleting zero length bones
* v0.8.13  (19-Mar-2019) - Exporting material files is optional
* v0.8.12  (14-Mar-2019) - Fixed error exporting animation scale keyframes
* v0.8.11  (26-Feb-2019) - Fixed tangents and binormals for mirrorred uvs
* v0.8.10  (32-Jan-2019) - Fixed export when mesh has multiple uv sets
* v0.8.9   (08-Mar-2018) - Added import option to match weight maps and link with a previously imported skeleton
* v0.8.8   (26-feb-2018) - Fixed export triangulation and custom normals
* v0.8.7   (01-Feb-2018) - Scene frame rate adjusted on import, Fixed quatenion normalisation
* v0.8.6   (31-Jan-2018) - Fixed crash exporting animations in blender 2.79
* v0.8.5   (02-Jan-2018) - Optimisation: Use hashmap for duplicate vertex detection
* v0.8.4   (20-Nov-2017) - Fixed animation quaternion interpolation
* v0.8.3   (06-Nov-2017) - Warning when linked skeleton file not found
* v0.8.2   (25-Sep-2017) - Fixed bone translations in animations
* v0.8.1   (28-Jul-2017) - Added alpha component to vertex colour
* v0.8.0   (30-Jun-2017) - Added animation and shape key support. Rewritten skeleton export
* v0.7.2   (08-Dec-2016) - fixed divide by 0 error calculating tangents
* v0.7.1   (07-Sep-2016) - bug fixes
* v0.7.0   (02-Sep-2016) - Implemented changes needed for Kenshi: Persistant Ogre bone IDs, Export vertex colours. Generates tangents and binormals.
* v0.6.2   (09-Mar-2013) - bug fixes (working with materials+textures), added 'Apply modifiers' and 'Copy textures'
* v0.6.1   (27-Sep-2012) - updated to work with Blender 2.63a
* v0.6     (01-Sep-2012) - added skeleton import + vertex weights import/export
* v0.5     (06-Mar-2012) - added material import/export
* v0.4.1   (29-Feb-2012) - flag for applying transformation, default=true
* v0.4     (28-Feb-2012) - fixing export when no UV data are present
* v0.3     (22-Feb-2012) - WIP - started cleaning + using OgreXMLConverter
* v0.2     (19-Feb-2012) - WIP - working export of geometry and faces
* v0.1     (18-Feb-2012) - initial 2.59 import code (from .xml)
* v0.0     (12-Feb-2012) - file created
```

## License

- MIT
- Based on 
