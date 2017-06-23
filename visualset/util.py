def chunked(seq, n):
    chunk = []
    for i in seq:
        chunk.append(i)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
            
