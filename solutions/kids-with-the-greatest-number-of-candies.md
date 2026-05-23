# Simple One-Pass Maximum Comparison

# Intuition
To determine if a kid can have the greatest number of candies after receiving the `extraCandies`, we first need to know the current maximum number of candies any kid has. Once we establish this benchmark, we can simply check if each kid's candy count, when increased by `extraCandies`, is at least equal to this maximum.

# Approach
1. **Find the Maximum:** Use `Math.max(...candies)` to find the maximum number of candies currently held by any kid.
2. **Map and Compare:** Iterate through the `candies` array using the `.map()` method. For each kid's candy count `c`, check if `c + extraCandies` is greater than or equal to the precalculated maximum.
3. **Return Results:** The map operation automatically returns an array of booleans representing whether each kid can achieve the maximum.

```javascript
/**
 * @param {number[]} candies
 * @param {number} extraCandies
 * @return {boolean[]}
 */
var kidsWithCandies = function(candies, extraCandies) {
    let max = Math.max(...candies)
    return candies.map(c => c + extraCandies >= max)
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $$n$$ is the number of kids (length of the `candies` array). Finding the maximum element takes $$O(n)$$ time, and mapping over the array to perform the comparison takes another $$O(n)$$ time.

- Space complexity:
$$O(1)$$ auxiliary space, as we only store a single variable `max` for the calculation. The output array of size $$O(n)$$ is required by the problem description.