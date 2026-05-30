# Logarithmic Check in Constant Time

# Intuition
A number $n$ is a power of two if and only if its logarithm to the base 2 is an integer. By leveraging JavaScript's built-in mathematical functions, we can determine if $n$ is a power of two in constant time without relying on loops or recursion.

# Approach
1. **Base Cases**: 
   - If $n = 1$, it is $2^0$, so we return `true`.
   - If $n = 0$, it cannot be a power of two, so we return `false`.
2. **Logarithmic Calculation**: We calculate the base-2 logarithm of $n$ using `Math.log2(n)`.
3. **Integer Check**: We check if the result is an integer. If `log2` is greater than its integer representation (`parseInt(log2)`), it means `log2` has a fractional part, so $n$ is not a power of two.
4. **Precision Verification**: To guard against floating-point precision inaccuracies, we perform a final check to ensure that $2^{\log_2(n)}$ indeed equals $n$.

```javascript
/**
 * @param {number} n
 * @return {boolean}
 */
var isPowerOfTwo = function(n) {
    if(1 === n) return true
    if(0 === n) return false
    let log2 = Math.log2(n)
    if(log2 > parseInt(log2)) return false
    return Math.pow(2, log2) === n
};
```

# Complexity
- Time complexity:
$$O(1)$$
The mathematical operations `Math.log2` and `Math.pow` execute in constant time.

- Space complexity:
$$O(1)$$
The algorithm uses a constant amount of extra space to store the `log2` variable.