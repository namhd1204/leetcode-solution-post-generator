# Binary Search with Midpoint Partitioning

# Intuition
The problem asks us to find a hidden number within a sorted range from `1` to `n`. Since the range is sorted and we receive feedback on whether our guess is too high or too low, we can discard half of the remaining search space with each guess. This logarithmic reduction of the search space makes Binary Search the optimal strategy.

# Approach
1. **Edge Case Check**: First, check if the maximum number `n` is the correct guess. If `guess(n) === 0`, return `n` immediately.
2. **Initialize Pointers**: Define the search boundaries with `from = 1` and `to = n`.
3. **Binary Search Loop**:
   - Calculate the midpoint `val` of the current range using `parseInt((to + from) / 2)`.
   - Query the API with `guess(val)`:
     - If the result is `0`, we have found the correct number and return `val`.
     - If the result is `1`, the picked number is higher than our guess, so we shift our lower bound `from` to `val`.
     - If the result is `-1`, the picked number is lower than our guess, so we shift our upper bound `to` to `val`.
4. The loop runs until the correct number is found and returned.

```javascript
/** 
 * Forward declaration of guess API.
 * @param {number} num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * var guess = function(num) {}
 */

/**
 * @param {number} n
 * @return {number}
 */
var guessNumber = function(n) {
    if(guess(n) === 0) return n

    let from = 1
    let to = n

    while(true) {
        let val = parseInt((to + from) / 2)
        // console.log({from, to, val})
        if(guess(val) === 0) {
            return val
        }
        guess(val) === 1 ? from = val : to = val
    }
};
```

# Complexity
- Time complexity:
$$O(\log n)$$
In each step of the binary search, the search space is halved. Thus, the algorithm takes logarithmic time to find the target number.

- Space complexity:
$$O(1)$$
The algorithm uses a constant amount of extra space for pointers (`from`, `to`, and `val`), requiring no additional memory allocation.