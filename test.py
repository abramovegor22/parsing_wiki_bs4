def gcd(a, b):
  assert type(a) == int and type(b) == int
  
  while b != 0:
    r = a % b
    b = a
    a = r
  return a

gcd(1, 1)