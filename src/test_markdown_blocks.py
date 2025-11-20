from markdown_blocks import *
import unittest
class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is the first paragraph.

This is the second paragraph."""
        expected_blocks = [
            "This is the first paragraph.",
            "This is the second paragraph."
        ]
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, expected_blocks)
    def test_block_to_block_type(self):
        test_cases = {
            "# Heading 1": BlockType.HEADING,
            "```python\nprint('Hello, World!')\n```": BlockType.CODE,
            "> This is a quote.\n> It has multiple lines.": BlockType.QUOTE,
            "- Item 1\n- Item 2\n- Item 3": BlockType.ULIST,
            "1. First item\n2. Second item\n3. Third item": BlockType.OLIST,
            "This is a simple paragraph.": BlockType.PARAGRAPH,
        }
        for block, expected_type in test_cases.items():
            with self.subTest(block=block):
                block_type = block_to_block_type(block)
                self.assertEqual(block_type, expected_type)
    def test_empty_blocks(self):
        markdown = "\n\nThis is a paragraph after empty blocks.\n\n"
        expected_blocks = [
            "This is a paragraph after empty blocks."
        ]
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, expected_blocks)
if __name__ == "__main__":
    unittest.main()