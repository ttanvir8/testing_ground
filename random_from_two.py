# take one number from 10 or 11 and print it
import random
two_numbers = [10, 11]
count = 0
count_10 = 0
count_11 = 0
total = 0
def random_from_two(count, count_10, count_11, total, two_numbers):
    for i in range(31):
        num = random.choice(two_numbers)
        count += 1 
        if num == 10:
            count_10 += 1
        else:
            count_11 += 1
    
        total += num
    return total, count, count_10, count_11

total, count, count_10, count_11 = random_from_two(count, count_10, count_11, total, two_numbers)    
print(count)
print(count_10)
print(count_11)
print(total)

# now run the random_from_two function 3 times and print the values for total, count, count_10, count_11 for each run
for i in range(3):
    count = 0
    count_10 = 0
    count_11 = 0
    total = 0
    total, count, count_10, count_11 = random_from_two(count, count_10, count_11, total, two_numbers)
    print(f"Run {i+1}:", end= " ")
    print(total)
    print(count)
    print(count_10)
    print(count_11)
    print(" ")