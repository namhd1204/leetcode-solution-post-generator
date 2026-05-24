# DFS Leaf Sequence Extraction and Comparison

# Intuition
To determine if two binary trees are leaf-similar, we need to extract their leaf nodes in a strict left-to-right order and compare the resulting sequences. A Depth-First Search (DFS) traversal naturally visits nodes from left to right if we traverse the left subtree before the right subtree. By collecting the values of all leaf nodes (nodes with no left or right children) during this traversal, we can easily compare the two sequences.

# Approach
1. **Leaf Extraction (`getLeafs`):** We define a recursive helper function that performs a DFS traversal on a given tree node.
   - If the current node is a leaf (both `left` and `right` children are `null`), we return an array containing only the node's value.
   - If the node has children, we recursively retrieve the leaf sequences of the left and right subtrees and merge them.
2. **Sequence Comparison:** 
   - We extract the leaf sequences for both `root1` and `root2`.
   - If the lengths of the two sequences differ, they cannot be leaf-similar, so we return `false`.
   - Otherwise, we iterate through both arrays and compare the elements at each index. If any mismatch is found, we return `false`.
   - If all elements match, we return `true`.

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
 * @param {TreeNode} root1
 * @param {TreeNode} root2
 * @return {boolean}
 */
var leafSimilar = function(root1, root2) {
    
    const leafs1 = getLeafs(root1);
    const leafs2 = getLeafs(root2);
    
    if(leafs1.length !== leafs2.length) return false

    for(let i=0; i<leafs1.length; i++) {
        if(leafs1[i] !== leafs2[i]) {
            return false
        }
    }

    return true;
};

var getLeafs = function(node) {
    let leafs = []

    if(!node.left && !node.right) {
        leafs.push(node.val)
        return leafs
    }

    if(node.left) {
        let leftLeafs = getLeafs(node.left)
        leafs.push(...leftLeafs)
    }

    if(node.right) {
        let rightLeafs = getLeafs(node.right)
        leafs.push(...rightLeafs)
    }

    return leafs
}
```

# Complexity
- Time complexity:
$$O(N_1 + N_2)$$ where $$N_1$$ and $$N_2$$ are the number of nodes in the first and second trees, respectively. We visit every node in both trees exactly once during the DFS traversal.

- Space complexity:
$$O(H_1 + H_2 + L_1 + L_2)$$ where $$H_1, H_2$$ are the heights of the trees (representing the recursion stack depth) and $$L_1, L_2$$ are the number of leaf nodes stored in the arrays. In the worst-case scenario of a skewed tree, the space complexity is $$O(N_1 + N_2)$$.