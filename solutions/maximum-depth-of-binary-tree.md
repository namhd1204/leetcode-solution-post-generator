# Simple Recursive Depth-First Search

# Intuition
The maximum depth of a binary tree is the length of the longest path from the root node down to the farthest leaf node. This problem can be naturally broken down into smaller subproblems using recursion: the maximum depth of any binary tree is $1$ (for the current root node) plus the maximum of the depths of its left and right subtrees. 

# Approach
We can solve this using a Depth-First Search (DFS) post-order traversal strategy:
1. **Base Case:** If the current node (`root`) is `null`, the tree is empty, so its depth is `0`.
2. **Recursive Step:** 
   - Recursively calculate the maximum depth of the left subtree: `maxDepth(root.left)`.
   - Recursively calculate the maximum depth of the right subtree: `maxDepth(root.right)`.
3. **Combine:** The depth of the current node is the maximum of the depths of its left and right subtrees plus `1` (to count the current node itself).

```javascript
/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {number}
 */
var maxDepth = function(root) {

    if(!root) return 0

    // pre-order: node -> left -> right
    let d = 0

    d += Math.max(maxDepth(root.left), maxDepth(root.right)) + 1

    return d;
};
```

# Complexity
- Time complexity:
$$O(N)$$ where $$N$$ is the total number of nodes in the binary tree. We must visit each node exactly once to determine the overall maximum depth.

- Space complexity:
$$O(H)$$ where $$H$$ is the height of the tree. This space is consumed by the recursive call stack. In the worst-case scenario (a completely skewed tree), the height $$H$$ is equal to $$N$$, resulting in $$O(N)$$ space. In the best-case scenario (a completely balanced tree), the height $$H$$ is $$O(\log N)$$.