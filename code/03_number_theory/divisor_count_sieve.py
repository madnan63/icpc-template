N = 10**5

divisor_count = [0] * (N + 1)

for i in range(1, N + 1):
    for j in range(i, N + 1, i):
        divisor_count[j] += 1

# For sum of divisors instead:
divisor_sum = [0] * (N + 1)
for i in range(1, N + 1):
    for j in range(i, N + 1, i):
        divisor_sum[j] += i
