class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented("Not implemented yet")
    
    def props_to_html(self):
        if self.props is None:
            raise Exception("HTMLNode does not contains any props")
        props = ""
        for key, value in self.props.items(): #Loop through each kvp in dict and add to the empty string
            props += f' {key}="{value}"'
        return props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other): #Method to compare htmlnodes objects for tests
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
    
    

class LeafNode(HTMLNode): #Leaf nodes requires a tag and takes no child nodes
    def __init__(self, tag, value, props = None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            return f"{self.value}"
        
        if self.props is not None: #If node has props add to opening tag 
            props = self.props_to_html()
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"
        else: #If node does not have props, add tags and return
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):#Method to convert to HTML
        if self.tag is None:
            raise ValueError("Parentnode must have a tag")
        if not self.children: 
            raise ValueError("ParentNode must have children")
        
        res = ""
        for child in self.children:
            if child is not None:
                res += child.to_html()

        if self.props is not None: #If node has props add to opening tag 
            props = self.props_to_html()
            return f"<{self.tag}{props}>{res}</{self.tag}>"
        return f"<{self.tag}>{res}</{self.tag}>"

