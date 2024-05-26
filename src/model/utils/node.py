from __future__ import annotations
from pydantic import BaseModel


class Node(BaseModel):
    hashValue: str
    left: Node | None = None
    right: Node | None = None
    
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
    
    def set_left(self, node: Node) -> None:
        self.left = node
        
    def set_right(self, node: Node) -> None:
        self.right = node
