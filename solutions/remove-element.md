# Two-Pointer Swap from End

# Intuition
The problem requires us to remove all occurrences of a specific value `val` from an array in-place and return the new length. Since the order of elements does not matter, we can optimize the process by using a two-pointer approach. Instead of shifting all elements forward every time we encounter `val`, we can swap or overwrite the target elements at the beginning of the array with valid elements from the end of the array. This minimizes the number of write operations.

# Approach
We use two pointers, `i` starting at the beginning of the array (`0`) and `j` starting at the end of the array (`nums.length - 1`):

1. We iterate while `i <= j`.
2. If the element at the right pointer `nums[j]` is equal to `val`, it is already in the portion of the array to be discarded. We can safely decrement `j` (and optionally set the discarded position to `null`).
3. If `nums[j]` is not equal to `val`, we check the left pointer `nums[i]`:
   - If `nums[i]` is equal to `val`, we overwrite `nums[i]` with the valid element `nums[j]`, then increment `i` and decrement `j`.
   - If `nums[i]` is not equal to `val`, it is already a valid element in the correct position, so we simply increment `i`.
4. When the pointers cross (`i > j`), all valid elements are grouped at the beginning of the array up to index `i - 1`.
5. We return `i` as the count of elements not equal to `val`.

```javascript
/**
 * @param {number[]} nums
 * @param {number} val
 * @return {number}
 */
var removeElement = function(nums, val) {
    let i = 0, j = nums.length - 1
    while(i <= j) {
        if(nums[j] === val) {
            nums[j--] = null
        } else {
            if(nums[i] === val) {
                nums[i++] = nums[j]
                nums[j--] = null
            } else {
                i++
            }
        }
    }
    // console.log({nums, i, j})
    return i
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $$n$$ is the length of the array. In the worst case, both pointers meet in the middle, meaning we traverse each element of the array at most once.

- Space complexity:
$$O(1)$$ because the algorithm operates entirely in-place, modifying the input array without allocating any extra space.