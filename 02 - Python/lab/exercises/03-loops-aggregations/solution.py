import cmath

sum_count =0

for i in range(11):
    print(i)
    sum_count+=i

print(sum_count)

response_times = [120, 340, 95, 610, 450, 280, 190]

print(f'avg {sum(response_times)/len(response_times)}')

print("slow:")

for time in response_times:
    if(time > 300):
        print(f"time, {time}, index: {response_times.index(time)}")