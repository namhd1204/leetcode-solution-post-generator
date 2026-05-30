# Bottom-Up Dynamic Programming with Linear Space

# Intuition
The problem asks for the minimum cost to reach the top of a staircase. At any step $i$, the minimum cost to reach it depends only on the minimum costs to reach the previous two steps ($i-1$ and $i-2$) plus the cost of stepping off them. This optimal substructure and overlapping subproblems naturally point to a Dynamic Programming approach.

# Approach
1. Create a DP array `rememberCost` of size `cost.length + 1` initialized to `0`. Each index `i` in this array represents the minimum cost to reach step `i`.
2. Since we can start at either index `0` or index `1` without paying any initial cost, the minimum cost to reach step `0` and step `1` is `0`. Thus, `rememberCost[0] = 0` and `rememberCost[1] = 0`.
3. Iterate from step `2` up to `cost.length`. For each step `i`, the minimum cost to reach it is the minimum of:
   - The cost to reach step `i-1` plus the cost to step off it: `rememberCost[i-1] + cost[i-1]`
   - The cost to reach step `i-2` plus the cost to step off it: `rememberCost[i-2] + cost[i-2]`
4. Return `rememberCost[cost.length]`, which represents the minimum cost to reach the top of the staircase.

```javascript
/**
 * @param {number[]} cost
 * @return {number}
 */
var minCostClimbingStairs = function (cost) {
    const rememberCost = Array(cost.length + 1).fill(0)
    for(let i=2; i<rememberCost.length; i++) {
        rememberCost[i] = Math.min(
            rememberCost[i-1] + cost[i-1],
            rememberCost[i-2] + cost[i-2]
        )
    }
    return rememberCost[cost.length]
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $n$ is the length of the `cost` array. We iterate from `2` to `n` exactly once, performing constant-time operations at each step.

- Space complexity:
$$O(n)$$ to store the `rememberCost` array of size $n + 1$.