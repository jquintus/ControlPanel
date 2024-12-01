import os
import board
import microcontroller

print("CircuitPython Version:", os.uname().version)
print("Machine Info:", os.uname().machine)
print("Board:", board.board_id)

# Get the unique ID of the microcontroller
unique_id = microcontroller.cpu.uid
unique_id_str = ":".join("{:02x}".format(byte) for byte in unique_id)

# Get the microcontroller name
#cpu_name = microcontroller.cpu.name

# Get the frequency of the CPU
cpu_frequency = microcontroller.cpu.frequency

# Print board-specific information
print("Microcontroller Unique ID:", unique_id_str)
#print("CPU Name:", cpu_name)
print("CPU Frequency (Hz):", cpu_frequency)
