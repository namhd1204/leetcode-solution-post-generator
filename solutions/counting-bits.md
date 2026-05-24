# Simple Binary String Conversion

# Intuition
The goal is to count the number of set bits (1s) in the binary representation of every number from $0$ to $n$. A straightforward way to achieve this in JavaScript is to convert each number into its binary string representation, filter out all the '0's, and count the length of the remaining string containing only '1's.

# Approach
1. Initialize the result array `res` with `[0]` since the binary representation of `0` has zero `1`s.
2. Iterate through each integer `i` from `1` to `n`.
3. For each integer, convert it to a binary string using `i.toString(2)`.
4. Remove all '0' characters from the binary string using `.replaceAll('0', '')`.
5. The length of the resulting string represents the count of '1's. Push this length into the `res` array.
6. Return the populated `res` array.

```javascript
/**
 * @param {number} n
 * @return {number[]}
 */
var countBits = function(n) {
    const res = [0]
    for(let i=1; i<=n; i++) {
        res.push(i.toString(2).replaceAll('0', '').length)
    }
    return res
};
```

# Complexity
- Time complexity:
$$O(n \log n)$$
For each number $i$ up to $n$, converting it to a binary string takes $O(\log i)$ time because a number $i$ has approximately $\log_2(i)$ bits. Replacing characters and calculating the length also scales with the number of bits, resulting in an overall time complexity of $O(n \log n)$.

- Space complexity:
$$O(n)$$
The output array `res` requires $O(n)$ space to store the results for $n + 1$ elements. The intermediate string allocations for each number require $O(\log n)$ auxiliary space.