# Greedy Single-Pass Simulation with Boundary Checks

# Intuition
The problem asks us to determine if we can plant $n$ flowers in a flowerbed without planting any two flowers adjacent to each other. 

A greedy approach is optimal here: we should place a flower at the very first available valid plot we encounter. Placing a flower as early as possible leaves the maximum number of options open for the remaining plots. A plot at index `i` is valid for planting if:
1. The plot itself is empty (`0`).
2. The left neighbor (if it exists) is empty (`0`).
3. The right neighbor (if it exists) is empty (`0`).

# Approach
1. **Base Case**: If `n` is already `0`, we can immediately return `true`.
2. **Iteration**: Traverse the `flowerbed` array from left to right.
3. **Skip Occupied Plots**: If the current plot is `1`, we cannot plant here, so we skip to the next index.
4. **Validation**: If the current plot is `0`, we use a helper function `canPlaceFlower` to check if both adjacent plots are empty.
   - If `index` is `0`, we only need to check if the next plot is `0` (or if the array has a length of 1).
   - If `index` is the last element, we only need to check if the previous plot is `0`.
   - Otherwise, we check if both the previous and next plots are `0`.
5. **Placement**: If the helper function returns `true`, we plant a flower by setting `flowerbed[index] = 1` and decrementing `n`.
6. **Early Exit**: If `n` reaches `0` at any point during the loop, we return `true`.
7. **Final Check**: If we finish traversing the array and `n` is still greater than `0`, we return `false`.

```javascript
/**
 * @param {number[]} flowerbed
 * @param {number} n
 * @return {boolean}
 */
var canPlaceFlowers = function(flowerbed, n) {
    if(n === 0) return true
    let index = 0
    for(let index = 0; index < flowerbed.length; index++) {
        if(flowerbed[index] === 1) {
            continue
        }

        if(canPlaceFlower(flowerbed, index)) {
            flowerbed[index] = 1
            n--
        }

        if(n === 0) return true    
    }
    return false
};

var canPlaceFlower = function(flowerbed, index) {
    if(index === 0) {
        if(index + 1 === flowerbed.length) return true
        return flowerbed[index + 1] === 0
    }

     if(index === flowerbed.length - 1) {
        return flowerbed[index - 1] === 0
    }

    return flowerbed[index + 1] === 0 && flowerbed[index - 1] === 0
}
```

# Complexity
- Time complexity:
$$O(N)$$ where $$N$$ is the length of the `flowerbed` array. We perform a single pass over the array, and the helper function `canPlaceFlower` runs in $$O(1)$$ constant time.

- Space complexity:
$$O(1)$$ auxiliary space. The algorithm modifies the input array in-place and uses only a few variables to keep track of the loop index and the count of remaining flowers.