# Clean Recursive BST Traversal

# Intuition
The problem asks us to find a node with a specific value in a Binary Search Tree (BST) and return the subtree rooted at that node. 

The defining property of a BST is that for any given node:
- All nodes in its left subtree have values strictly less than the node's value.
- All nodes in its right subtree have values strictly greater than the node's value.

This property allows us to make a binary decision at each step. Instead of searching the entire tree, we can compare the target value `val` with the current node's value and confidently discard one half of the tree, reducing the search space efficiently.

# Approach
We can solve this problem recursively:
1. **Base Case 1:** If the current `root` is `null`, the value does not exist in the tree. We return `null`.
2. **Base Case 2:** If the current `root.val` equals `val`, we have found the target node. We return the `root` node itself (which naturally includes its entire subtree).
3. **Recursive Step:**
   - If `root.val < val`, the target value must lie in the right subtree. We recursively call `searchBST` on `root.right`.
   - If `root.val > val`, the target value must lie in the left subtree. We recursively call `searchBST` on `root.left`.

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
 * @param {number} val
 * @return {TreeNode}
 */
var searchBST = function (root, val) {
    if (!root) return null
    if(root.val === val) return root
    if (root.val < val) {
        return searchBST(root.right, val)
    } else if(root.val > val) {
        return searchBST(root.left, val)
    }
};
```

# Complexity
- Time complexity:
$$O(H)$$, where $$H$$ is the height of the BST. In the average case of a balanced BST, the height is $$O(\log N)$$, where $$N$$ is the number of nodes. In the worst-case scenario (a skewed tree resembling a linked list), the height $$H$$ can be $$O(N)$$.

- Space complexity:
$$O(H)$$ due to the recursion stack. In the average case, the call stack will consume $$O(\log N)$$ space, and in the worst case, it will consume $$O(N)$$ space.