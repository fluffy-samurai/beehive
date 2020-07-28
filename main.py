import qwiic
import time
import sys
import splunklib.client as client

HOST = "localhost"
PORT = 8089
USERNAME = "admin"
PASSWORD = "yourpassword"

#These values are used to give BME280 and CCS811 some time to take samples
initialize=True
n=2

#Qwiic Board define
bme = qwiic.QwiicBme280()
ccs = qwiic.QwiicCcs811()

#Begin statements
bme.begin()
#ccs.begin()

#Used for debugging CCS811
try:
    ccs.begin()

except Exception as e:
    print(e)

# Create a Service instance and log in
service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)

beehive_index = service.indexes.create("beehive_index")

while True:
    try:
        if initialize:
            print("Initializing: BME280 and CCS811 are taking samples before printing and publishing data!")
            print(" ")

            pressure = bme.get_reference_pressure()  # in Pa
            humidity = bme.read_humidity()
            tempf = bme.get_temperature_fahrenheit()
            dewf = bme.get_dewpoint_fahrenheit()

            ccs.read_algorithm_results()  # updates the TVOC and CO2 values
            tvoc = ccs.get_tvoc()
            co2 = ccs.get_co2()

            # Give some time for the BME280 and CCS811 to initialize when starting up
            time.sleep(10)
            initialize = False
        else:
            # BME280 sensor variables
            # reference pressure is available to read or set for altitude calculation
            pressure = bme.get_reference_pressure()  # in Pa
            humidity = bme.read_humidity()
            tempf = bme.get_temperature_fahrenheit()
            dewf = bme.get_dewpoint_fahrenheit()

            ccs.read_algorithm_results()  # updates the TVOC and CO2 values
            tvoc = ccs.get_tvoc()
            co2 = ccs.get_co2()

            # Give some time for the BME280 and CCS811 to initialize when starting up
            if initialize:
                time.sleep(10)
                initialize = False

        print("BME Temperature %.1f F" % tempf)
        print("Humidity %.1f" % humidity)
        print("Pressure %.2f Pa" % pressure)
        print("TVOC %.2f" % tvoc)
        print("CO2 %.2f" % co2)

        print(" ")  # blank line for easier readability

        beehive_index.submit(f"[temp={tempf}] [humidity={humidity}] [pressure={pressure}] [tvoc={tvoc}] [co2={co2}] [dewf={dewf}]")

        # delay (number of seconds) so we are not constantly displaying data and overwhelming devices
        time.sleep(5)

    except (EOFError, SystemExit, KeyboardInterrupt):
        sys.exit()
