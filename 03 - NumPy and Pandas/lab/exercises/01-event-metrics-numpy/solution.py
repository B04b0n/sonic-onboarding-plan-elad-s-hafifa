# Import NumPy
import numpy as np
import time

# Import the data generator
# from  import generate_latencies
from exercis_01_sample_data import generate_latencies

# Generate 1,000 latency measurements
latencies = generate_latencies(100000)

# Print first few values to see what you're working with
print("First 10 latencies:")
print(latencies[:10])
print(f"\nTotal events: {len(latencies)}")
print(f"Data type: {latencies.dtype}")
print(np.shape(latencies))
print(np.ndim(latencies))
print(latencies.dtype)
print(latencies.min())
print(latencies.max())

# step 3
print(f'Mean: {np.mean(latencies)} or another way is {latencies.sum()/len(latencies)}')
print(f'meidan: {np.percentile(latencies,50)} another way is {np.median(latencies,)}')
print(f'std: {np.std(latencies)}')

#step 4
print(f'95%: {np.percentile(latencies, 95)}')
print(f'99%: {np.percentile(latencies, 99)}')

# step 5
slow_events = latencies[latencies > 500]
super_slow_events = latencies[latencies > 1000]
print(f'slow event {len(slow_events)} and the super slow ones are {len(super_slow_events)}')

# step 6
fast_events_amount = len(latencies[latencies < 200])
mid_events_amount = len(latencies[(latencies >= 200) & (latencies < 500)])
slow_events_amount = len(latencies[(latencies >= 500) & (latencies < 1000)])
super_slow_events_amount = len(latencies[latencies >= 1000])

print(f"""
fast_events_amout {fast_events_amount}
mid_events_amout {mid_events_amount}
slow_events_amout {slow_events_amount}
super_slow_events_amout {super_slow_events_amount}
total {
fast_events_amount
+mid_events_amount
+slow_events_amount
+super_slow_events_amount
}
""")

# step 7
latency_mean = latencies.mean()
latency_std = latencies.std()

def calc_z_score (value):
     return (value - latency_mean) / latency_std

latencies_distance_from_mean = latencies - latency_mean
latencies_z_score = np.abs(latencies_distance_from_mean / latency_std)

print(f"""
z score is 
{latencies_z_score[:10]}

another way is
{np.abs(calc_z_score(latencies))[:10]}
""")

# step 8
print(-(len(latencies_z_score)/100))

suspicious_z_scores_positions = (np.argpartition(latencies_z_score, -(len(latencies_z_score) // 100))[-(len(latencies_z_score) // 100):])

print(suspicious_z_scores_positions)

print( np.where(latencies_z_score > 2)[0][-10:])


# Performance Comparison
# step 9
# how fast is numpy

print('calc min duration via numpy')
np_time_sart = time.time()
np_mean_calc = latencies.mean()
np_time_end = time.time()
print(f"numpy timestemp {np_time_end - np_time_sart}")

print('-------------------------------')
print('calc min duration via python function')
py_fun_time_sart = time.time()
py_fun_mean = sum(latencies)/len(latencies)
py_fun_time_end = time.time()
print(f"python timetemp functions {py_fun_time_end - py_fun_time_sart}")
print('-------------------------------')
print('calc min duration via python loop')
py_time_sart = time.time()
sum =0
for latency in latencies:
    sum += latency
py_loop_mean = sum/len(latencies)
py_time_end = time.time()
print(f"python timetemp {py_time_end - py_time_sart}")
print('-------------------------------')
print('calc min duration via python while loop')
py_time_sart_while = time.time()
sum =0
current_index = 0
while current_index < len(latencies):
    sum += latencies[current_index]
    current_index+=1
py_loop_mean = sum/len(latencies)
py_time_end_while = time.time()
print(f"python timetemp while {py_time_end_while - py_time_sart_while}")

print('--------------------------------')
print(f"""
np {np_mean_calc}
function { py_fun_mean}
loop { py_loop_mean}
""")

print(time.time())
print(time.time())

# sum = 0
# y = map(lambda x, y: x+y, latencies)
# print (y)
# x = lambda a: sun +=a, latencies