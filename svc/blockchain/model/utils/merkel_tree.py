import hashlib
from .node import Node


def hash(hash_1: str, hash_2: str) -> str:
    sum_hash = hash_1 + hash_2
    return hashlib.sha256(sum_hash.encode()).hexdigest()


def build_merkel_tree(hashes: list[str]) -> Node | None:
    if len(hashes) == 1:
        return Node(
            hashValue=hashes[0],
            left=None, 
            right=None
        )
    mid_index = len(hashes) // 2
    left_node = build_merkel_tree(hashes=hashes[:mid_index])
    right_node = build_merkel_tree(hashes=hashes[mid_index:])
    return Node(
        hashValue=hash(left_node.hashValue, right_node.hashValue),
        left=left_node,
        right=right_node
    )
    
    
def calculate_hash(hashes: list[str]) -> str:
    merkel_tree_root = build_merkel_tree(hashes=hashes)
    return merkel_tree_root.hashValue
