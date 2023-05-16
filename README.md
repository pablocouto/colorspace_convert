### About
This repository contains a script to generate an OSL shader for converting between color spaces. The shader is pre-generated (`colorspace_convert.osl`) for conversions between ACES2065-1, ACEScg, ITU-R BT.709, and Sharp RGB.

### Instructions
- (Optional, but recommended) Create a Python virtual environment
    ```powershell
    $ python -m venv venv
    $ .\venv\Scripts\Activate.ps1
    ```
- Install requirements
    ```powershell
    $ pip install -r requirements.txt
    ```
- Configure the desired color spaces in `colorspace_convert.osl` by modifying the `colorspaces` global variable at the top. For example,
    ```python
    colorspaces = [RGB_COLOURSPACES[cs] for cs in [
        'ACES2065-1',
        'ACEScg',
        'ITU-R BT.709',
        'Sharp RGB',
        ]]
    ```
    Note that the color space names must be selected from those available in [`colour.RGB_COLOURSPACES`](https://colour.readthedocs.io/en/latest/generated/colour.RGB_COLOURSPACES.html).
    You can also change the color appearance transform by modifying the global variable `CAT` at the same location. It is set by default to CAT16, but you may prefer CAT02, which, for context, is the one used in [OpenColorIO-Configs](https://github.com/colour-science/OpenColorIO-Configs).
- Run `cog -r colorspace_convert.osl`
- Use the updated shader where desired
