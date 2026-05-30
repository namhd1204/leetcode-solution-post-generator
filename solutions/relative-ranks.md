# Index Mapping and Sorting for Rank Assignment

# Intuition
To assign ranks to the athletes, we need to sort their scores in descending order. However, because the final output must match the original order of the athletes, we cannot simply sort the scores in place. 

The core idea is to pair each score with its original index before sorting. This allows us to determine the rank of each athlete based on their sorted position while knowing exactly where to place their rank in the final output array.

# Approach
1. **Map Scores to Indices**: Create an array of objects where each object stores the athlete's score (`value`) and their original position (`index`).
2. **Sort Descending**: Sort this array of objects in descending order based on the score `value`. After sorting, the athlete at index `0` has the highest score (1st place), the athlete at index `1` has the second highest (2nd place), and so on.
3. **Assign Ranks**: Initialize a `result` array of the same length. Iterate through the sorted array and assign the ranks to their original indices:
   - Index `0` gets `"Gold Medal"`.
   - Index `1` gets `"Silver Medal"`.
   - Index `2` gets `"Bronze Medal"`.
   - Any index `i >= 3` gets the string representation of their rank, which is `(i + 1).toString()`.
4. **Return Result**: Return the populated `result` array.

```javascript
var findRelativeRanks = function (score) {
    const n = score.length;
    const indices = score.map((value, index) => {
        return {
            value, index
        }
    })
    
    indices.sort((a, b) => b.value - a.value);
    
    const result = new Array(n);
    
    for (let i = 0; i < n; i++) {
        const originalIndex = indices[i].index;
        if (i === 0) result[originalIndex] = "Gold Medal";
        else if (i === 1) result[originalIndex] = "Silver Medal";
        else if (i === 2) result[originalIndex] = "Bronze Medal";
        else result[originalIndex] = (i + 1).toString();
    }
    
    return result;
};
```

# Complexity
- Time complexity:
$$O(n \log n)$$  
Mapping the array takes $$O(n)$$ time. Sorting the array of size $$n$$ takes $$O(n \log n)$$ time. Assigning the ranks in the loop takes $$O(n)$$ time. Thus, the overall time complexity is dominated by the sorting step, which is $$O(n \log n)$$.

- Space complexity:
$$O(n)$$  
We use $$O(n)$$ extra space to store the mapped `indices` array of objects and the final `result` array of size $$n$$.