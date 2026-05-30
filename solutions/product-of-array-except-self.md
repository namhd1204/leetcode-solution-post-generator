# Case-Based Zero Counting Approach

# Intuition
The presence of zero elements completely dictates the output of this problem. By analyzing the number of zeros in the input array, we can divide the problem into three distinct scenarios:
1. **No zeros:** The product except `nums[i]` is simply the total product of all elements divided by `nums[i]`. Since division is restricted, we can mathematically represent division by multiplying by the reciprocal ($$x^{-1}$$).
2. **Exactly one zero:** The product except self for the zero element will be the product of all other non-zero elements. For all other elements, the product will be `0` because it includes the single zero.
3. **Two or more zeros:** The product except self for every single element will always include at least one zero, meaning the entire output array will consist of zeros.

# Approach
1. Filter the input array to extract all non-zero elements.
2. Determine the count of zeros by subtracting the length of the non-zero array from the original array's length.
3. Calculate the product of all non-zero elements using the `reduce` helper.
4. Branch into three cases based on the zero count:
   - **Case 1 (0 zeros):** Map each element to the product of all non-zeros multiplied by its reciprocal (`Math.pow(num, -1)`).
   - **Case 2 (1 zero):** Map the zero element to the product of all non-zeros, and map all other elements to `0`.
   - **Case 3 (2+ zeros):** Return an array of the same length filled entirely with `0`.

```javascript
/**
 * @param {number[]} nums
 * @return {number[]}
 */
var productExceptSelf = function(nums) {
    let total = 0;
    let noneZeros = nums.filter(x => x)
    let countZero = nums.length - noneZeros.length
    let allNoneZeros = noneZeros.reduce((a, b) => a * b, 1)
    if(countZero === 0) {
        return nums.map(num => allNoneZeros * Math.pow(num, -1))
    } else if(countZero === 1) {
        return nums.map(num => {
            return num === 0 ? allNoneZeros : 0 
        })
    } else {
        return Array(nums.length).fill(0)
    }
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $$n$$ is the length of the array. Filtering, reducing, and mapping each take linear time $$O(n)$$, resulting in an overall linear time complexity.

- Space complexity:
$$O(n)$$ auxiliary space to store the filtered `noneZeros` array.