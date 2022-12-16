from paths.base import AreaMovementBase


class Moonflow1(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-138, -254],
        1: [-179, -262],
        # Picking up chest
        3: [-114, -291],
        4: [-36, -369],
        5: [-10, -450],
        6: [57, -19],
        7: [60, -54],
        8: [3, -227],
        9: [-11, -325],
        10: [-20, -400],
        11: [610, 843],  # Map - Fork in the road
        12: [567, 991],
        13: [567, 1200],
        # Start of the long Moonflow path/map
        14: [-988, 1678],
        15: [-1072, 1557],
        16: [-1112, 1484],
        17: [-1159, 1369],
        18: [-1176, 1347],
        19: [-1230, 1140],
        20: [-1317, 783],
        21: [-1317, 783],  # Ronso discussion
        22: [-1348, 758],
        23: [-1438, 717],
        24: [-1523, 661],
        25: [-1571, 624],
        26: [-1624, 573],
        27: [-1666, 538],
        28: [-1704, 484],
        29: [-1801, 365],
        30: [-1833, 317],
        31: [-1838, 299],
        32: [-1838, 299],
        33: [-1856, 214],
        34: [-1864, 162],
        35: [-1866, 124],
        36: [-1872, -23],
        37: [-1880, -163],
        38: [-1901, -401],
        39: [-1898, -483],
        40: [-1893, -506],
        41: [-1855, -503],
        42: [-1812, -476],
        # Moonflow chest
        44: [-1862, -511],
        45: [-1901, -513],
        46: [-1913, -559],
        47: [-1968, -650],
        48: [-1970, -900],
        49: [-1190, 193],  # Actual Moonflow map
        50: [-1118, -614],  # Can be used for tuning later.
        51: [-1118, -614],
        52: [-1034, -566],
        53: [-960, -500],  # Last before "Whoa a Shoopuff"
        54: [-200, -60],
        55: [-30, 180],
    }
    checkpoint_fallback = {
        2: "Picking up chest",
        43: "Moonflow chest",
    }


class MoonflowBankSouth(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-104, 112],
        1: [-108, 97],
        2: [-83, 69],
        3: [-71, 48],
    }


class MoonflowBankNorth(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-305, 184],
        1: [-400, 150],
        2: [-1001, -767],
        3: [-1135, -807],  # Rikku scene
        4: [-1123, -759],
        5: [-1134, -699],
        6: [-1125, -627],
        # Rikku steal/mix tutorial
        8: [-1076, -553],
        9: [-944, -384],
        10: [-892, -327],
        11: [-800, -270],  # Into the Guadosalam entrance map
        12: [313, -911],
        13: [269, -812],
        14: [130, -443],
        15: [98, -300],
        16: [86, -190],
        17: [74, 32],
        18: [70, 200],
    }
    checkpoint_fallback = {
        7: "Rikku steal/mix tutorial",
    }
