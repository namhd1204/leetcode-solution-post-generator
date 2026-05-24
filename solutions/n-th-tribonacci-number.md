# Iterative Sliding Window with Constant Space

# Intuition
The Tribonacci sequence is a variation of the Fibonacci sequence where each term is the sum of the preceding three terms: $T_n = T_{n-1} + T_{n-2} + T_{n-3}$. 

Instead of using recursion (which can lead to redundant calculations) or storing the entire sequence in an array of size $n$ (which uses $O(n)$ space), we only need to keep track of the three most recent values. By shifting these three values forward in a sliding-window fashion, we can compute the $n$-th Tribonacci number in linear time and constant space.

# Approach
1. **Handle Base Cases**: Directly return the known values for $n = 0$ ($0$), $n = 1$ ($1$), and $n = 2$ ($1$).
2. **Initialize State**: For $n \ge 3$, we start our tracking at $i = 3$. We initialize:
   - `currentTribonacci` to $2$ (which is $T_3 = T_2 + T_1 + T_0 = 1 + 1 + 0$)
   - `preOne` to $1$ (representing $T_2$)
   - `preTwo` to $1$ (representing $T_1$)
3. **Iterate and Shift**: Run a loop from $i = 3$ up to $n - 1$. In each iteration, we update our three state variables simultaneously using JavaScript's array destructuring assignment:
   - The new `currentTribonacci` becomes the sum of the current three values.
   - `preOne` shifts to the old `currentTribonacci`.
   - `preTwo` shifts to the old `preOne`.
4. **Return Result**: Once the loop finishes, `currentTribonacci` will hold the value of $T_n$.

```javascript
/**
 * @param {number} n
 * @return {number}
 */
var tribonacci = function(n) {
    if(n === 0) return 0
    if(n === 1 || n === 2) return 1

    let currentTribonacci = 2
    let preOne = preTwo = 1
    let i = 3
    while(i < n) {
        [currentTribonacci, preOne, preTwo] = [currentTribonacci + preOne + preTwo, currentTribonacci, preOne ]
        i++
    }

    return currentTribonacci
};
```

# Complexity
- Time complexity:
$$O(n)$$  
We perform a single loop from $3$ to $n$, executing a constant number of operations in each iteration.

- Space complexity:
$$O(1)$$  
We only use a fixed number of variables (`currentTribonacci`, `preOne`, `preTwo`, and `i`) to maintain the state, requiring constant extra memory.