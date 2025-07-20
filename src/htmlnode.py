class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.__props_string = self.__props_dict_to_string__(props)

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return self.__props_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __props_dict_to_string__(self, props_dict):
        props = []

        if props_dict == None:
            return ""

        for key in props_dict:
            props.append(f'{key}="{props_dict[key]}"')

        return " ".join(props)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: missing value")

        if self.tag == None:
            return self.value

        opening_tag = f"<{self.tag}>"
        closing_tag = f"</{self.tag}>"

        if self.props != None:
            i = opening_tag.index(">")
            opening_tag = opening_tag[:i] + f" {self.props_to_html()}" + opening_tag[i:]

        return f"{opening_tag}{self.value}{closing_tag}"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("invalid HTML: missing tag")

        if self.children == None:
            raise ValueError("invalid HTML: missing children")

        opening_tag = f"<{self.tag}>"
        closing_tag = f"</{self.tag}>"

        if self.props != None:
            i = opening_tag.index(">")
            opening_tag = opening_tag[:i] + f" {self.props_to_html()}" + opening_tag[i:]

        html = opening_tag

        for child in self.children:
            html += child.to_html()

        html += closing_tag

        return html

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
