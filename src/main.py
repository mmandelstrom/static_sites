from textnode import Textnode, TextType

def main():

    tn = Textnode('This is some text', TextType.BOLD, 'https://url.url')
    print(tn)


main()