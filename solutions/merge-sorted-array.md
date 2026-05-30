# In-Place Insertion and Shifting from Left to Right

# Intuition
The core idea is to merge `nums2` into `nums1` by traversing `nums1` from left to right. Since `nums1` has pre-allocated space at the end (filled with `0`s), we can insert elements from `nums2` at their correct sorted positions. To make room for these insertions, we shift the existing elements of `nums1` to the right. We also maintain a dynamic boundary `newM` to distinguish between the actual elements of `nums1` and the trailing placeholder zeros.

# Approach
1. Initialize a pointer `j` to track our position in `nums2` and a variable `newM` (initially set to `m`) to track the logical end of the valid elements in `nums1`.
2. Iterate through `nums1` using a pointer `i`.
3. If we encounter a placeholder `0` at or beyond the logical boundary (`i >= newM`), we can safely overwrite it with `nums2[j]` without shifting, then increment `j`.
4. If the current element `nums1[i]` is greater than or equal to `nums2[j]`, we insert `nums2[j]` at index `i`. 
5. The insertion is handled by a helper function `insert`, which shifts all elements from index `i` to the end of the array one position to the right, and then places the new value at index `i`.
6. After an insertion, we increment `newM` (since the logical size of `nums1` has increased) and advance our pointers accordingly.

```javascript
/**
 * @param {number[]} nums1
 * @param {number} m
 * @param {number[]} nums2
 * @param {number} n
 * @return {void} Do not return anything, modify nums1 in-place instead.
 */
var merge = function(nums1, m, nums2, n) {
    let j = 0
    let newM = m
    for(let i = 0; i<nums1.length && j<n; i++) {

        if(nums1[i] === 0 && i >= newM) {
            nums1[i] = nums2[j]
            j++
            continue
        }
        
        if(nums1[i] === nums2[j]) {
            insert(nums1, i, nums2[j])
            i++
            j++
            newM++
        } else if(nums1[i] > nums2[j]) {
            insert(nums1, i, nums2[j])
            j++
            newM++
        }
    }
};

var insert = function(array, index, value) {
    for(let i = array.length-1; i >= index; i--) {
        array[i] = i === index ? value : array[i-1]
    }
}
```

# Complexity
- Time complexity:
$$O((m + n)^2)$$  
In the worst case (for example, when all elements of `nums2` are smaller than the elements of `nums1`), we have to insert elements at the beginning of `nums1`. Each insertion triggers the `insert` helper function, which shifts up to $$m + n$$ elements. Doing this for $$n$$ elements results in a quadratic time complexity.

- Space complexity:
$$O(1)$$  
The algorithm modifies `nums1` in-place and only uses a few pointers and counter variables, requiring constant extra space.