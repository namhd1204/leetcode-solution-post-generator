# Queue-Based Sliding Window

# Intuition
The problem requires us to count the number of requests that have occurred in the last 3000 milliseconds. Since the incoming timestamps `t` are guaranteed to be strictly increasing, any request that becomes too old (i.e., older than `t - 3000`) will remain invalid for all future `ping` calls. 

This First-In, First-Out (FIFO) behavior makes a **Queue** the ideal data structure. We can append new requests to the end of the queue and efficiently discard outdated requests from the front.

# Approach
1. **Initialization**: We initialize a queue to store the timestamps of the incoming requests.
2. **On `ping(t)`**:
   - Add the current timestamp `t` to the end of the queue.
   - Check the front of the queue. While the oldest timestamp is strictly less than `t - 3000`, it is out of the active window, so we remove (dequeue) it.
   - Once the front of the queue contains a timestamp within the range `[t - 3000, t]`, all remaining elements in the queue are guaranteed to be valid.
   - Return the size of the queue, which represents the number of active requests in the current window.

```csharp
public class RecentCounter {

    Queue<int> request {get; set;} = new Queue<int>();

    public RecentCounter() {
        
    }
    
    public int Ping(int t) {
        request.Enqueue(t);

        while(request.Count > 0) {
            if(request.Peek() < t - 3000) {
                request.Dequeue();
            } else {
                break;
            }
        }

        return request.Count;
    }
}

/**
 * Your RecentCounter object will be instantiated and called as such:
 * RecentCounter obj = new RecentCounter();
 * int param_1 = obj.Ping(t);
 */
```

# Complexity
- Time complexity:
  - **Amortized $$O(1)$$** per `ping` call. Each timestamp is enqueued exactly once and dequeued at most once. Across $N$ total calls, the total time spent on queue operations is $$O(N)$$.

- Space complexity:
  - **$$O(W)$$**, where $W$ is the maximum number of requests that can occur within any 3000-millisecond window. In the worst case, this is bounded by the total number of queries, which is $$O(N)$$.