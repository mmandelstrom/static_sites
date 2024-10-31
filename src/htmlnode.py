class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

#To be overwritten by child classes
    def to_html(self):
        raise NotImplementedError

#Loop through properties and build a string if they are present   
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
            
        return props_html
    
    def __repr__(self):
        return f"HTMLNode(Tag = {self.tag}, Value = {self.value}, Children = {self.children}, Props = {self.props})"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value,  None, props)

    def __repr__(self):
        return f"LeafNode(Tag = {self.tag}, Value = {self.value}, Props = {self.props})"

#Return a string with leafnode value, tag and property transformed to html
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

#Return a string with leafnode value, tag and property transformed to html, if the node has child nodes it recursively calls the function until all nodes have been transformed
    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag submitted")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parentnode must have children")
        
        res = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            res += child.to_html()

        res += f"</{self.tag}>"
        return res
