import pathlib
from pygame import font
fontsPath = pathlib.Path(__file__).parent

def getPath(name):
    global fontsPath, fontPaths
    localFontPath = fontPaths.get(name)
    if localFontPath is None:
        return None
    fontPath = fontsPath/localFontPath
    return str(fontPath)

fontPaths = {
    "ROG": "ROGFONTS-REGULAR.ttf",
    "Encode Sans": "EncodeSans_Condensed-SemiBold.ttf",
    "Encode Sans Bold": "EncodeSans_Condensed-SemiBold.ttf"
}

cachedFonts = {} #indexed by tuple (name, size)
    
def getFont(name, size):
    global cachedFonts, fontPaths
    
    fontPath = getPath(name)
    if fontPath is None:
        return None
    
    if cachedFonts.get((name, size)) is None:
        cachedFonts[(name, size)] = font.Font(fontPath, size)
        
    return cachedFonts[(name, size)]