import serial
import time
import csv

# Open serial connection
ser = serial.Serial('/dev/cu.usbserial-0001', 9600, timeout=2)
time.sleep(2)  # Wait for Arduino reset

# Open the CSV file
with open('delta_path.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 2:
            continue  # skip bad rows

        try:
            # Parse x and y as integers
            x = int(row[0].strip())
            y = int(row[1].strip())
        except ValueError:
            print(f"Invalid row: {row}")
            continue  # skip bad rows

        # Send the step command
        msg = f"{x},{y}\n"
        ser.write(msg.encode())
        print(f"Sent: {msg.strip()}")

        # Wait for OK from Arduino
        start_time = time.time()
        while True:
            if ser.in_waiting:
                response = ser.readline().decode().strip()
                if response == "OK":
                    print("Received OK")
                    break
                elif response:
                    print(f"Received unexpected: {response}")

            # Timeout in case Arduino doesn't reply
            if time.time() - start_time > 5:
                print("Timeout waiting for OK!")
                ser.close()
                raise Exception("Arduino not responding")

ser.close()