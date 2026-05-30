# Set-Based In-Place Deduplication

# Intuition
The core idea of this approach is to leverage the uniqueness property of a `Set` to automatically filter out duplicate elements. Since JavaScript `Set` preserves insertion order, iterating through the sorted array and adding elements to the set naturally keeps the unique elements in their original sorted order. Once we have the unique elements, we can overwrite the original array in-place.

# Approach
1. **Edge Case**: If the array contains only one element, it is already unique, so we immediately return `1`.
2. **Collect Unique Elements**: We iterate through the `nums` array and add each element to a `Set`. The set will automatically discard duplicates while maintaining the sorted order.
3. **Overwrite Original Array**: We obtain an iterator for the set's values. We then loop through the original `nums` array and replace each position with the next value from the iterator. If the iterator runs out of unique values, we fill the remaining positions with `null`.
4. **Return Count**: Finally, we return the size of the set, which represents the number of unique elements ($$k$$).

```javascript
/**
 * @param {number[]} nums
 * @return {number}
 */
var removeDuplicates = function (nums) {
    if (nums.length === 1) return 1;

    const set = new Set()
    for(let num of nums) {
        set.add(num)
    }
    const iterator = set.values();

    for(let i=0; i<nums.length;i++) {
        const curentSetValue = iterator.next()
        nums[i] = curentSetValue.done ? null : curentSetValue.value
    }
    // console.log({set})
    return set.size
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $$n$$ is the length of the `nums` array. We iterate through the array once to populate the set, and a second time to overwrite the elements in-place.

- Space complexity:
$$O(n)$$ auxiliary space to store the unique elements in the `Set`. In the worst-case scenario where all elements in the array are unique, the set will store $$n$$ elements.