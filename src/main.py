from textnode import TextNode, TextType

def main():

    tn = TextNode('This is some text', TextType.BOLD, 'https://url.url')
    print(tn)


main()