# Iterative Node Creation and Prepending

# Intuition
The core idea of this approach is to traverse the original linked list and construct a new reversed list on the fly. By creating new nodes and prepending them to the front of our growing list, we naturally reverse the order of the elements (similar to pushing elements onto a stack and then popping them).

# Approach
1. **Initialization**: We keep track of the current node `cur` and the original head `oldHead`. Both are initially set to the input `head`.
2. **Traversal**: We iterate through the list as long as `cur` and `cur.next` are not null.
3. **Node Creation & Prepending**: 
   - In each iteration, we create a new node (`newNode`) containing the value of the next node (`cur.next.val`).
   - We set this new node's `next` pointer to the current `head`, effectively prepending it.
   - We then update `head` to point to this `newNode`.
4. **Pointer Maintenance**: 
   - We advance `cur` to `cur.next`.
   - We set `oldHead.next = null` to disconnect the original head node from the rest of the list, ensuring that the tail of our newly reversed list correctly terminates with `null`.
5. **Return**: Once the traversal is complete, we return the updated `head`.

```javascript
/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var reverseList = function(head) {
    let cur = head, oldHead = head
    while(cur && cur.next) {
        let newNode = new ListNode(cur.next.val, head)
        head = newNode
        cur = cur.next
        oldHead.next = null
    }
    return head
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $$n$$ is the number of nodes in the linked list. We traverse the list exactly once.

- Space complexity:
$$O(n)$$ because we allocate a new `ListNode` for each node in the list (except the original head node), resulting in linear auxiliary space.