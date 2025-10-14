# Define a binary tree node
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Recursive tree traversals
def inorder(node):
    """Left → Root → Right"""
    if node:
        inorder(node.left)
        print(node.value, end=" ")
        inorder(node.right)


def preorder(node):
    """Root → Left → Right"""
    if node:
        print(node.value, end=" ")
        preorder(node.left)
        preorder(node.right)


def postorder(node):
    """Left → Right → Root"""
    if node:
        postorder(node.left)
        postorder(node.right)
        print(node.value, end=" ")


# Example usage
if __name__ == "__main__":
    # Construct a binary tree
    #
    #        A
    #       / \
    #      B   C
    #     / \   \
    #    D   E   F
    #

    # root = Node("дівинка чи хлопчик?")
    # root.left = Node("носить сукню?")
    # root.right = Node("грає у футбол?")
    # root.left.left = Node("сукня рожева?")
    # root.left.right = Node("носить спідницю?")
    # root.right.left = Node("грає машинками?")
    # root.right.right = Node("грає роботами?")

    # root = Node(8)
    # root.left = Node(4)
    # root.right = Node(12)
    # root.left.left = Node(2)
    # root.left.right = Node(6)
    # root.right.left = Node(10)
    # root.right.right = Node(14)

    # root = Node(15)
    # root.left = Node(14)
    # root.right = Node(13)
    # root.left.left = Node(12)
    # root.left.right = Node(6)
    # root.right.left = Node(10)
    # root.right.right = Node(14)
    #
    # root.left.left.left = Node(1)
    # root.left.left.right = Node(3)
    #
    # root.left.right.left = Node(5)
    # root.left.right.right = Node(7)
    #
    # root.right.left.left = Node(9)
    # root.right.left.right = Node(11)
    #
    # root.right.right.left = Node(13)
    # root.right.right.right = Node(15)
    #
    #
    #
    # print("Inorder traversal:")
    # inorder(root)
    # print("\nPreorder traversal:")
    # preorder(root)
    # print("\nPostorder traversal:")
    # postorder(root)

# for i in range(16):
# print(1)
# # print(16)
# print(bin(16//2))
# print(bin(16//4))
# print(bin(16//2+16//4))
# print(bin(16//8))
# b0 = 16
# # b1 = 16
# l_ = list(range(16))
# j0 = 16
# a = 0
# b = 15
# j = j0
# for i in range(1, 15):
#     l_[0] = a
#     l_[-1] = b
#
#     # j = j // 2
#     l_[j] = i
    # root.right = Node(12)
    # root.left.left = Node(2)
    # root.left.right = Node(6)
    # root.right.left = Node(10)
    # root.right.right = Node(14)

    # root = Node(15)
    # root.left = Node(14)
    # root.right = Node(13)
    # root.left.left = Node(12)
    # root.left.right = Node(6)
    # root.right.left = Node(10)
    # root.right.right = Node(14)
    #
    # root.left.left.left = Node(1)
    # root.left.left.right = Node(3)
    #
    # root.left.right.left = Node(5)
    # root.left.right.right = Node(7)
    #
    # root.right.left.left = Node(9)
    # root.right.left.right = Node(11)
    #
    # root.right.right.left = Node(13)
    # root.right.right.right = Node(15)
    #
    #
    #
    # print("Inorder traversal:")
    # inorder(root)
    # print("\nPreorder traversal:")
    # preorder(root)
    # print("\nPostorder traversal:")
    # postorder(root)

# for i in range(16):
# print(1)
# # print(16)
# print(bin(16//2))
# print(bin(16//4))
# print(bin(16//2+16//4))
# print(bin(16//8))
# b0 = 16
# # b1 = 16
# l_ = list(range(16))
# j0 = 16
# a = 0
# b = 15
# j = j0
# for i in range(1, 15):
#     l_[0] = a
#     l_[-1] = b
#
#     # j = j // 2
#     # if j < j0/2:
#     #     j0 = j
#     #     j += j0//2
#     print(j)
#
    # print(8<<1)
    print(8)
    print(8>>1)
    #
    print(8|(8>>1))
    print(8>>2)
    print((8>>2)|8)

