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

  @caching_decorator(max_cache_size=3)
  def slow_function(x):
      print(f"Вычисляем {x}...")
      return x * x

  @caching_decorator(max_cache_size=3)
  def slow_function2(x):
      print(f"Вычисляем {x}...")
      return x + 2

# Первый вызов - вычисление
print(slow_function(2))  # Вычисляем 2...
print(slow_function(3))  # Вычисляем 3...
print(slow_function(4))  # Вычисляем 4...

# Повторные вызовы - из кэша
print(slow_function(2))  # Из кэша
print(slow_function(3))  # Из кэша

# Добавим еще один элемент, чтобы проверить ограничение кэша
print(slow_function(5))  # Вычисляем 5...

# Проверяем кэш: 2 и 3 должны быть в кэше, а 4 должен быть удален
print(slow_function(2))  # Вычисляем заново, так как он был удален из кэша

print(slow_function2(1)) # Вычисляем 1...
print(slow_function2(2)) # Вычисляем 2...
print(slow_function2(3)) # Вычисляем 3...

print(slow_function(4)) # Из кэша
print(slow_function2(1)) # Из кэша
