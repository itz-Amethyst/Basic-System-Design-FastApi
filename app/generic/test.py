from typing import TypeVar, Generic, List, Union

# Define a generic type variable T
#? This one resisted to only str and int generics
# T = TypeVar('T', int, str)
#! This can be anything
T = TypeVar('T')

# Define a generic class Box
class Box(Generic[T]):
    def __init__(self, item: T):
        self.item = item

    def get_item(self) -> T:
        return self.item

    def set_item(self, new_item: T) -> None:
        self.item = new_item

# Generic function example
def get_first_item(items: List[T]) -> T:
    return items[0]

def main() -> None:
    # For integers
    int_box = Box(123)
    int_item = int_box.get_item()
    print(f"Item in int_box: {int_item}")  # Outputs: Item in int_box: 123

    # For strings
    str_box = Box("Hello, Generics!")
    str_item = str_box.get_item()
    print(f"Item in str_box: {str_item}")  # Outputs: Item in str_box: Hello, Generics!

    # For lists
    list_box = Box([1, 2, 3])  # Error: List[int] not allowed
    # list_item = list_box.get_item()
    # print(f"Item in list_box: {list_item}")

    # Generic function
    first_item = get_first_item([1, 2, 3])
    print(f"First item in the list: {first_item}")



if __name__ == "__main__":
    main()