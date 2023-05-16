# Copyright (c) 2023 Pablo Couto <hello@pablo.nohyphen.org>

import numpy as np
from colour import RGB_COLOURSPACES, xy_to_XYZ
from colour.adaptation import matrix_chromatic_adaptation_VonKries


def zero_round(matrix, epsilon):
    return np.where(np.abs(matrix) < epsilon, 0, matrix)


def extend_to_4x4(matrix):
    """Extend a 3x3 transform to a 4x4 transform."""
    matrix_4x4 = np.eye(4)
    matrix_4x4[:3, :3] = matrix
    return matrix_4x4


def generate_options(colorspaces):
    options = '|'.join([f'{cs.name} ({cs.whitepoint_name}):{i}'
                        for i, cs in enumerate(colorspaces)])
    return f'string options = "{options}"'


def generate_transforms(colorspaces, output=False, cat='CAT02'):
    """Produce OSL code for all color transforms in one direction.

    :param output: Whether to produce code for the output half of the color
        transformation."""
    def osl_transform(array):
        """Produce OSL code for a transform."""
        code = [[f'{x: 13.10f}' for x in row] for row in array.tolist()]
        code = ',\n\t\t'.join([', '.join(row) for row in code])
        return 'matrix(\n\t\t' + code + ');'

    def osl_transform_case(output, i, cs, m, cat):
        """Produce OSL code for a transform case."""
        var_names = {True: ('ocs', 'm_o', 'cat_o'),
                     False: ('ics', 'm_i', 'cat_i')}
        sel_v, m_v, cat_v = var_names[output]

        case = (f'{"else " if i else ""}if ({sel_v} == {i})\t'
                f'// {cs.name}, w: {cs.whitepoint_name}\n')
        transforms = f'''{{
    {m_v} = {osl_transform(m)}
    {cat_v} = {osl_transform(cat)}
}}
'''
        return case + transforms

    code = ''
    # reference whitepoint (E)
    wr = xy_to_XYZ(RGB_COLOURSPACES['CIE RGB'].whitepoint)
    for i, cs in enumerate(colorspaces):
        # color transform
        # See note in https://colour.readthedocs.io/en/latest/generated/colour.RGB_Colourspace.html#colour.RGB_Colourspace
        cs.use_derived_matrix_RGB_to_XYZ = True
        cs.use_derived_matrix_XYZ_to_RGB = True
        m = cs.matrix_XYZ_to_RGB if output else cs.matrix_RGB_to_XYZ
        m = extend_to_4x4(m)

        # color appearance transform
        w = xy_to_XYZ(cs.whitepoint)
        w_from, w_to = (wr, w) if output else (w, wr)
        catm = matrix_chromatic_adaptation_VonKries(w_from, w_to, cat)
        catm = extend_to_4x4(zero_round(catm, 1e-10))

        transform = osl_transform_case(output, i, cs, m, catm)
        code = code + transform

    return code
