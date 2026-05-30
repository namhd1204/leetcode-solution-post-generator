# Simple Iterative Row Generation

# Intuition
Pascal's Triangle is built row by row, where each row starts and ends with `1`. Any element in the middle of a row is the sum of the two elements directly above it from the previous row. By leveraging this mathematical property, we can construct the triangle iteratively, using the previously computed row to build the current one.

# Approach
1. Initialize an empty array `res` to store the rows of Pascal's Triangle.
2. Loop through each row index `rowIndex` from `0` up to `numRows - 1`.
3. For each row, initialize an array of size `rowIndex + 1` filled with `1`s. This automatically handles the boundary elements (the first and last elements of each row, which are always `1`).
4. For rows with an index greater than 1 (i.e., rows with 3 or more elements), iterate through the inner elements (from index `1` to `rowIndex - 1`).
5. Update each inner element at `res[rowIndex][columnIndex]` by summing the two adjacent elements from the previous row: `res[rowIndex - 1][columnIndex]` and `res[rowIndex - 1][columnIndex - 1]`.
6. Return the completed list of rows.

```javascript
/**
 * @param {number} numRows
 * @return {number[][]}
 */
var generate = function(numRows) {
    let res = []
    let rowIndex = 0
    while(rowIndex < numRows) {
        if(rowIndex <= 1) {
            res[rowIndex] = Array(rowIndex + 1).fill(1)
        } else {
            res[rowIndex] = Array(rowIndex + 1).fill(1)
            for(let columnIndex = 1; columnIndex < rowIndex; columnIndex++) {
                // console.log({rowIndex, columnIndex})
                res[rowIndex][columnIndex] = res[rowIndex - 1][columnIndex] + res[rowIndex-1][columnIndex-1]
            }
        }
        rowIndex++
    }
    // console.log(res)
    return res
};
```

# Complexity
- Time complexity:
$$O(\text{numRows}^2)$$  
The total number of iterations is proportional to the total number of elements in the triangle. For $N$ rows, the number of elements is $\frac{N(N+1)}{2}$, which results in a quadratic time complexity.

- Space complexity:
$$O(\text{numRows}^2)$$  
The space complexity is determined by the storage required for the output array, which contains $\frac{N(N+1)}{2}$ elements. Excluding the output space, the auxiliary space complexity is $$O(1)$$.