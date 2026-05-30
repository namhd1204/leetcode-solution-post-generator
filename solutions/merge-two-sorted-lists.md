# Iterative In-Place Pointer Swapping

# Intuition
Since both input linked lists are already sorted, we can merge them in-place without allocating any new nodes. The core idea is to designate one list (the one starting with the smaller value) as our main chain (`tail`) and the other as a temporary chain (`temp`). As we traverse, whenever the next node in our main chain has a larger value than the head of the temporary chain, we splice the temporary chain into our main chain and swap our pointers to continue the process.

# Approach
1. **Handle Base Cases:** If either `list1` or `list2` is empty, return the other list immediately.
2. **Initialize Pointers:** Compare the starting values of both lists. Set `head` and `tail` to the list with the smaller starting value, and set `temp` to the other list.
3. **Weave the Lists:** Traverse the main list using a `while (tail.next)` loop:
   - If the next node in the main list (`tail.next.val`) is greater than or equal to the current node of the other list (`temp.val`), we need to insert `temp` here.
   - To do this in-place, we temporarily store `tail.next`, point `tail.next` to `temp`, advance `tail` to this new node, and set `temp` to the stored next node. This effectively swaps the roles of the remaining lists.
   - If `tail.next.val` is smaller than `temp.val`, we simply advance `tail` to `tail.next`.
4. **Attach Remaining Nodes:** Once the loop ends (meaning we reached the end of the main chain), append any remaining nodes in `temp` to `tail.next`.
5. **Return Result:** Return the original `head` pointer.

```javascript
/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} list1
 * @param {ListNode} list2
 * @return {ListNode}
 */
var mergeTwoLists = function(list1, list2) {
    if(!list1) return list2
    if(!list2) return list1
    let head = tail = list1
    let temp = list2
    if(list1.val >= list2.val) {
        head = tail = list2
        temp = list1
    }
    while(tail.next) {
        // console.log({head, tail, temp})
        if(tail.next.val >= temp.val) {
            let currentTailNext = tail.next
            tail.next = temp
            tail = tail.next
            temp = currentTailNext
        } else {
            tail = tail.next
        }
    }

    tail.next = temp
    
    // console.log({head, tail, temp})
    
    return head
};
```

# Complexity
- Time complexity:
$$O(n + m)$$ where $$n$$ and $$m$$ are the lengths of `list1` and `list2` respectively. We traverse each node in both lists at most once.

- Space complexity:
$$O(1)$$ because the merge is performed entirely in-place by rearranging the existing node pointers without using any extra memory.