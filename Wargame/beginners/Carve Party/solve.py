pumpkin = [ 124, 112, 59, 73, 167, 100, 105, 75, 59, 23, 16, 181, 165, 104, 43, 49, 118, 71, 112, 169, 43, 53 ];
counter = 0;
pie = 1;

for i in range(10000):
    if i <= 10000 and i % 100 == 0:
      for j in range(len(pumpkin)):
        pumpkin[j] ^= pie
        pie = ((pie ^ 0xff) + (j * 10)) & 0xff


for i in range(len(pumpkin)):
   pumpkin[i] = chr(pumpkin[i])
print("".join(pumpkin))