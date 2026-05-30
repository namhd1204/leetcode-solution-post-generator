
# Intuition
To find the third distinct maximum number, we must first eliminate duplicate values to ensure we are counting unique maximums. Once we have a collection of unique elements, we can organize them into a Max Heap. A Max Heap allows us to efficiently retrieve the largest elements in descending order. By extracting the root of the heap up to three times, we can easily find the third maximum if it exists, or fall back to the first maximum if there are fewer than three unique elements.

# Approach
1. **Deduplication**: Convert the input array `nums` into a `Set` to remove all duplicate values, and then convert it back into an array.
2. **Heap Construction**: Build a Max Heap from the unique array in-place using the bottom-up heapify method (Floyd's formulation), which runs in linear time relative to the number of unique elements.
3. **Extraction**: Extract the maximum element from the heap up to three times:
   - The first extraction yields the absolute maximum (`firstMax`).
   - The second extraction yields the second maximum (`secondMax`).
   - The third extraction yields the third maximum (`thirdMax`).
4. **Result Selection**: If the third maximum is successfully extracted (i.e., it is not `null`), return it. Otherwise, return the first maximum.

```javascript
/**
 * @param {number[]} nums
 * @return {number}
 */
var thirdMax = function(nums) {
    const maxheap = buildUniqueMaxHeap(nums)
    const firstMax = extractMax(maxheap)
    const secondMax = extractMax(maxheap)
    const thirdMax = extractMax(maxheap)
    // console.log({firstMax, secondMax, thirdMax})
    return thirdMax !== null ? thirdMax : firstMax
};

/**
 * Transforms an array of integers into a unique Max Heap.
 * @param {number[]} rawArray - The input array of integers.
 * @return {number[]} A flat array representing the Max Heap with unique elements.
 */
function buildUniqueMaxHeap(rawArray) {
    // 1. Remove duplicates using a Set and immediately convert back to an array
    const heap = Array.from(new Set(rawArray));
    const size = heap.length;

    // 2. Heapify Down function using a loop for performance optimization
    const heapifyDown = (index) => {
        while (true) {
            let maxIndex = index;
            const left = 2 * index + 1;
            const right = 2 * index + 2;

            if (left < size && heap[left] > heap[maxIndex]) {
                maxIndex = left;
            }
            if (right < size && heap[right] > heap[maxIndex]) {
                maxIndex = right;
            }

            // If the current node is the largest, the heap property is valid at this position
            if (maxIndex === index) break;

            // Direct swap using ES6 Destructuring syntax
            [heap[index], heap[maxIndex]] = [heap[maxIndex], heap[index]];
            
            // Continue to heapify down from the newly swapped position
            index = maxIndex;
        }
    };

    // 3. Build the Heap using the bottom-up approach (from the last internal node up to the root)
    const startIndex = Math.floor(size / 2) - 1;
    for (let i = startIndex; i >= 0; i--) {
        heapifyDown(i);
    }

    // Return the underlying flat heap array
    return heap;
}

/**
 * Extracts and removes the maximum element from the unique Max Heap.
 * @param {number[]} heap - The unique flat heap array (result of buildUniqueMaxHeap).
 * @return {number|null} The maximum value, or null if the Heap is empty.
 */
function extractMax(heap) {
    const size = heap.length;
    
    // Case 1: Empty heap
    if (size === 0) return null;
    
    // Case 2: Heap has exactly 1 element, extract it directly
    if (size === 1) return heap.pop();

    // Case 3: Heap has multiple elements
    const maxVal = heap[0]; // 1. Store the maximum value at the root
    heap[0] = heap.pop();   // 2. Move the last element to replace the root position

    // 3. Heapify down the root element to its correct position
    let index = 0;
    const currentSize = heap.length; // New size after pop()

    while (true) {
        let maxIndex = index;
        const left = 2 * index + 1;
        const right = 2 * index + 2;

        // Directly compare integer values between parent and left child nodes
        if (left < currentSize && heap[left] > heap[maxIndex]) {
            maxIndex = left;
        }
        
        // Compare with the right child node
        if (right < currentSize && heap[right] > heap[maxIndex]) {
            maxIndex = right;
        }

        // If the parent node is larger than both children, the heap property is valid; stop the loop
        if (maxIndex === index) break;

        // Swap the parent node with the larger child node
        [heap[index], heap[maxIndex]] = [heap[maxIndex], heap[index]];
        
        // Update the index to continue checking the lower levels
        index = maxIndex;
    }

    // Return the extracted maximum value
    return maxVal;
}
```