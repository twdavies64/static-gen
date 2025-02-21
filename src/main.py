import sys
from textnode import TextNode, TextType


def main():
    bob = TextNode("This is only a test", TextType.BOLD, "https://www.boot.dev")
    print(bob)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())