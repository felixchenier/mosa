#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Félix Chénier

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Constants used by the Mobility and Adaptive Sports Research Lab."""

import numpy as np


#--- Some calibration matrices ---#
INSTRUMENTED_WHEEL_CALIBRATION = {}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_93'] = {
    'gains': np.array([-0.1080, 0.1080, 0.0930, 0.0222, -0.0222, 0.0234999]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_94'] = {
    'gains': np.array([-0.1070, 0.1070, 0.0960, 0.0222, -0.0222, 0.0230]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_123'] = {
    'gains': np.array([-0.106, 0.106, 0.094, 0.022, -0.022, 0.0234999]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_124'] = {
    'gains': np.array([-0.106, 0.106, 0.0949999, 0.0215, -0.0215, 0.0225]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_125'] = {
    'gains': np.array([-0.104, 0.104, 0.0979999, 0.0215, -0.0215, 0.0225]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_126'] = {
    'gains': np.array([-0.1059999, 0.1059999, 0.086, 0.021, -0.021, 0.023]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_126_S18'] = {
    'gains': np.array([-0.1083, 0.1109, 0.0898, 0.0211, -0.0194, 0.0214]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_179_S18'] = {
    'gains': np.array([-0.1399, 0.1091, 0.0892, 0.0240, -0.0222, 0.0241]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_180_S18'] = {
    'gains': np.array([-0.1069, 0.1091, 0.0932, 0.0240, -0.0226, 0.0238]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
INSTRUMENTED_WHEEL_CALIBRATION['SmartWheel_181_S18'] = {
    'gains': np.array([-0.1152, 0.1095, 0.0791, 0.0229, -0.0197, 0.0220]),
    'offsets': np.array([0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
    'transducer': 'smartwheel',
}
# Carbon wheel 1
INSTRUMENTED_WHEEL_CALIBRATION['MOSA_Racing_1'] = {
    'gains': (np.array([
        [201.027, 1.387, 2.077, -3.852, -1.837, -1.519],
        [-0.840, 201.396, 2.119, 0.083, -6.877, 4.482],
        [-1.935, -1.643, 402.286, 1.687, 0.897, -23.616],
        [0.213, 0.122, 0.120, 25.190, -0.013, 0.147],
        [-0.072, 0.286, 0.076, 0.012, 25.430, 0.146],
        [0.016, -0.015, 0.046, -0.099, -0.076, 25.206]])  # Cell calibration
        / ((2.**15) / 10)  # ADC gains
        / np.array([-2., -2., -2., -2., -4., -4.])  # Board gains
    ),
    'offsets': [-111.3874, -63.3298, -8.6596, 1.8089, 1.5761, -0.8869],
    'transducer': 'force_cell',
}
# Green wheel 1
INSTRUMENTED_WHEEL_CALIBRATION['MOSA_Racing_2'] = {
    'gains': (np.array([
        [182.176, 2.860, 3.333, -4.092, 0.217, -3.291],
        [-0.456, 176.603, 1.178, -0.276, 4.523, 4.344],
        [-1.540, -3.053, 370.970, -5.003, -5.824, -13.577],
        [-0.061, -0.042, -0.077, 21.597, 0.092, 0.163],
        [-0.061, 0.321, -0.121, -0.051, 22.411, 0.249],
        [-0.105, 0.161, -0.002, -0.183, -0.066, 23.260]])  # Cell calibration
        / ((2.**15) / 10)  # ADC gains
        / np.array([-2., -2., -2., -2., -4., -4.])  # Board gains
    ),
    'offsets': [-111.3874, -63.3298, -8.6596, 1.8089, 1.5761, -0.8869],
    'transducer': 'force_cell',
}
