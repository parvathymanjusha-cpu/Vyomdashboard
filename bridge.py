import serial
import requests
import json
import time


# ==========================================
# SETTINGS
# ==========================================

SERIAL_PORT = "COM5"

# Matches the real receiver and fake ESP32
BAUD_RATE = 9600

DJANGO_URL = https://vyomdashboard.onrender.com/api/telemetry/

SERIAL_TIMEOUT = 1


# ==========================================
# PARSE DATA PACKET
# ==========================================

def parse_data_packet(line):
    """
    Converts a receiver DATA line into a dictionary.

    Example:
    DATA: ID=1,TEMP=25.5,HUM=50.0,LAT=10.100000,
    LON=76.200000,ALT=100.0,SAT=5
    """

    line = line.strip()

    if not line.startswith("DATA:"):
        return None

    data_text = line.replace("DATA:", "", 1).strip()

    values = {}

    try:
        parts = data_text.split(",")

        for part in parts:
            if "=" not in part:
                continue

            key, value = part.split("=", 1)

            key = key.strip().upper()
            value = value.strip()

            values[key] = value

        return values

    except Exception as error:
        print("Packet parsing error:", error)
        return None


# ==========================================
# SEND DATA TO DJANGO
# ==========================================

def send_to_django(values):
    """
    Sends the telemetry fields currently supported
    by the Django API.
    """

    try:
        telemetry_data = {
            "temperature": float(values["TEMP"]),
            "humidity": float(values["HUM"]),
            "latitude": float(values["LAT"]),
            "longitude": float(values["LON"])
        }

    except KeyError as error:
        print("Missing telemetry field:", error)
        return

    except ValueError as error:
        print("Invalid telemetry value:", error)
        return

    try:
        response = requests.post(
            DJANGO_URL,
            json=telemetry_data,
            timeout=5
        )

        if response.status_code in [200, 201]:
            print("SUCCESS: Telemetry sent to Django")
            print("Data:", telemetry_data)
            print("Status:", response.status_code)

        else:
            print("Django returned an error")
            print("Status:", response.status_code)
            print("Response:", response.text)

    except requests.exceptions.RequestException as error:
        print("Could not connect to Django:", error)


# ==========================================
# MAIN SERIAL BRIDGE
# ==========================================

def main():

    print("------------------------------------------")
    print("VYOMASTHRA TELEMETRY BRIDGE")
    print("------------------------------------------")
    print("Serial port:", SERIAL_PORT)
    print("Baud rate:", BAUD_RATE)
    print("Django URL:", DJANGO_URL)
    print("------------------------------------------")

    try:
        serial_connection = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=SERIAL_TIMEOUT
        )

        time.sleep(2)

        print("Serial connection established.")
        print("Waiting for telemetry packets...")
        print("Press CTRL+C to stop.")
        print("------------------------------------------")

    except serial.SerialException as error:
        print("Could not open serial port.")
        print("Error:", error)
        print()
        print("Check the following:")
        print("1. The correct COM port is selected.")
        print("2. Arduino Serial Monitor is closed.")
        print("3. Another Python bridge is not running.")
        return

    try:

        while True:

            raw_line = serial_connection.readline()

            if not raw_line:
                continue

            try:
                line = raw_line.decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

            except Exception:
                continue

            if not line:
                continue

            print("SERIAL:", line)

            # Process receiver-style DATA packets
            values = parse_data_packet(line)

            if values is not None:

                print("PACKET PARSED:", values)

                send_to_django(values)

                print("------------------------------------------")

    except KeyboardInterrupt:
        print()
        print("Bridge stopped by user.")

    finally:
        serial_connection.close()
        print("Serial connection closed.")


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()