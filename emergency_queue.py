class Patient:
    """Represents a patient waiting for emergency care."""

    def __init__(self, name, urgency):
        if not isinstance(name, str):
            raise TypeError("Patient name must be a string.")

        if (
            not isinstance(urgency, int)
            or isinstance(urgency, bool)
            or not 1 <= urgency <= 10
        ):
            raise ValueError("Urgency must be an integer from 1 to 10.")

        self.name = name
        self.urgency = urgency


class MinHeap:
    """Manages patients using a min-heap priority queue."""

    def __init__(self):
        self.data = []

    def heapify_up(self, index):
        """Move a patient upward until the heap property is restored."""
        if index < 0 or index >= len(self.data):
            return

        while index > 0:
            parent_index = (index - 1) // 2

            if (
                self.data[index].urgency
                < self.data[parent_index].urgency
            ):
                self.data[index], self.data[parent_index] = (
                    self.data[parent_index],
                    self.data[index],
                )
                index = parent_index
            else:
                break

    def heapify_down(self, index):
        """Move a patient downward until the heap property is restored."""
        if index < 0 or index >= len(self.data):
            return

        left_index = 2 * index + 1
        right_index = 2 * index + 2
        smallest_index = index

        if (
            left_index < len(self.data)
            and self.data[left_index].urgency
            < self.data[smallest_index].urgency
        ):
            smallest_index = left_index

        if (
            right_index < len(self.data)
            and self.data[right_index].urgency
            < self.data[smallest_index].urgency
        ):
            smallest_index = right_index

        if smallest_index != index:
            self.data[index], self.data[smallest_index] = (
                self.data[smallest_index],
                self.data[index],
            )
            self.heapify_down(smallest_index)

    def insert(self, patient):
        """Add a patient and restore the heap property."""
        if not isinstance(patient, Patient):
            raise TypeError("insert() requires a Patient object.")

        self.data.append(patient)
        self.heapify_up(len(self.data) - 1)

    def peek(self):
        """Return the most urgent patient without removing them."""
        if not self.data:
            return None

        return self.data[0]

    def remove_min(self):
        """Remove and return the patient with the lowest urgency score."""
        if not self.data:
            return None

        min_patient = self.data[0]
        last_patient = self.data.pop()

        if self.data:
            self.data[0] = last_patient
            self.heapify_down(0)

        return min_patient

    def print_heap(self):
        """Print patients in the heap's current array order."""
        print("Current Queue:")

        for patient in self.data:
            print(f"- {patient.name} ({patient.urgency})")


# Test the MinHeap class, including edge cases.
def test_min_heap():
    # Test an empty queue.
    empty_heap = MinHeap()

    assert empty_heap.data == []
    assert empty_heap.peek() is None
    assert empty_heap.remove_min() is None

    # Invalid indices should not cause errors.
    empty_heap.heapify_up(0)
    empty_heap.heapify_down(0)

    # Test the example from the assignment.
    heap = MinHeap()
    heap.insert(Patient("Jordan", 3))
    heap.insert(Patient("Taylor", 1))
    heap.insert(Patient("Avery", 5))

    assert heap.peek().name == "Taylor"
    assert heap.peek().urgency == 1
    assert len(heap.data) == 3  # peek() must not remove a patient.

    heap.print_heap()

    served = heap.remove_min()
    assert served.name == "Taylor"
    assert served.urgency == 1

    assert heap.peek().name == "Jordan"
    assert len(heap.data) == 2

    heap.print_heap()

    # Test removing the only patient in a queue.
    single_heap = MinHeap()
    single_heap.insert(Patient("Morgan", 4))

    assert single_heap.remove_min().name == "Morgan"
    assert single_heap.data == []
    assert single_heap.peek() is None
    assert single_heap.remove_min() is None

    # Test that every parent has urgency <= its children's urgency.
    def check_heap_property(test_heap):
        for child_index in range(1, len(test_heap.data)):
            parent_index = (child_index - 1) // 2

            assert (
                test_heap.data[parent_index].urgency
                <= test_heap.data[child_index].urgency
            ), "Min-heap property violated."

    # Test heapify_down when the right child is more urgent
    # than the left child.
    priority_heap = MinHeap()

    for name, urgency in [
        ("P1", 1),
        ("P2", 4),
        ("P3", 2),
        ("P4", 8),
        ("P5", 6),
        ("P6", 3),
        ("P7", 5),
    ]:
        priority_heap.insert(Patient(name, urgency))
        check_heap_property(priority_heap)

    # All patients must be removed in ascending urgency order.
    removed_urgencies = []

    while priority_heap.data:
        removed_urgencies.append(
            priority_heap.remove_min().urgency
        )
        check_heap_property(priority_heap)

    assert removed_urgencies == [1, 2, 3, 4, 5, 6, 8]

    # Test duplicate urgency scores.
    duplicate_heap = MinHeap()
    duplicate_heap.insert(Patient("Alex", 2))
    duplicate_heap.insert(Patient("Casey", 2))
    duplicate_heap.insert(Patient("Riley", 1))

    assert duplicate_heap.remove_min().urgency == 1
    assert duplicate_heap.remove_min().urgency == 2
    assert duplicate_heap.remove_min().urgency == 2

    # Test invalid urgency values.
    for invalid_urgency in [0, 11, 1.5, "1", True]:
        try:
            Patient("Invalid", invalid_urgency)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"Invalid urgency was accepted: {invalid_urgency}"
            )

    # Test that insert() rejects objects that are not Patients.
    try:
        heap.insert("Not a patient")
    except TypeError:
        pass
    else:
        raise AssertionError("insert() accepted a non-Patient object.")

    print("All emergency queue tests passed!")


if __name__ == "__main__":
    test_min_heap()
