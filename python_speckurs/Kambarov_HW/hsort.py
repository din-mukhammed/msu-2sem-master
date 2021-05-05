def heapify(X, n, i):
    largest = i
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
  
    if l < n and X[i] < X[l]:
        largest = l
  
    if r < n and X[largest] < X[r]:
        largest = r
  
    if largest != i:
        X[i], X[largest] = X[largest], X[i]
        heapify(X, n, largest)
        
def heap_sort(X):
    n = len(X)
    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(X, n, i)
  
    # One by one extract elements
    for i in range(n-1, 0, -1):
        X[i], X[0] = X[0], X[i]   # swap
        heapify(X, i, 0)
    return X
