class DoctorNode:
    """Represents a doctor in the hospital reporting tree."""

    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class DoctorTree:
    """Manages the doctor reporting hierarchy using a binary tree."""

    def __init__(self):
        self.root = None

    def insert(self, parent_name, employee_name, side):
        """Insert a doctor under an existing parent.

        Returns True if insertion succeeds and False otherwise.
        """
        if self.root is None:
            return False

        if not isinstance(side, str):
            return False

        side = side.strip().lower()

        if side not in ("left", "right"):
            return False

        return self._insert_recursive(
            self.root, parent_name, employee_name, side
        )

    def _insert_recursive(self, node, parent_name, employee_name, side):
        """Recursively search for the parent and insert the new doctor."""
        if node is None:
            return False

        if node.name == parent_name:
            if side == "left":
                if node.left is not None:
                    return False
                node.left = DoctorNode(employee_name)
                return True

            if node.right is not None:
                return False

            node.right = DoctorNode(employee_name)
            return True

        if self._insert_recursive(
            node.left, parent_name, employee_name, side
        ):
            return True

        return self._insert_recursive(
            node.right, parent_name, employee_name, side
        )

    def preorder(self, node):
        """Return names in Root-Left-Right order."""
        if node is None:
            return []

        return (
            [node.name]
            + self.preorder(node.left)
            + self.preorder(node.right)
        )

    def inorder(self, node):
        """Return names in Left-Root-Right order."""
        if node is None:
            return []

        return (
            self.inorder(node.left)
            + [node.name]
            + self.inorder(node.right)
        )

    def postorder(self, node):
        """Return names in Left-Right-Root order."""
        if node is None:
            return []

        return (
            self.postorder(node.left)
            + self.postorder(node.right)
            + [node.name]
        )


# Test the DoctorNode and DoctorTree classes.
def test_doctor_tree():
    # Test an empty tree.
    empty_tree = DoctorTree()

    assert empty_tree.root is None
    assert empty_tree.preorder(None) == []
    assert empty_tree.inorder(None) == []
    assert empty_tree.postorder(None) == []
    assert empty_tree.insert(
        "Dr. Croft", "Dr. Goldsmith", "right"
    ) is False

    # Build the example tree from the assignment.
    tree = DoctorTree()
    tree.root = DoctorNode("Dr. Croft")

    assert tree.insert(
        "Dr. Croft", "Dr. Goldsmith", "right"
    ) is True
    assert tree.insert(
        "Dr. Croft", "Dr. Phan", "left"
    ) is True
    assert tree.insert(
        "Dr. Phan", "Dr. Carson", "right"
    ) is True
    assert tree.insert(
        "Dr. Phan", "Dr. Morgan", "left"
    ) is True

    # Verify all three required traversal orders.
    expected_preorder = [
        "Dr. Croft",
        "Dr. Phan",
        "Dr. Morgan",
        "Dr. Carson",
        "Dr. Goldsmith",
    ]

    expected_inorder = [
        "Dr. Morgan",
        "Dr. Phan",
        "Dr. Carson",
        "Dr. Croft",
        "Dr. Goldsmith",
    ]

    expected_postorder = [
        "Dr. Morgan",
        "Dr. Carson",
        "Dr. Phan",
        "Dr. Goldsmith",
        "Dr. Croft",
    ]

    assert tree.preorder(tree.root) == expected_preorder
    assert tree.inorder(tree.root) == expected_inorder
    assert tree.postorder(tree.root) == expected_postorder

    # Test an existing parent that does not have the requested name.
    assert tree.insert(
        "Dr. Missing", "Dr. New", "left"
    ) is False

    # Test an invalid insertion side.
    assert tree.insert(
        "Dr. Croft", "Dr. Invalid", "middle"
    ) is False

    # Test that an occupied child is not overwritten.
    assert tree.insert(
        "Dr. Croft", "Dr. Replacement", "left"
    ) is False

    # Confirm failed insertions did not change the tree.
    assert tree.preorder(tree.root) == expected_preorder

    # Test a tree containing only one doctor.
    single_tree = DoctorTree()
    single_tree.root = DoctorNode("Dr. Solo")

    assert single_tree.preorder(single_tree.root) == ["Dr. Solo"]
    assert single_tree.inorder(single_tree.root) == ["Dr. Solo"]
    assert single_tree.postorder(single_tree.root) == ["Dr. Solo"]

    print("Preorder:", tree.preorder(tree.root))
    print("Inorder:", tree.inorder(tree.root))
    print("Postorder:", tree.postorder(tree.root))
    print("All doctor tree tests passed!")


if __name__ == "__main__":
    test_doctor_tree()