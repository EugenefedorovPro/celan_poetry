import ipdb
import fitz  # PyMuPDF


doc = fitz.open("celan.pdf")
texts = [page.get_text("text") for page in doc]
ipdb.set_trace()
print(texts[2])

# In [29]: import pymupdf


# In [29]: doc = pymupdf.open(path)

# In [28]: doc[2].get_text("dict")["blocks"][1]
# Out[28]:
# {'type': 0,
#  'number': 1,
#  'flags': 0,
#  'bbox': (89.87999725341797,
#   124.52349853515625,
#   224.908447265625,
#   139.99935913085938),
#  'lines': [{'spans': [{'size': 13.979999542236328,
#      'flags': 20,
#      'bidi': 0,
#      'char_flags': 24,
#      'font': 'TimesNewRomanPS-BoldMT',
#      'color': 0,
#      'alpha': 255,
#      'ascender': 0.890999972820282,
#      'descender': -0.2160000056028366,
#      'text': 'Ein Lied in der Wüste ',
#      'origin': (89.87999725341797, 136.97967529296875),
#      'bbox': (89.87999725341797,
#       124.52349853515625,
#       224.908447265625,
#       139.99935913085938)}],
#    'wmode': 0,
#    'dir': (1.0, 0.0),
#    'bbox': (89.87999725341797,
#     124.52349853515625,
#     224.908447265625,
#     139.99935913085938)}]}
