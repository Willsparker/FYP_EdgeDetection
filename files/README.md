This is the place where files for the system will be. Currently should just be:

'tmp.png' - an image that is a copy of of the image _before_ convolution. Used for the 'undo' button, as well as a means of loading the altered image into Kivy's Image object (via the BytesIO trick)

'presetMasks' - a text file of preset masks for the user to load in, in the following format: `<name> <matrixCoefficient> <list of mask values> <greyCheck>`. `<name>` must be in the list found in `main.kv` under id 'presetSpinner', except in lowercase & removed spaces. `<list of Mask values>` is the mask, delimited by a `,` char.

