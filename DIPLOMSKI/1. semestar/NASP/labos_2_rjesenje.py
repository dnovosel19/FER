class Node:
    """
    A class to represent a node of simple binary
    tree that contains integer values.

    ...

    Attributes
    ----------
    
    value : int
        value stored within a node
    left : Node
        left child
    right : Node
        right child
    parent : Node
        parent of the current node
    """
    def __init__(self,   value) -> None:
        self.value = value
        self.parent = self.right = self.left = None


def valjano_bin_stablo(korijen: Node) -> bool:
    """
    Decides if the binary (sub)tree rooted in
    korijen is a valid binary search tree

    Args:
        korijen (Node): root of the tree

    Returns:
        bool: True if the binary tree is search tree
              False,  otherwise
    """
    # TODO: recursive implementation that satisfies the requirements in docstring  
			 
    if korijen.left is None and korijen.right is None:
        return True
    l = True
    r = True
	 
    if korijen.left is not None:
        if korijen.left.value >= korijen.value:
            return False
        l = valjano_bin_stablo(korijen.left)
    if korijen.right is not None:
        if korijen.right.value < korijen.value:
            return False
        l = valjano_bin_stablo(korijen.right)
	
    if l and r:
        return True
    return False