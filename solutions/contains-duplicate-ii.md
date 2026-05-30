# Single-Pass Hash Map with Index Tracking

# Intuition
To determine if there are two identical elements within a distance of `k`, we need to keep track of the indices where each number has previously appeared. As we traverse the array from left to right, the most relevant duplicate for any number is always its most recently seen occurrence. By storing the indices of each number in a hash map, we can instantly check if the distance between the current index and the previous index of the same number is less than or equal to `k`.

# Approach
1. Initialize an empty object `hashSet` to map each unique number to an array of its indices.
2. Iterate through the `nums` array using a loop, keeping track of the current index `i`.
3. For each element `num` at index `i`:
   - If `num` is not already a key in `hashSet`, initialize it with an empty array.
   - Push the current index `i` into the array corresponding to `num`.
   - Check if the number has appeared at least twice (i.e., the length of its index array is $\ge 2$).
   - If it has, compare the current index `i` with the previously recorded index (`hashSet[num][len - 2]`).
   - If the difference is less than or equal to `k`, return `true`.
4. If the loop completes without finding any such pair, return `false`.

```javascript
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {boolean}
 */
var containsNearbyDuplicate = function (nums, k) {
    let hashSet = {}
    let i = 0
    for(let num of nums) {
        if(!hashSet[num]) {
            hashSet[num] = []
        }
        hashSet[num].push(i)
        
        let len = hashSet[num].length
        if(len >= 2) {
            if(i - hashSet[num][len - 2] <= k) {
                return true
            }
        }
        i++
    }
    
    return false
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $$n$$ is the length of the `nums` array. We perform a single pass through the array, and hash map lookups as well as array insertions take $$O(1)$$ average time.

- Space complexity:
$$O(n)$$ because, in the worst-case scenario (where all elements in the array are unique), we store all $$n$$ elements and their indices in the hash map.