#!/usr/bin/python3
from typing import Iterable, List, Tuple, Union

"""A repository of named colors."""


def hex_to_rgb(value: str) -> Tuple[int]:
    """
    Turn hex color value into RGB(A).
    :param value: string hex
    :return: tuple int
    """
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(*rgba_values: [Iterable[int]]) -> str:
    """
    Turn RGB(A) color rgba into hex.
    :param rgba_values: tuple int
    :return: string hex
    """
    rgba: List[int] = [x for x, _ in zip(rgba_values, range(4))]
    assert len(rgba) in (3, 4), "Colors are a triplet of Red, Green, and Blue (and, possibly, an Alpha or transparency)."
    assert all(0 <= x < 256 for x in rgba), 'Color does not exist.'
    return '#{:02x}{:02x}{:02x}{}'.format(rgba[0], rgba[1], rgba[2], '{:02x}'.format(rgba[3]) if len(rgba) > 3 else '').upper()


def fade(r: int, g: int, b: int, fading: int = 0, get_hex: bool = False) -> Union[Tuple[int], str]:
    """
    Dim a color (r, g, b) to (r - fading, g - fading, b - fading).
    :param r: int red
    :param g: int green
    :param b: int blue
    :param fading: int dimming
    :param get_hex: bool
    :return: tuple-int RGB if not get_hex else str hex
    """
    a: Tuple[int] = tuple((c - fading) for c in (r, g, b))
    assert (min(a) >= 0 and max(a) <= 255), 'Color does not exist.'
    return a if not get_hex else rgb_to_hex(*a)


def fade_alpha(r: int, g: int, b: int, a: int, fading: int = 0, get_hex: bool = False, simple: bool = False) -> Union[Tuple[int], str]:
    """
    If simple, dim a color (r, g, b, a) to (r - fading, g - fading, b - fading, a - fading).
    If not, dim a color (r, g, b, a) to (r, g, b, a - fading).
    :param r: int red
    :param g: int green
    :param b: int blue
    :param a: int alpha (transparency)
    :param fading: int dimming
    :param get_hex: bool
    :param simple: bool
    :return: tuple-int RGB if not get_hex else str hex
    """
    t: Tuple[int, ...] = tuple((((c - fading) for c in (r, g, b, a)) if simple else (r, g, b, a - fading)))
    assert (min(t) >= 0 and max(t) <= 255), 'Color does not exist.'
    return t if not get_hex else rgb_to_hex(*t)


T_COLOR = Tuple[Tuple[int, int, int], str]


