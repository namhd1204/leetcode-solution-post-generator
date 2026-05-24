# Bitwise XOR Reduction in O(N) Time and O(1) Space

# Intuition
The problem requires us to find the only element in an array that appears once, while all other elements appear exactly twice. We must do this in linear time and with constant extra space. 

The key to solving this efficiently lies in the properties of the bitwise XOR (`^`) operator:
1. **Identity**: $A \oplus 0 = A$ (Any number XORed with zero remains unchanged)
2. **Self-inverse**: $A \oplus A = 0$ (Any number XORed with itself results in zero)
3. **Commutative and Associative**: The order of XOR operations does not matter ($A \oplus B \oplus A = A \oplus A \oplus B = 0 \oplus B = B$)

By XORing all the numbers in the array together, all the duplicate pairs will cancel each other out to $0$, leaving behind only the single unique number.

# Approach
We can implement this elegant logic using JavaScript's `Array.prototype.reduce()` method. 

We initialize the accumulator with `0` and iteratively apply the XOR operator (`^`) between the accumulator and each element in the array. 
- Duplicate numbers will cancel out.
- The single number will remain.

```javascript
/**
 * @param {number[]} nums
 * @return {number}
 */
var singleNumber = function(nums) {
    return nums.reduce((a, b) => a ^ b, 0)
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $$n$$ is the length of the array. We iterate through the array exactly once to compute the XOR sum.

- Space complexity:
$$O(1)$$ as the reduction is performed in-place using a single accumulator variable, requiring no additional memory.