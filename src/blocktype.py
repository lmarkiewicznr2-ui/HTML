from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6
def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(("-", "*", "+")):
        return BlockType.UNORDERED_LIST
    elif block[0:2].isdigit() and block[2:3] == ".":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH