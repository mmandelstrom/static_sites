class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        to_html = ""
        for prop in self.props:
            to_html += f' {prop}="{self.props[prop]}"'
            
        return to_html
    
    def __repr__(self):
        return f"HTMLNode(Tag = {self.tag}, Value = {self.value}, Children = {self.children}, Props = {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value,  None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag submitted")
        if self.children is None:
            raise ValueError("Parentnode must have children")
        res = f"<{self.tag}>"

        for child in self.children:
            res += child.to_html()

        res += f"</{self.tag}>"
        return res