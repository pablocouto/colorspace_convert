# Copyright (c) 2023 Pablo Couto <hello@pablo.nohyphen.org>

import numpy as np
from codegen import extend_to_4x4, zero_round
from colour import RGB_COLOURSPACES, matrix_RGB_to_RGB


def print_cat_difference(csi, cso):
    for input_space in csi:
        for output_space in cso:
            matrices = []
            for cat_method in ['CAT02', 'CAT16']:
                m = extend_to_4x4(
                        matrix_RGB_to_RGB(
                            input_space, output_space, cat_method))
                m = zero_round(m, 1e-10)
                matrices.append(m)
                print(
                    f"Conversion matrix for {input_space.name} to {output_space.name} "
                    f"using {cat_method}:")
                print(m)
                print()

            # Compare the results numerically
            difference = np.abs(matrices[0] - matrices[1])
            max_difference = np.max(difference)

            print(f"Max difference between CAT02 and CAT16 for {input_space.name} to "
                  f"{output_space.name}: {max_difference}")
            print()


if __name__ == '__main__':
    csi = [RGB_COLOURSPACES[x]
           for x in ['Sharp RGB', 'ACEScc', 'ACEScct', 'ACEScg',
                     'ITU-R BT.709', 'sRGB', 'ITU-R BT.2020']]
    cso = [RGB_COLOURSPACES[x] for x in ['ACES2065-1']]
    cat = ['CAT02', 'CAT16']

    print_cat_difference(csi, cso)
