#a module that stores all the fonts used in the game in one easy location

# external imports
import pathlib # for manipulating file paths
from pygame import font # for loading fonts

fontsPath = pathlib.Path(__file__).parent # get the path to the fonts folder

fontPaths = { # a dictionary of all the fonts that can be accessed
    "ROG": "ROGFONTS-REGULAR.otf", # the ROG font
    "Encode Sans": "EncodeSans_Condensed-SemiBold.ttf", # the Encode Sans font
    "Encode Sans Bold": "EncodeSans_Condensed-SemiBold.ttf" # the Encode Sans Bold font
}

def getPath(name): # gets the path to a font from a name
    global fontsPath, fontPaths # globals
    localFontPath = fontPaths.get(name) # get the local font path
    if localFontPath is None: # if the font doesn't exist
        return None # return none
    fontPath = fontsPath/localFontPath #else get the path to the font
    return str(fontPath) # return the path to the font as a string

cachedFonts = {} #dict of all the cached fonts, indexed by tuple (name, size)
    
def getFont(name, size): # gets a font from a name and size
    global cachedFonts, fontPaths # globals
    
    fontPath = getPath(name) # get the path to the font
    if fontPath is None: # if the font doesn't exist
        return None # return none
    
    if cachedFonts.get((name, size)) is None: # if the font isn't cached
        cachedFonts[(name, size)] = font.Font(fontPath, size) # cache the font
        
    return cachedFonts[(name, size)] # return the cached font