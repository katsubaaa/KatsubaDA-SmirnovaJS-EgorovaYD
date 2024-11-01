  import functools

  def caching_decorator(max_cache_size=128):
    cache = {}
    
    def decorator(func):
      @functools.wraps(func)
      def wrapper(*args):
        if args in cache:
          return cache[args]
        result = func(*args)
        if len(cache) >= max_cache_size:
          cache.pop(next(iter(cache)))  # Удаляем старейший элемент
        cache[args] = result
        return result
      return wrapper
      
    return decorator

