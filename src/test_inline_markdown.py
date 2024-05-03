import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes
)
from inline_markdown import (
    extract_markdown_images, 
    extract_markdown_links,
    )
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )
        
class TestInlineMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(text), expected)

class TestMarkdownSplitting(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode("This is an image ![img](url) end", text_type_text)
        expected = [
            TextNode("This is an image ", text_type_text),
            TextNode("img", text_type_image, "url"),
            TextNode(" end", text_type_text),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

class TestMarkdownSplitting(unittest.TestCase):
    def test_split_nodes_link(self):
        # Create a TextNode that includes a markdown link
        node = TextNode("Click here [Link](https://example.com) for more info", text_type_text)
        
        # What we expect after the split
        expected_output = [
            TextNode("Click here ", text_type_text),
            TextNode("Link", text_type_link, "https://example.com"),
            TextNode(" for more info", text_type_text)
]
        
        # Call the function with the node
        result = split_nodes_link([node])
        
        # Assert to check if the output matches the expected output
        self.assertEqual(result, expected_output)
class TestMarkdownToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        text = "This is **text**"
        expected_output = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_output)



if __name__ == "__main__":
    unittest.main()