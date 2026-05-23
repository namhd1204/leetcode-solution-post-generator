# Hash Map and Set Lookup

# Intuition
To determine if the number of occurrences of each value in the array is unique, we need to perform two main steps:
1. Count how many times each number appears in the array.
2. Verify if any two numbers share the same frequency.

A hash map (or object in JavaScript) is perfect for counting frequencies, and a hash set is ideal for detecting duplicate frequencies in linear time.

# Approach
1. **Count Frequencies**: Iterate through the input array `arr` and populate a frequency map (`hashSet`) where the keys are the unique numbers from the array and the values are their respective counts.
2. **Check Uniqueness**: Create a new `Set` to keep track of the frequencies we have encountered.
3. Iterate through the counts stored in our frequency map:
   - If a count is already present in the `Set`, it means another number had the exact same frequency. In this case, return `false`.
   - Otherwise, add the count to the `Set`.
4. If the loop finishes without finding any duplicate frequencies, return `true`.

```javascript
/**
 * @param {number[]} arr
 * @return {boolean}
 */
var uniqueOccurrences = function(arr) {
    let hashSet = {}
    for(let num of arr) {
        hashSet[num] = (hashSet[num] || 0) + 1
    }
    // console.log(hashSet)
    const set = new Set()
    for(let num in hashSet) {
        // console.log(num, hashSet[num], set)
        if(set.has(hashSet[num])) {
            return false
        }
        set.add(hashSet[num])
    }
    return true
};
```

# Complexity
* Time complexity:
  $O(N)$ where $N$ is the length of the array `arr`. We traverse the array once to build the frequency map, and then traverse the unique keys of the map (which is at most $N$) to check for duplicate frequencies. Both operations run in linear time.

* Space complexity:
  $O(N)$ to store the frequency map and the set of unique frequencies. In the worst-case scenario where all elements in `arr` are unique, the map and the set will both store $N$ elements.