import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="p",
            value="Hello world",
            children=None,
            props={"id": "1", "style": "color:red;"},
        )
        props_html = node.props_to_html()

        self.assertEqual('id="1" style="color:red;"', props_html)

    def test_html_node_repr(self):
        node = HTMLNode(
            "div",
            "some text",
            ["h3", "p"],
            {
                "class": "div",
            },
        )

        self.assertEqual(
            "HTMLNode(div, some text, ['h3', 'p'], {'class': 'div'})",
            repr(node),
        )

    def test_leaf_node_to_html_without_value(self):
        self.assertRaises(
            ValueError,
            lambda: LeafNode(None, None, None).to_html(),
        )

    def test_leaf_node_repr(self):
        node = LeafNode(
            "div",
            "some text",
            {
                "class": "div",
            },
        )

        self.assertEqual(
            "LeafNode(div, some text, {'class': 'div'})",
            repr(node),
        )

    def test_leaf_node_to_html(self):
        html = LeafNode(
            tag="p",
            value="Hello world",
        ).to_html()

        self.assertEqual("<p>Hello world</p>", html)

    def test_leaf_node_to_html_with_props(self):
        html = LeafNode(
            tag="a",
            value="Hello world",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        ).to_html()

        self.assertEqual(
            '<a href="https://www.google.com" target="_blank">Hello world</a>', html
        )

    def test_parent_node_to_html_without_tag(self):
        self.assertRaises(
            ValueError,
            lambda: ParentNode(None, [LeafNode("div", "child")], None).to_html(),
        )

    def test_parent_node_to_html_without_children(self):
        self.assertRaises(ValueError, lambda: ParentNode("div", None, None).to_html())

    def test_parent_node_repr(self):
        node = ParentNode(
            "div",
            ["h3", "p"],
            {
                "class": "div",
            },
        )

        self.assertEqual(
            "ParentNode(div, ['h3', 'p'], {'class': 'div'})",
            repr(node),
        )

    def test_parent_node_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_node_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_to_html_with_grandchildren_and_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"class": "grandchild"})
        child_node = ParentNode("span", [grandchild_node], {"class": "child"})
        parent_node = ParentNode("div", [child_node], {"class": "parent"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="parent"><span class="child"><b class="grandchild">grandchild</b></span></div>',
        )


if __name__ == "__main__":
    unittest.main()
