from .mappings import MAPPINGS

def name(code):
    return MAPPINGS.get(code, code)