class Colors:
    """ Colors. Each color is a ( (red: int, green: int, blue: int), hex: str) tuple. """
    grey: T_COLOR = ((84, 84, 84), '#545454')
    grey_silver: T_COLOR = ((192, 192, 192), '#C0C0C0')
    grey101: T_COLOR = ((190, 190, 190), '#BEBEBE')
    lightgray: T_COLOR = ((211, 211, 211), '#D3D3D3')
    lightslategrey: T_COLOR = ((119, 136, 153), '#778899')
    slategray: T_COLOR = ((112, 128, 144), '#708090')
    slategray1: T_COLOR = ((198, 226, 255), '#C6E2FF')
    slategray2: T_COLOR = ((185, 211, 238), '#B9D3EE')
    slategray3: T_COLOR = ((159, 182, 205), '#9FB6CD')
    slategray4: T_COLOR = ((108, 123, 139), '#6C7B8B')
    black: T_COLOR = ((0, 0, 0), '#000000')
    grey0: T_COLOR = ((0, 0, 0), '#000000')
    grey1: T_COLOR = ((3, 3, 3), '#030303')
    grey2: T_COLOR = ((5, 5, 5), '#050505')
    grey3: T_COLOR = ((8, 8, 8), '#080808')
    grey4: T_COLOR = ((10, 10, 10), '#0A0A0A')
    grey5: T_COLOR = ((13, 13, 13), '#0D0D0D')
    grey6: T_COLOR = ((15, 15, 15), '#0F0F0F')
    grey7: T_COLOR = ((18, 18, 18), '#121212')
    grey8: T_COLOR = ((20, 20, 20), '#141414')
    grey9: T_COLOR = ((23, 23, 23), '#171717')
    grey10: T_COLOR = ((26, 26, 26), '#1A1A1A')
    grey11: T_COLOR = ((28, 28, 28), '#1C1C1C')
    grey12: T_COLOR = ((31, 31, 31), '#1F1F1F')
    grey13: T_COLOR = ((33, 33, 33), '#212121')
    grey14: T_COLOR = ((36, 36, 36), '#242424')
    grey15: T_COLOR = ((38, 38, 38), '#262626')
    grey16: T_COLOR = ((41, 41, 41), '#292929')
    grey17: T_COLOR = ((43, 43, 43), '#2B2B2B')
    grey18: T_COLOR = ((46, 46, 46), '#2E2E2E')
    grey19: T_COLOR = ((48, 48, 48), '#303030')
    grey20: T_COLOR = ((51, 51, 51), '#333333')
    grey21: T_COLOR = ((54, 54, 54), '#363636')
    grey22: T_COLOR = ((56, 56, 56), '#383838')
    grey23: T_COLOR = ((59, 59, 59), '#3B3B3B')
    grey24: T_COLOR = ((61, 61, 61), '#3D3D3D')
    grey25: T_COLOR = ((64, 64, 64), '#404040')
    grey26: T_COLOR = ((66, 66, 66), '#424242')
    grey27: T_COLOR = ((69, 69, 69), '#454545')
    grey28: T_COLOR = ((71, 71, 71), '#474747')
    grey29: T_COLOR = ((74, 74, 74), '#4A4A4A')
    grey30: T_COLOR = ((77, 77, 77), '#4D4D4D')
    grey31: T_COLOR = ((79, 79, 79), '#4F4F4F')
    grey32: T_COLOR = ((82, 82, 82), '#525252')
    grey33: T_COLOR = ((84, 84, 84), '#545454')
    grey34: T_COLOR = ((87, 87, 87), '#575757')
    grey35: T_COLOR = ((89, 89, 89), '#595959')
    grey36: T_COLOR = ((92, 92, 92), '#5C5C5C')
    grey37: T_COLOR = ((94, 94, 94), '#5E5E5E')
    grey38: T_COLOR = ((97, 97, 97), '#616161')
    grey39: T_COLOR = ((99, 99, 99), '#636363')
    grey40: T_COLOR = ((102, 102, 102), '#666666')
    grey41_dimgrey: T_COLOR = ((105, 105, 105), '#696969')
    grey42: T_COLOR = ((107, 107, 107), '#6B6B6B')
    grey43: T_COLOR = ((110, 110, 110), '#6E6E6E')
    grey44: T_COLOR = ((112, 112, 112), '#707070')
    grey45: T_COLOR = ((115, 115, 115), '#737373')
    grey46: T_COLOR = ((117, 117, 117), '#757575')
    grey47: T_COLOR = ((120, 120, 120), '#787878')
    grey48: T_COLOR = ((122, 122, 122), '#7A7A7A')
    grey49: T_COLOR = ((125, 125, 125), '#7D7D7D')
    grey50: T_COLOR = ((127, 127, 127), '#7F7F7F')
    grey51: T_COLOR = ((130, 130, 130), '#828282')
    grey52: T_COLOR = ((133, 133, 133), '#858585')
    grey53: T_COLOR = ((135, 135, 135), '#878787')
    grey54: T_COLOR = ((138, 138, 138), '#8A8A8A')
    grey55: T_COLOR = ((140, 140, 140), '#8C8C8C')
    grey56: T_COLOR = ((143, 143, 143), '#8F8F8F')
    grey57: T_COLOR = ((145, 145, 145), '#919191')
    grey58: T_COLOR = ((148, 148, 148), '#949494')
    grey59: T_COLOR = ((150, 150, 150), '#969696')
    grey60: T_COLOR = ((153, 153, 153), '#999999')
    grey61: T_COLOR = ((156, 156, 156), '#9C9C9C')
    grey62: T_COLOR = ((158, 158, 158), '#9E9E9E')
    grey63: T_COLOR = ((161, 161, 161), '#A1A1A1')
    grey64: T_COLOR = ((163, 163, 163), '#A3A3A3')
    grey65: T_COLOR = ((166, 166, 166), '#A6A6A6')
    grey66: T_COLOR = ((168, 168, 168), '#A8A8A8')
    grey67: T_COLOR = ((171, 171, 171), '#ABABAB')
    grey68: T_COLOR = ((173, 173, 173), '#ADADAD')
    grey69: T_COLOR = ((176, 176, 176), '#B0B0B0')
    grey70: T_COLOR = ((179, 179, 179), '#B3B3B3')
    grey71: T_COLOR = ((181, 181, 181), '#B5B5B5')
    grey72: T_COLOR = ((184, 184, 184), '#B8B8B8')
    grey73: T_COLOR = ((186, 186, 186), '#BABABA')
    grey74: T_COLOR = ((189, 189, 189), '#BDBDBD')
    grey75: T_COLOR = ((191, 191, 191), '#BFBFBF')
    grey76: T_COLOR = ((194, 194, 194), '#C2C2C2')
    grey77: T_COLOR = ((196, 196, 196), '#C4C4C4')
    grey78: T_COLOR = ((199, 199, 199), '#C7C7C7')
    grey79: T_COLOR = ((201, 201, 201), '#C9C9C9')
    grey80: T_COLOR = ((204, 204, 204), '#CCCCCC')
    grey81: T_COLOR = ((207, 207, 207), '#CFCFCF')
    grey82: T_COLOR = ((209, 209, 209), '#D1D1D1')
    grey83: T_COLOR = ((212, 212, 212), '#D4D4D4')
    grey84: T_COLOR = ((214, 214, 214), '#D6D6D6')
    grey85: T_COLOR = ((217, 217, 217), '#D9D9D9')
    grey86: T_COLOR = ((219, 219, 219), '#DBDBDB')
    grey87: T_COLOR = ((222, 222, 222), '#DEDEDE')
    grey88: T_COLOR = ((224, 224, 224), '#E0E0E0')
    grey89: T_COLOR = ((227, 227, 227), '#E3E3E3')
    grey90: T_COLOR = ((229, 229, 229), '#E5E5E5')
    grey91: T_COLOR = ((232, 232, 232), '#E8E8E8')
    grey92: T_COLOR = ((235, 235, 235), '#EBEBEB')
    grey93: T_COLOR = ((237, 237, 237), '#EDEDED')
    grey94: T_COLOR = ((240, 240, 240), '#F0F0F0')
    grey95: T_COLOR = ((242, 242, 242), '#F2F2F2')
    grey96: T_COLOR = ((245, 245, 245), '#F5F5F5')
    grey97: T_COLOR = ((247, 247, 247), '#F7F7F7')
    grey98: T_COLOR = ((250, 250, 250), '#FAFAFA')
    grey99: T_COLOR = ((252, 252, 252), '#FCFCFC')
    grey100_white: T_COLOR = ((255, 255, 255), '#FFFFFF')
    dark_slate_grey: T_COLOR = ((47, 79, 79), '#2F4F4F')
    dim_grey: T_COLOR = ((84, 84, 84), '#545454')
    very_light_grey: T_COLOR = ((205, 205, 205), '#CDCDCD')
    free_speech_grey: T_COLOR = ((99, 86, 136), '#635688')
    aliceblue: T_COLOR = ((240, 248, 255), '#F0F8FF')
    blueviolet: T_COLOR = ((138, 43, 226), '#8A2BE2')
    cadet_blue: T_COLOR = ((95, 159, 159), '#5F9F9F')
    cadetblue: T_COLOR = ((95, 158, 160), '#5F9EA0')
    cadetblue5: T_COLOR = ((95, 158, 160), '#5F9EA0')
    cadetblue1: T_COLOR = ((152, 245, 255), '#98F5FF')
    cadetblue2: T_COLOR = ((142, 229, 238), '#8EE5EE')
    cadetblue3: T_COLOR = ((122, 197, 205), '#7AC5CD')
    cadetblue4: T_COLOR = ((83, 134, 139), '#53868B')
    corn_flower_blue: T_COLOR = ((66, 66, 111), '#42426F')
    cornflowerblue: T_COLOR = ((100, 149, 237), '#6495ED')
    darkslateblue: T_COLOR = ((72, 61, 139), '#483D8B')
    darkturquoise: T_COLOR = ((0, 206, 209), '#00CED1')
    deepskyblue: T_COLOR = ((0, 191, 255), '#00BFFF')
    deepskyblue1: T_COLOR = ((0, 191, 255), '#00BFFF')
    deepskyblue2: T_COLOR = ((0, 178, 238), '#00B2EE')
    deepskyblue3: T_COLOR = ((0, 154, 205), '#009ACD')
    deepskyblue4: T_COLOR = ((0, 104, 139), '#00688B')
    dodgerblue: T_COLOR = ((30, 144, 255), '#1E90FF')
    dodgerblue1: T_COLOR = ((30, 144, 255), '#1E90FF')
    dodgerblue2: T_COLOR = ((28, 134, 238), '#1C86EE')
    dodgerblue3: T_COLOR = ((24, 116, 205), '#1874CD')
    dodgerblue4: T_COLOR = ((16, 78, 139), '#104E8B')
    lightblue: T_COLOR = ((173, 216, 230), '#ADD8E6')
    lightblue1: T_COLOR = ((191, 239, 255), '#BFEFFF')
    lightblue2: T_COLOR = ((178, 223, 238), '#B2DFEE')
    lightblue3: T_COLOR = ((154, 192, 205), '#9AC0CD')
    lightblue4: T_COLOR = ((104, 131, 139), '#68838B')
    lightcyan: T_COLOR = ((224, 255, 255), '#E0FFFF')
    lightcyan1: T_COLOR = ((224, 255, 255), '#E0FFFF')
    lightcyan2: T_COLOR = ((209, 238, 238), '#D1EEEE')
    lightcyan3: T_COLOR = ((180, 205, 205), '#B4CDCD')
    lightcyan4: T_COLOR = ((122, 139, 139), '#7A8B8B')
    lightskyblue: T_COLOR = ((135, 206, 250), '#87CEFA')
    lightskyblue1: T_COLOR = ((176, 226, 255), '#B0E2FF')
    lightskyblue2: T_COLOR = ((164, 211, 238), '#A4D3EE')
    lightskyblue3: T_COLOR = ((141, 182, 205), '#8DB6CD')
    lightskyblue4: T_COLOR = ((96, 123, 139), '#607B8B')
    lightslateblue: T_COLOR = ((132, 112, 255), '#8470FF')
    lightsteelblue: T_COLOR = ((176, 196, 222), '#B0C4DE')
    lightsteelblue1: T_COLOR = ((202, 225, 255), '#CAE1FF')
    lightsteelblue2: T_COLOR = ((188, 210, 238), '#BCD2EE')
    lightsteelblue3: T_COLOR = ((162, 181, 205), '#A2B5CD')
    lightsteelblue4: T_COLOR = ((110, 123, 139), '#6E7B8B')
    aquamarine: T_COLOR = ((112, 219, 147), '#70DB93')
    mediumblue: T_COLOR = ((0, 0, 205), '#0000CD')
    mediumslateblue: T_COLOR = ((123, 104, 238), '#7B68EE')
    mediumturquoise: T_COLOR = ((72, 209, 204), '#48D1CC')
    midnightblue: T_COLOR = ((25, 25, 112), '#191970')
    navyblue: T_COLOR = ((0, 0, 128), '#000080')
    paleturquoise: T_COLOR = ((175, 238, 238), '#AFEEEE')
    paleturquoise1: T_COLOR = ((187, 255, 255), '#BBFFFF')
    paleturquoise2: T_COLOR = ((174, 238, 238), '#AEEEEE')
    paleturquoise3: T_COLOR = ((150, 205, 205), '#96CDCD')
    paleturquoise4: T_COLOR = ((102, 139, 139), '#668B8B')
    powderblue: T_COLOR = ((176, 224, 230), '#B0E0E6')
    royalblue: T_COLOR = ((65, 105, 225), '#4169E1')
    royalblue1: T_COLOR = ((72, 118, 255), '#4876FF')
    royalblue2: T_COLOR = ((67, 110, 238), '#436EEE')
    royalblue3: T_COLOR = ((58, 95, 205), '#3A5FCD')
    royalblue4: T_COLOR = ((39, 64, 139), '#27408B')
    royalblue5: T_COLOR = ((0, 34, 102), '#002266')
    skyblue: T_COLOR = ((135, 206, 235), '#87CEEB')
    skyblue1: T_COLOR = ((135, 206, 255), '#87CEFF')
    skyblue2: T_COLOR = ((126, 192, 238), '#7EC0EE')
    skyblue3: T_COLOR = ((108, 166, 205), '#6CA6CD')
    skyblue4: T_COLOR = ((74, 112, 139), '#4A708B')
    slateblue: T_COLOR = ((106, 90, 205), '#6A5ACD')
    slateblue1: T_COLOR = ((131, 111, 255), '#836FFF')
    slateblue2: T_COLOR = ((122, 103, 238), '#7A67EE')
    slateblue3: T_COLOR = ((105, 89, 205), '#6959CD')
    slateblue4: T_COLOR = ((71, 60, 139), '#473C8B')
    steelblue: T_COLOR = ((70, 130, 180), '#4682B4')
    steelblue1: T_COLOR = ((99, 184, 255), '#63B8FF')
    steelblue2: T_COLOR = ((92, 172, 238), '#5CACEE')
    steelblue3: T_COLOR = ((79, 148, 205), '#4F94CD')
    steelblue4: T_COLOR = ((54, 100, 139), '#36648B')
    aquamarine5: T_COLOR = ((127, 255, 212), '#7FFFD4')
    aquamarine1: T_COLOR = ((127, 255, 212), '#7FFFD4')
    aquamarine2: T_COLOR = ((118, 238, 198), '#76EEC6')
    aquamarine3_mediumaquamarine: T_COLOR = ((102, 205, 170), '#66CDAA')
    aquamarine4: T_COLOR = ((69, 139, 116), '#458B74')
    azure: T_COLOR = ((240, 255, 255), '#F0FFFF')
    azure1: T_COLOR = ((240, 255, 255), '#F0FFFF')
    azure2: T_COLOR = ((224, 238, 238), '#E0EEEE')
    azure3: T_COLOR = ((193, 205, 205), '#C1CDCD')
    azure4: T_COLOR = ((131, 139, 139), '#838B8B')
    blue: T_COLOR = ((0, 0, 255), '#0000FF')
    blue1: T_COLOR = ((0, 0, 255), '#0000FF')
    blue2: T_COLOR = ((0, 0, 238), '#0000EE')
    blue3: T_COLOR = ((0, 0, 205), '#0000CD')
    blue4: T_COLOR = ((0, 0, 139), '#00008B')
    aqua: T_COLOR = ((0, 255, 255), '#00FFFF')
    true_iris_blue: T_COLOR = ((3, 180, 204), '#03B4CC')
    cyan: T_COLOR = ((0, 255, 255), '#00FFFF')
    cyan1: T_COLOR = ((0, 255, 255), '#00FFFF')
    cyan2: T_COLOR = ((0, 238, 238), '#00EEEE')
    cyan3: T_COLOR = ((0, 205, 205), '#00CDCD')
    cyan4: T_COLOR = ((0, 139, 139), '#008B8B')
    navy: T_COLOR = ((0, 0, 128), '#000080')
    teal: T_COLOR = ((0, 128, 128), '#008080')
    turquoise: T_COLOR = ((64, 224, 208), '#40E0D0')
    turquoise1: T_COLOR = ((0, 245, 255), '#00F5FF')
    turquoise2: T_COLOR = ((0, 229, 238), '#00E5EE')
    turquoise3: T_COLOR = ((0, 197, 205), '#00C5CD')
    turquoise4: T_COLOR = ((0, 134, 139), '#00868B')
    darkslategray: T_COLOR = ((47, 79, 79), '#2F4F4F')
    darkslategray1: T_COLOR = ((151, 255, 255), '#97FFFF')
    darkslategray2: T_COLOR = ((141, 238, 238), '#8DEEEE')
    darkslategray3: T_COLOR = ((121, 205, 205), '#79CDCD')
    darkslategray4: T_COLOR = ((82, 139, 139), '#528B8B')
    dark_slate_blue: T_COLOR = ((36, 24, 130), '#241882')
    dark_turquoise: T_COLOR = ((112, 147, 219), '#7093DB')
    medium_slate_blue: T_COLOR = ((127, 0, 255), '#7F00FF')
    medium_turquoise: T_COLOR = ((112, 219, 219), '#70DBDB')
    midnight_blue: T_COLOR = ((47, 47, 79), '#2F2F4F')
    navy_blue: T_COLOR = ((35, 35, 142), '#23238E')
    neon_blue: T_COLOR = ((77, 77, 255), '#4D4DFF')
    new_midnight_blue: T_COLOR = ((0, 0, 156), '#00009C')
    rich_blue: T_COLOR = ((89, 89, 171), '#5959AB')
    sky_blue: T_COLOR = ((50, 153, 204), '#3299CC')
    slate_blue: T_COLOR = ((0, 127, 255), '#007FFF')
    summer_sky: T_COLOR = ((56, 176, 222), '#38B0DE')
    iris_blue: T_COLOR = ((3, 180, 200), '#03B4C8')
    free_speech_blue: T_COLOR = ((65, 86, 197), '#4156C5')
    rosybrown: T_COLOR = ((188, 143, 143), '#BC8F8F')
    rosybrown1: T_COLOR = ((255, 193, 193), '#FFC1C1')
    rosybrown2: T_COLOR = ((238, 180, 180), '#EEB4B4')
    rosybrown3: T_COLOR = ((205, 155, 155), '#CD9B9B')
    rosybrown4: T_COLOR = ((139, 105, 105), '#8B6969')
    saddlebrown: T_COLOR = ((139, 69, 19), '#8B4513')
    sandybrown: T_COLOR = ((244, 164, 96), '#F4A460')
    beige: T_COLOR = ((245, 245, 220), '#F5F5DC')
    brown: T_COLOR = ((165, 42, 42), '#A52A2A')
    brown5: T_COLOR = ((166, 42, 42), '#A62A2A')
    brown1: T_COLOR = ((255, 64, 64), '#FF4040')
    brown2: T_COLOR = ((238, 59, 59), '#EE3B3B')
    brown3: T_COLOR = ((205, 51, 51), '#CD3333')
    brown4: T_COLOR = ((139, 35, 35), '#8B2323')
    dark_brown: T_COLOR = ((92, 64, 51), '#5C4033')
    burlywood: T_COLOR = ((222, 184, 135), '#DEB887')
    burlywood1: T_COLOR = ((255, 211, 155), '#FFD39B')
    burlywood2: T_COLOR = ((238, 197, 145), '#EEC591')
    burlywood3: T_COLOR = ((205, 170, 125), '#CDAA7D')
    burlywood4: T_COLOR = ((139, 115, 85), '#8B7355')
    bakers_chocolate: T_COLOR = ((92, 51, 23), '#5C3317')
    chocolate: T_COLOR = ((210, 105, 30), '#D2691E')
    chocolate1: T_COLOR = ((255, 127, 36), '#FF7F24')
    chocolate2: T_COLOR = ((238, 118, 33), '#EE7621')
    chocolate3: T_COLOR = ((205, 102, 29), '#CD661D')
    chocolate4: T_COLOR = ((139, 69, 19), '#8B4513')
    peru: T_COLOR = ((205, 133, 63), '#CD853F')
    tan: T_COLOR = ((210, 180, 140), '#D2B48C')
    tan1: T_COLOR = ((255, 165, 79), '#FFA54F')
    tan2: T_COLOR = ((238, 154, 73), '#EE9A49')
    tan3: T_COLOR = ((205, 133, 63), '#CD853F')
    tan4: T_COLOR = ((139, 90, 43), '#8B5A2B')
    dark_tan: T_COLOR = ((151, 105, 79), '#97694F')
    dark_wood: T_COLOR = ((133, 94, 66), '#855E42')
    light_wood: T_COLOR = ((133, 99, 99), '#856363')
    medium_wood: T_COLOR = ((166, 128, 100), '#A68064')
    new_tan: T_COLOR = ((235, 199, 158), '#EBC79E')
    semi_sweet_chocolate: T_COLOR = ((107, 66, 38), '#6B4226')
    sienna: T_COLOR = ((142, 107, 35), '#8E6B23')
    tan5: T_COLOR = ((219, 147, 112), '#DB9370')
    very_dark_brown: T_COLOR = ((92, 64, 51), '#5C4033')
    dark_green: T_COLOR = ((47, 79, 47), '#2F4F2F')
    darkgreen: T_COLOR = ((0, 100, 0), '#006400')
    dark_green_copper: T_COLOR = ((74, 118, 110), '#4A766E')
    darkkhaki: T_COLOR = ((189, 183, 107), '#BDB76B')
    darkolivegreen: T_COLOR = ((85, 107, 47), '#556B2F')
    darkolivegreen1: T_COLOR = ((202, 255, 112), '#CAFF70')
    darkolivegreen2: T_COLOR = ((188, 238, 104), '#BCEE68')
    darkolivegreen3: T_COLOR = ((162, 205, 90), '#A2CD5A')
    darkolivegreen4: T_COLOR = ((110, 139, 61), '#6E8B3D')
    olive: T_COLOR = ((128, 128, 0), '#808000')
    darkseagreen: T_COLOR = ((143, 188, 143), '#8FBC8F')
    darkseagreen1: T_COLOR = ((193, 255, 193), '#C1FFC1')
    darkseagreen2: T_COLOR = ((180, 238, 180), '#B4EEB4')
    darkseagreen3: T_COLOR = ((155, 205, 155), '#9BCD9B')
    darkseagreen4: T_COLOR = ((105, 139, 105), '#698B69')
    forestgreen: T_COLOR = ((34, 139, 34), '#228B22')
    greenyellow: T_COLOR = ((173, 255, 47), '#ADFF2F')
    lawngreen: T_COLOR = ((124, 252, 0), '#7CFC00')
    lightseagreen: T_COLOR = ((32, 178, 170), '#20B2AA')
    limegreen: T_COLOR = ((50, 205, 50), '#32CD32')
    mediumseagreen: T_COLOR = ((60, 179, 113), '#3CB371')
    mediumspringgreen: T_COLOR = ((0, 250, 154), '#00FA9A')
    mintcream: T_COLOR = ((245, 255, 250), '#F5FFFA')
    olivedrab: T_COLOR = ((107, 142, 35), '#6B8E23')
    olivedrab1: T_COLOR = ((192, 255, 62), '#C0FF3E')
    olivedrab2: T_COLOR = ((179, 238, 58), '#B3EE3A')
    olivedrab3: T_COLOR = ((154, 205, 50), '#9ACD32')
    olivedrab4: T_COLOR = ((105, 139, 34), '#698B22')
    palegreen: T_COLOR = ((152, 251, 152), '#98FB98')
    palegreen1: T_COLOR = ((154, 255, 154), '#9AFF9A')
    palegreen2: T_COLOR = ((144, 238, 144), '#90EE90')
    palegreen3: T_COLOR = ((124, 205, 124), '#7CCD7C')
    palegreen4: T_COLOR = ((84, 139, 84), '#548B54')
    seagreen_seagreen4: T_COLOR = ((46, 139, 87), '#2E8B57')
    seagreen1: T_COLOR = ((84, 255, 159), '#54FF9F')
    seagreen2: T_COLOR = ((78, 238, 148), '#4EEE94')
    seagreen3: T_COLOR = ((67, 205, 128), '#43CD80')
    springgreen: T_COLOR = ((0, 255, 127), '#00FF7F')
    springgreen1: T_COLOR = ((0, 255, 127), '#00FF7F')
    springgreen2: T_COLOR = ((0, 238, 118), '#00EE76')
    springgreen3: T_COLOR = ((0, 205, 102), '#00CD66')
    springgreen4: T_COLOR = ((0, 139, 69), '#008B45')
    yellowgreen: T_COLOR = ((154, 205, 50), '#9ACD32')
    chartreuse: T_COLOR = ((127, 255, 0), '#7FFF00')
    chartreuse1: T_COLOR = ((127, 255, 0), '#7FFF00')
    chartreuse2: T_COLOR = ((118, 238, 0), '#76EE00')
    chartreuse3: T_COLOR = ((102, 205, 0), '#66CD00')
    chartreuse4: T_COLOR = ((69, 139, 0), '#458B00')
    green: T_COLOR = ((0, 255, 0), '#00FF00')
    green5: T_COLOR = ((0, 128, 0), '#008000')
    lime: T_COLOR = ((0, 255, 0), '#00FF00')
    green1: T_COLOR = ((0, 255, 0), '#00FF00')
    green2: T_COLOR = ((0, 238, 0), '#00EE00')
    green3: T_COLOR = ((0, 205, 0), '#00CD00')
    green4: T_COLOR = ((0, 139, 0), '#008B00')
    khaki: T_COLOR = ((240, 230, 140), '#F0E68C')
    khaki1: T_COLOR = ((255, 246, 143), '#FFF68F')
    khaki2: T_COLOR = ((238, 230, 133), '#EEE685')
    khaki3: T_COLOR = ((205, 198, 115), '#CDC673')
    khaki4: T_COLOR = ((139, 134, 78), '#8B864E')
    dark_olive_green: T_COLOR = ((79, 79, 47), '#4F4F2F')
    forest_green_khaki_medium_aquamarine: T_COLOR = ((35, 142, 35), '#238E23')
    medium_forest_green: T_COLOR = ((219, 219, 112), '#DBDB70')
    medium_sea_green: T_COLOR = ((66, 111, 66), '#426F42')
    medium_spring_green: T_COLOR = ((127, 255, 0), '#7FFF00')
    pale_green: T_COLOR = ((143, 188, 143), '#8FBC8F')
    sea_green: T_COLOR = ((35, 142, 104), '#238E68')
    spring_green: T_COLOR = ((0, 255, 127), '#00FF7F')
    free_speech_green: T_COLOR = ((9, 249, 17), '#09F911')
    free_speech_aquamarine: T_COLOR = ((2, 157, 116), '#029D74')
    darkorange: T_COLOR = ((255, 140, 0), '#FF8C00')
    darkorange1: T_COLOR = ((255, 127, 0), '#FF7F00')
    darkorange2: T_COLOR = ((238, 118, 0), '#EE7600')
    darkorange3: T_COLOR = ((205, 102, 0), '#CD6600')
    darkorange4: T_COLOR = ((139, 69, 0), '#8B4500')
    darksalmon: T_COLOR = ((233, 150, 122), '#E9967A')
    lightcoral: T_COLOR = ((240, 128, 128), '#F08080')
    lightsalmon: T_COLOR = ((255, 160, 122), '#FFA07A')
    lightsalmon1: T_COLOR = ((255, 160, 122), '#FFA07A')
    lightsalmon2: T_COLOR = ((238, 149, 114), '#EE9572')
    lightsalmon3: T_COLOR = ((205, 129, 98), '#CD8162')
    lightsalmon4: T_COLOR = ((139, 87, 66), '#8B5742')
    peachpuff: T_COLOR = ((255, 218, 185), '#FFDAB9')
    peachpuff1: T_COLOR = ((255, 218, 185), '#FFDAB9')
    peachpuff2: T_COLOR = ((238, 203, 173), '#EECBAD')
    peachpuff3: T_COLOR = ((205, 175, 149), '#CDAF95')
    peachpuff4: T_COLOR = ((139, 119, 101), '#8B7765')
    bisque: T_COLOR = ((255, 228, 196), '#FFE4C4')
    bisque1: T_COLOR = ((255, 228, 196), '#FFE4C4')
    bisque2: T_COLOR = ((238, 213, 183), '#EED5B7')
    bisque3: T_COLOR = ((205, 183, 158), '#CDB79E')
    bisque4: T_COLOR = ((139, 125, 107), '#8B7D6B')
    coral: T_COLOR = ((255, 127, 0), '#FF7F00')
    coral5: T_COLOR = ((255, 127, 80), '#FF7F50')
    coral1: T_COLOR = ((255, 114, 86), '#FF7256')
    coral2: T_COLOR = ((238, 106, 80), '#EE6A50')
    coral3: T_COLOR = ((205, 91, 69), '#CD5B45')
    coral4: T_COLOR = ((139, 62, 47), '#8B3E2F')
    honeydew: T_COLOR = ((240, 255, 240), '#F0FFF0')
    honeydew1: T_COLOR = ((240, 255, 240), '#F0FFF0')
    honeydew2: T_COLOR = ((224, 238, 224), '#E0EEE0')
    honeydew3: T_COLOR = ((193, 205, 193), '#C1CDC1')
    honeydew4: T_COLOR = ((131, 139, 131), '#838B83')
    orange: T_COLOR = ((255, 165, 0), '#FFA500')
    orange1: T_COLOR = ((255, 165, 0), '#FFA500')
    orange2: T_COLOR = ((238, 154, 0), '#EE9A00')
    orange3: T_COLOR = ((205, 133, 0), '#CD8500')
    orange4: T_COLOR = ((139, 90, 0), '#8B5A00')
    salmon: T_COLOR = ((250, 128, 114), '#FA8072')
    salmon1: T_COLOR = ((255, 140, 105), '#FF8C69')
    salmon2: T_COLOR = ((238, 130, 98), '#EE8262')
    salmon3: T_COLOR = ((205, 112, 84), '#CD7054')
    salmon4: T_COLOR = ((139, 76, 57), '#8B4C39')
    sienna5: T_COLOR = ((160, 82, 45), '#A0522D')
    sienna1: T_COLOR = ((255, 130, 71), '#FF8247')
    sienna2: T_COLOR = ((238, 121, 66), '#EE7942')
    sienna3: T_COLOR = ((205, 104, 57), '#CD6839')
    sienna4: T_COLOR = ((139, 71, 38), '#8B4726')
    mandarian_orange: T_COLOR = ((142, 35, 35), '#8E2323')
    orange5: T_COLOR = ((255, 127, 0), '#FF7F00')
    orange_red: T_COLOR = ((255, 36, 0), '#FF2400')
    deeppink: T_COLOR = ((255, 20, 147), '#FF1493')
    deeppink1: T_COLOR = ((255, 20, 147), '#FF1493')
    deeppink2: T_COLOR = ((238, 18, 137), '#EE1289')
    deeppink3: T_COLOR = ((205, 16, 118), '#CD1076')
    deeppink4: T_COLOR = ((139, 10, 80), '#8B0A50')
    hotpink: T_COLOR = ((255, 105, 180), '#FF69B4')
    hotpink1: T_COLOR = ((255, 110, 180), '#FF6EB4')
    hotpink2: T_COLOR = ((238, 106, 167), '#EE6AA7')
    hotpink3: T_COLOR = ((205, 96, 144), '#CD6090')
    hotpink4: T_COLOR = ((139, 58, 98), '#8B3A62')
    indianred: T_COLOR = ((205, 92, 92), '#CD5C5C')
    indianred1: T_COLOR = ((255, 106, 106), '#FF6A6A')
    indianred2: T_COLOR = ((238, 99, 99), '#EE6363')
    indianred3: T_COLOR = ((205, 85, 85), '#CD5555')
    indianred4: T_COLOR = ((139, 58, 58), '#8B3A3A')
    lightpink: T_COLOR = ((255, 182, 193), '#FFB6C1')
    lightpink1: T_COLOR = ((255, 174, 185), '#FFAEB9')
    lightpink2: T_COLOR = ((238, 162, 173), '#EEA2AD')
    lightpink3: T_COLOR = ((205, 140, 149), '#CD8C95')
    lightpink4: T_COLOR = ((139, 95, 101), '#8B5F65')
    mediumvioletred: T_COLOR = ((199, 21, 133), '#C71585')
    mistyrose: T_COLOR = ((255, 228, 225), '#FFE4E1')
    mistyrose1: T_COLOR = ((255, 228, 225), '#FFE4E1')
    mistyrose2: T_COLOR = ((238, 213, 210), '#EED5D2')
    mistyrose3: T_COLOR = ((205, 183, 181), '#CDB7B5')
    mistyrose4: T_COLOR = ((139, 125, 123), '#8B7D7B')
    orangered: T_COLOR = ((255, 69, 0), '#FF4500')
    orangered1: T_COLOR = ((255, 69, 0), '#FF4500')
    orangered2: T_COLOR = ((238, 64, 0), '#EE4000')
    orangered3: T_COLOR = ((205, 55, 0), '#CD3700')
    orangered4: T_COLOR = ((139, 37, 0), '#8B2500')
    palevioletred: T_COLOR = ((219, 112, 147), '#DB7093')
    palevioletred1: T_COLOR = ((255, 130, 171), '#FF82AB')
    palevioletred2: T_COLOR = ((238, 121, 159), '#EE799F')
    palevioletred3: T_COLOR = ((205, 104, 137), '#CD6889')
    palevioletred4: T_COLOR = ((139, 71, 93), '#8B475D')
    violetred: T_COLOR = ((208, 32, 144), '#D02090')
    violetred1: T_COLOR = ((255, 62, 150), '#FF3E96')
    violetred2: T_COLOR = ((238, 58, 140), '#EE3A8C')
    violetred3: T_COLOR = ((205, 50, 120), '#CD3278')
    violetred4: T_COLOR = ((139, 34, 82), '#8B2252')
    firebrick: T_COLOR = ((178, 34, 34), '#B22222')
    firebrick1: T_COLOR = ((255, 48, 48), '#FF3030')
    firebrick2: T_COLOR = ((238, 44, 44), '#EE2C2C')
    firebrick3: T_COLOR = ((205, 38, 38), '#CD2626')
    firebrick4: T_COLOR = ((139, 26, 26), '#8B1A1A')
    pink: T_COLOR = ((255, 192, 203), '#FFC0CB')
    pink1: T_COLOR = ((255, 181, 197), '#FFB5C5')
    pink2: T_COLOR = ((238, 169, 184), '#EEA9B8')
    pink3: T_COLOR = ((205, 145, 158), '#CD919E')
    pink4: T_COLOR = ((139, 99, 108), '#8B636C')
    flesh: T_COLOR = ((245, 204, 176), '#F5CCB0')
    feldspar: T_COLOR = ((209, 146, 117), '#D19275')
    red: T_COLOR = ((255, 0, 0), '#FF0000')
    red1: T_COLOR = ((255, 0, 0), '#FF0000')
    red2: T_COLOR = ((238, 0, 0), '#EE0000')
    red3: T_COLOR = ((205, 0, 0), '#CD0000')
    red4: T_COLOR = ((139, 0, 0), '#8B0000')
    tomato: T_COLOR = ((255, 99, 71), '#FF6347')
    tomato1: T_COLOR = ((255, 99, 71), '#FF6347')
    tomato2: T_COLOR = ((238, 92, 66), '#EE5C42')
    tomato3: T_COLOR = ((205, 79, 57), '#CD4F39')
    tomato4: T_COLOR = ((139, 54, 38), '#8B3626')
    dusty_rose: T_COLOR = ((133, 99, 99), '#856363')
    firebrick5: T_COLOR = ((142, 35, 35), '#8E2323')
    indian_red: T_COLOR = ((245, 204, 176), '#F5CCB0')
    pink5: T_COLOR = ((188, 143, 143), '#BC8F8F')
    salmon5: T_COLOR = ((111, 66, 66), '#6F4242')
    scarlet: T_COLOR = ((140, 23, 23), '#8C1717')
    spicy_pink: T_COLOR = ((255, 28, 174), '#FF1CAE')
    free_speech_magenta: T_COLOR = ((227, 91, 216), '#E35BD8')
    free_speech_red: T_COLOR = ((192, 0, 0), '#C00000')
    darkorchid: T_COLOR = ((153, 50, 204), '#9932CC')
    darkorchid1: T_COLOR = ((191, 62, 255), '#BF3EFF')
    darkorchid2: T_COLOR = ((178, 58, 238), '#B23AEE')
    darkorchid3: T_COLOR = ((154, 50, 205), '#9A32CD')
    darkorchid4: T_COLOR = ((104, 34, 139), '#68228B')
    darkviolet: T_COLOR = ((148, 0, 211), '#9400D3')
    lavenderblush: T_COLOR = ((255, 240, 245), '#FFF0F5')
    lavenderblush1: T_COLOR = ((255, 240, 245), '#FFF0F5')
    lavenderblush2: T_COLOR = ((238, 224, 229), '#EEE0E5')
    lavenderblush3: T_COLOR = ((205, 193, 197), '#CDC1C5')
    lavenderblush4: T_COLOR = ((139, 131, 134), '#8B8386')
    mediumorchid: T_COLOR = ((186, 85, 211), '#BA55D3')
    mediumorchid1: T_COLOR = ((224, 102, 255), '#E066FF')
    mediumorchid2: T_COLOR = ((209, 95, 238), '#D15FEE')
    mediumorchid3: T_COLOR = ((180, 82, 205), '#B452CD')
    mediumorchid4: T_COLOR = ((122, 55, 139), '#7A378B')
    mediumpurple: T_COLOR = ((147, 112, 219), '#9370DB')
    medium_orchid: T_COLOR = ((147, 112, 219), '#9370DB')
    mediumpurple1: T_COLOR = ((171, 130, 255), '#AB82FF')
    dark_orchid: T_COLOR = ((153, 50, 205), '#9932CD')
    mediumpurple2: T_COLOR = ((159, 121, 238), '#9F79EE')
    mediumpurple3: T_COLOR = ((137, 104, 205), '#8968CD')
    mediumpurple4: T_COLOR = ((93, 71, 139), '#5D478B')
    lavender: T_COLOR = ((230, 230, 250), '#E6E6FA')
    magenta: T_COLOR = ((255, 0, 255), '#FF00FF')
    fuchsia: T_COLOR = ((255, 0, 255), '#FF00FF')
    magenta1: T_COLOR = ((255, 0, 255), '#FF00FF')
    magenta2: T_COLOR = ((238, 0, 238), '#EE00EE')
    magenta3: T_COLOR = ((205, 0, 205), '#CD00CD')
    magenta4: T_COLOR = ((139, 0, 139), '#8B008B')
    maroon: T_COLOR = ((176, 48, 96), '#B03060')
    maroon1: T_COLOR = ((255, 52, 179), '#FF34B3')
    maroon2: T_COLOR = ((238, 48, 167), '#EE30A7')
    maroon3: T_COLOR = ((205, 41, 144), '#CD2990')
    maroon4: T_COLOR = ((139, 28, 98), '#8B1C62')
    orchid: T_COLOR = ((218, 112, 214), '#DA70D6')
    orchid5: T_COLOR = ((219, 112, 219), '#DB70DB')
    orchid1: T_COLOR = ((255, 131, 250), '#FF83FA')
    orchid2: T_COLOR = ((238, 122, 233), '#EE7AE9')
    orchid3: T_COLOR = ((205, 105, 201), '#CD69C9')
    orchid4: T_COLOR = ((139, 71, 137), '#8B4789')
    plum: T_COLOR = ((221, 160, 221), '#DDA0DD')
    plum1: T_COLOR = ((255, 187, 255), '#FFBBFF')
    plum2: T_COLOR = ((238, 174, 238), '#EEAEEE')
    plum3: T_COLOR = ((205, 150, 205), '#CD96CD')
    plum4: T_COLOR = ((139, 102, 139), '#8B668B')
    purple: T_COLOR = ((160, 32, 240), '#A020F0')
    purple5: T_COLOR = ((128, 0, 128), '#800080')
    purple1: T_COLOR = ((155, 48, 255), '#9B30FF')
    purple2: T_COLOR = ((145, 44, 238), '#912CEE')
    purple3: T_COLOR = ((125, 38, 205), '#7D26CD')
    purple4: T_COLOR = ((85, 26, 139), '#551A8B')
    thistle: T_COLOR = ((216, 191, 216), '#D8BFD8')
    thistle1: T_COLOR = ((255, 225, 255), '#FFE1FF')
    thistle2: T_COLOR = ((238, 210, 238), '#EED2EE')
    thistle3: T_COLOR = ((205, 181, 205), '#CDB5CD')
    thistle4: T_COLOR = ((139, 123, 139), '#8B7B8B')
    violet: T_COLOR = ((238, 130, 238), '#EE82EE')
    violet_blue: T_COLOR = ((159, 95, 159), '#9F5F9F')
    dark_purple: T_COLOR = ((135, 31, 120), '#871F78')
    maroon5: T_COLOR = ((128, 0, 0), '#800000')
    medium_violet_red: T_COLOR = ((219, 112, 147), '#DB7093')
    neon_pink: T_COLOR = ((255, 110, 199), '#FF6EC7')
    plum5: T_COLOR = ((234, 173, 234), '#EAADEA')
    thistle5: T_COLOR = ((216, 191, 216), '#D8BFD8')
    turquoise5: T_COLOR = ((173, 234, 234), '#ADEAEA')
    violet5: T_COLOR = ((79, 47, 79), '#4F2F4F')
    violet_red: T_COLOR = ((204, 50, 153), '#CC3299')
    antiquewhite: T_COLOR = ((250, 235, 215), '#FAEBD7')
    antiquewhite1: T_COLOR = ((255, 239, 219), '#FFEFDB')
    antiquewhite2: T_COLOR = ((238, 223, 204), '#EEDFCC')
    antiquewhite3: T_COLOR = ((205, 192, 176), '#CDC0B0')
    antiquewhite4: T_COLOR = ((139, 131, 120), '#8B8378')
    floralwhite: T_COLOR = ((255, 250, 240), '#FFFAF0')
    ghostwhite: T_COLOR = ((248, 248, 255), '#F8F8FF')
    navajowhite: T_COLOR = ((255, 222, 173), '#FFDEAD')
    navajowhite1: T_COLOR = ((255, 222, 173), '#FFDEAD')
    navajowhite2: T_COLOR = ((238, 207, 161), '#EECFA1')
    navajowhite3: T_COLOR = ((205, 179, 139), '#CDB38B')
    navajowhite4: T_COLOR = ((139, 121, 94), '#8B795E')
    oldlace: T_COLOR = ((253, 245, 230), '#FDF5E6')
    whitesmoke: T_COLOR = ((245, 245, 245), '#F5F5F5')
    gainsboro: T_COLOR = ((220, 220, 220), '#DCDCDC')
    ivory: T_COLOR = ((255, 255, 240), '#FFFFF0')
    ivory1: T_COLOR = ((255, 255, 240), '#FFFFF0')
    ivory2: T_COLOR = ((238, 238, 224), '#EEEEE0')
    ivory3: T_COLOR = ((205, 205, 193), '#CDCDC1')
    ivory4: T_COLOR = ((139, 139, 131), '#8B8B83')
    linen: T_COLOR = ((250, 240, 230), '#FAF0E6')
    seashell: T_COLOR = ((255, 245, 238), '#FFF5EE')
    seashell1: T_COLOR = ((255, 245, 238), '#FFF5EE')
    seashell2: T_COLOR = ((238, 229, 222), '#EEE5DE')
    seashell3: T_COLOR = ((205, 197, 191), '#CDC5BF')
    seashell4: T_COLOR = ((139, 134, 130), '#8B8682')
    snow: T_COLOR = ((255, 250, 250), '#FFFAFA')
    snow1: T_COLOR = ((255, 250, 250), '#FFFAFA')
    snow2: T_COLOR = ((238, 233, 233), '#EEE9E9')
    snow3: T_COLOR = ((205, 201, 201), '#CDC9C9')
    snow4: T_COLOR = ((139, 137, 137), '#8B8989')
    wheat: T_COLOR = ((245, 222, 179), '#F5DEB3')
    wheat1: T_COLOR = ((255, 231, 186), '#FFE7BA')
    wheat2: T_COLOR = ((238, 216, 174), '#EED8AE')
    wheat3: T_COLOR = ((205, 186, 150), '#CDBA96')
    wheat4: T_COLOR = ((139, 126, 102), '#8B7E66')
    white: T_COLOR = ((255, 255, 255), '#FFFFFF')
    quartz: T_COLOR = ((217, 217, 243), '#D9D9F3')
    wheat5: T_COLOR = ((216, 216, 191), '#D8D8BF')
    blanchedalmond: T_COLOR = ((255, 235, 205), '#FFEBCD')
    darkgoldenrod: T_COLOR = ((184, 134, 11), '#B8860B')
    darkgoldenrod1: T_COLOR = ((255, 185, 15), '#FFB90F')
    darkgoldenrod2: T_COLOR = ((238, 173, 14), '#EEAD0E')
    darkgoldenrod3: T_COLOR = ((205, 149, 12), '#CD950C')
    darkgoldenrod4: T_COLOR = ((139, 101, 8), '#8B6508')
    lemonchiffon: T_COLOR = ((255, 250, 205), '#FFFACD')
    lemonchiffon1: T_COLOR = ((255, 250, 205), '#FFFACD')
    lemonchiffon2: T_COLOR = ((238, 233, 191), '#EEE9BF')
    lemonchiffon3: T_COLOR = ((205, 201, 165), '#CDC9A5')
    lemonchiffon4: T_COLOR = ((139, 137, 112), '#8B8970')
    lightgoldenrod: T_COLOR = ((238, 221, 130), '#EEDD82')
    lightgoldenrod1: T_COLOR = ((255, 236, 139), '#FFEC8B')
    lightgoldenrod2: T_COLOR = ((238, 220, 130), '#EEDC82')
    lightyellow1: T_COLOR = ((255, 255, 224), '#FFFFE0')
    lightgoldenrodyellow: T_COLOR = ((250, 250, 210), '#FAFAD2')
    lightyellow: T_COLOR = ((255, 255, 224), '#FFFFE0')
    lightyellow2: T_COLOR = ((238, 238, 209), '#EEEED1')
    lightyellow3: T_COLOR = ((205, 205, 180), '#CDCDB4')
    lightyellow4: T_COLOR = ((139, 139, 122), '#8B8B7A')
    palegoldenrod: T_COLOR = ((238, 232, 170), '#EEE8AA')
    papayawhip: T_COLOR = ((255, 239, 213), '#FFEFD5')
    cornsilk: T_COLOR = ((255, 248, 220), '#FFF8DC')
    cornsilk1: T_COLOR = ((255, 248, 220), '#FFF8DC')
    cornsilk2: T_COLOR = ((238, 232, 205), '#EEE8CD')
    cornsilk3: T_COLOR = ((205, 200, 177), '#CDC8B1')
    cornsilk4: T_COLOR = ((139, 136, 120), '#8B8878')
    goldenrod: T_COLOR = ((218, 165, 32), '#DAA520')
    goldenrod1: T_COLOR = ((255, 193, 37), '#FFC125')
    goldenrod2: T_COLOR = ((238, 180, 34), '#EEB422')
    goldenrod3: T_COLOR = ((205, 155, 29), '#CD9B1D')
    goldenrod4: T_COLOR = ((139, 105, 20), '#8B6914')
    moccasin: T_COLOR = ((255, 228, 181), '#FFE4B5')
    yellow1: T_COLOR = ((255, 255, 0), '#FFFF00')
    yellow2: T_COLOR = ((238, 238, 0), '#EEEE00')
    yellow3: T_COLOR = ((205, 205, 0), '#CDCD00')
    yellow4: T_COLOR = ((139, 139, 0), '#8B8B00')
    gold: T_COLOR = ((255, 215, 0), '#FFD700')
    gold1: T_COLOR = ((255, 215, 0), '#FFD700')
    gold2: T_COLOR = ((238, 201, 0), '#EEC900')
    gold3: T_COLOR = ((205, 173, 0), '#CDAD00')
    gold4: T_COLOR = ((139, 117, 0), '#8B7500')
    goldenrod5: T_COLOR = ((219, 219, 112), '#DBDB70')
    medium_goldenrod: T_COLOR = ((234, 234, 174), '#EAEAAE')
    yellow_green: T_COLOR = ((153, 204, 50), '#99CC32')
    copper: T_COLOR = ((184, 115, 51), '#B87333')
    cool_copper: T_COLOR = ((217, 135, 25), '#D98719')
    green_copper: T_COLOR = ((133, 99, 99), '#856363')
    brass: T_COLOR = ((181, 166, 66), '#B5A642')
    bronze: T_COLOR = ((140, 120, 83), '#8C7853')
    bronze_ii: T_COLOR = ((166, 125, 61), '#A67D3D')
    bright_gold: T_COLOR = ((217, 217, 25), '#D9D919')
    old_gold: T_COLOR = ((207, 181, 59), '#CFB53B')
    css_gold: T_COLOR = ((204, 153, 0), '#CC9900')
    gold5: T_COLOR = ((205, 127, 50), '#CD7F32')
    silver: T_COLOR = ((230, 232, 250), '#E6E8FA')
    silver_grey: T_COLOR = ((192, 192, 192), '#C0C0C0')
    light_steel_blue: T_COLOR = ((84, 84, 84), '#545454')
    steel_blue: T_COLOR = ((35, 107, 142), '#236B8E')
    lightgoldenrod3: T_COLOR = ((205, 190, 112), '#CDBE70')
    lightgoldenrod4: T_COLOR = ((139, 129, 76), '#8B814C')
    yellow: T_COLOR = ((255, 255, 0), '#FFFF00')


Colors.ALL = tuple(x for x in dir(Colors) if not x.startswith('_'))
# Colors.ALL.__doc__ = """ Names of all available colors in Colors. """
Colors.is_color = lambda s: s in Colors.ALL
Colors.is_color.__doc__ = """ Whether a given color's name is available in Colors. """
Colors.get_color = lambda i: getattr(Colors, Colors.ALL[i])
Colors.get_color.__doc__ = """ In name order, give the name of the color with a given index. """
Colors.get_number = lambda s: Colors.ALL.index(s)
Colors.get_number.__doc__ = """ In name order, give the index of the color with a given name. """


def test_colors():
    import simple_tools.reporter
    spi: simple_tools.reporter.Reporter = simple_tools.reporter.Reporter(256 ** 4)
    error = []
    for r in range(256):
        for g in range(256):
            for b in range(256):
                for a in range(256):
                    spi.add_step()
                    rgb = (r, g, b, a)
                    hx = rgb_to_hex(*rgb)
                    fhx = hex_to_rgb(hx)
                    if not (rgb == fhx):
                        error.append([rgb, hx, fhx])
    spi.stop()
    print(error)
    input('Done ')


if __name__ == '__main__':
    test_colors()