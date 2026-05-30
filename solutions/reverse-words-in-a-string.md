# Elegant One-Line Split, Filter, and Reverse

# Intuition
The core task is to reverse the order of words in a string while cleaning up any extra spaces (leading, trailing, or multiple spaces between words). By splitting the string by spaces, we can isolate the words. However, consecutive spaces will produce empty strings in our split array. We can easily clean these up by filtering out the empty strings, reversing the remaining valid words, and joining them back together with a single space.

# Approach
The solution leverages JavaScript's built-in array methods to achieve this in a clean, functional pipeline:

1. **`split(' ')`**: Splits the string into an array of substrings using a single space as the delimiter.
2. **`filter(x => x)`**: Filters out any empty strings (`""`). In JavaScript, an empty string is falsy, so `x => x` keeps only non-empty, truthy strings (the actual words). This handles leading, trailing, and multiple consecutive spaces.
3. **`reverse()`**: Reverses the array of cleaned words in-place.
4. **`join(' ')`**: Concatenates the reversed words back into a single string, separated by exactly one space.

```javascript
/**
 * @param {string} s
 * @return {string}
 */
var reverseWords = function(s) {
    return s.split(' ').filter(x => x).reverse().join(' ')
};
```

# Complexity
- Time complexity:
$$O(n)$$ where $$n$$ is the length of the string `s`. Splitting the string, filtering the array, reversing the elements, and joining them back together each take linear time relative to the size of the input.

- Space complexity:
$$O(n)$$ to store the intermediate array of words and the final reconstructed string.