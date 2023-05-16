# Copyright (c) 2023 Pablo Couto <hello@pablo.nohyphen.org>

import pyperclip
from codegen import extend_to_4x4
from colour import RGB_COLOURSPACES, matrix_RGB_to_RGB

if __name__ == '__main__':
    csi = RGB_COLOURSPACES['Sharp RGB']
    cso = RGB_COLOURSPACES['ACES2065-1']
    cat = 'CAT16'

    m = extend_to_4x4(matrix_RGB_to_RGB(csi, cso, cat))

    code = [[f'{x: 13.10f}' for x in row] for row in m.tolist()]
    code = '\n'.join([' '.join(row) for row in code])

    # # code formatting for ocio
    # code = f"matrix: [{', '.join([format(x, '.6g') for x in m.flatten().tolist()])}]"

    print(f"From {csi.name} to {cso.name} (CAT: {cat}):")
    print(code)
    pyperclip.copy(code)
