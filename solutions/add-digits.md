# Iterative Digit Summation via String Manipulation

# Intuition
The core idea is to directly simulate the process of summing digits step-by-step. By converting the number to a string, we can easily isolate each individual digit, sum them up, and repeat this reduction process until the number is reduced to a single digit (less than 10).

# Approach
1. We initiate an infinite loop (`while(true)`) to repeatedly perform the digit summation.
2. In each iteration, we convert the current number `num` to its string representation using `.toString()`.
3. We split the string into an array of individual digit characters using `.split('')`.
4. We convert each character back to a number using the unary plus operator (`+x`) and sum them up using the `.reduce()` method.
5. If the resulting sum is less than 10, we return it as the final single-digit answer. Otherwise, the loop continues with the new sum.

```javascript
/**
 * @param {number} num
 * @return {number}
 */
var addDigits = function(num) {
    while(true) {
        num = num.toString().split('').map(x => +x).reduce((a, b) => a + b, 0)
        if(num < 10) return num
    }
};
```

# Complexity
- Time complexity:
$$O(\log_{10}(\text{num}))$$
In each iteration, the number of digits is proportional to $$\log_{10}(\text{num})$$. The number of digits decreases extremely rapidly (e.g., a 10-digit number under the $$2^{31} - 1$$ constraint immediately reduces to a maximum sum of 90 in the first step, and then to a single digit in at most two more steps). Thus, the loop runs at most a few times, making the execution virtually instantaneous.

- Space complexity:
$$O(\log_{10}(\text{num}))$$
We temporarily store the string representation and the split array of digits. Since the maximum number of digits for a 32-bit integer is 10, the auxiliary space used is $$O(1)$$ in practice.