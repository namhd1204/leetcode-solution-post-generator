# Binary Search with Boundary Checks

# Intuition
Since the input array is already sorted and we need to achieve an $O(\log n)$ runtime complexity, **Binary Search** is the ideal approach. 

By handling the extreme edge cases first (where the target is smaller than the first element or larger than the last element), we can safely narrow down our search space. During the binary search, if the target is not found directly, the insertion index will naturally fall between two adjacent elements, which we can resolve when our search window shrinks to a size of 2.

# Approach
1. **Boundary Checks**: 
   - If the `target` is strictly greater than the last element in `nums`, it must be inserted at the very end, so we return `nums.length`.
   - If the `target` is strictly smaller than the first element in `nums`, it must be inserted at the very beginning, so we return `0`.
2. **Binary Search Initialization**: Set two pointers, `left = 0` and `right = nums.length - 1`.
3. **Search Loop**:
   - Calculate the middle index `mid` using `Math.floor(left + (right - left) / 2)` to avoid potential integer overflow.
   - If `nums[mid]` matches the `target`, return `mid` immediately.
   - If the pointers are adjacent (`right - left === 1`), it means the target is not in the array and belongs between `left` and `right`. Thus, the correct insertion index is `right`.
   - If `nums[mid] > target`, narrow the search space to the left half by setting `right = mid`.
   - Otherwise, narrow the search space to the right half by setting `left = mid`.

```javascript
/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number}
 */
var searchInsert = function(nums, target) {
    if(target > nums[nums.length - 1]) return nums.length
    if(target < nums[0]) return 0
    let left = 0, right = nums.length - 1
    let mid
    while(left <= right) {
        mid = Math.floor(left + (right - left) / 2);
        // console.log({left, right, mid, val: nums[mid], target})
        if(nums[mid] === target) return mid

        if(right - left === 1) return right
        if(nums[mid] > target) {
            right = mid
        } else {
            left = mid
        }

    }
    return mid
};
```

# Complexity
- Time complexity:
$$O(\log n)$$
The search space is halved in each iteration of the `while` loop, resulting in logarithmic time complexity.

- Space complexity:
$$O(1)$$
The algorithm only uses a constant amount of extra space for pointers (`left`, `right`, `mid`), making it highly memory efficient.