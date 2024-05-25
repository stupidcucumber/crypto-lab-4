import hashlib
from .node import Node
from .hashable import Hashable


def hash(hash_1: str, hash_2: str) -> str:
    sum_hash = hash_1 + hash_2
    return hashlib.sha256(sum_hash.encode()).hexdigest()


def build_merkel_tree(objects: list[Hashable]) -> Node | None:
    if len(objects) == 1:
        return Node(
            hashValue=objects[0],
            left=None, 
            right=None
        )
    mid_index = len(objects) // 2
    left_node = build_merkel_tree(objects=objects[:mid_index])
    right_node = build_merkel_tree(objects=objects[mid_index:])
    return Node(
        value=objects[0],
        hashValue=hash(left_node.hashValue, right_node.hashValue),
        left=left_node,
        right=right_node
    )
    
    
def calculate_hash(objects: list[Hashable]) -> str:
    merkel_tree_root = build_merkel_tree(objects=objects)
    return merkel_tree_root.hashValue
