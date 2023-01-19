import time
from csv import writer, DictWriter
import random
import time
CSV_PATH = 'data\\test.csv'

def ustaw(y):
    y = int(time.time())
    x = random.randint(0, 750)
    z = random.randint(0, 750)
    w = random.randint(0, 4)

    field_names = ['data','humidity','assigned_humidity','water_level']

    dict = {'data': y, 'humidity': x, 'assigned_humidity': z, 'water_level': w}

    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open(CSV_PATH, 'a') as f_object:
        # Pass the file object and a list
        # of column names to DictWriter()
        # You will get a object of DictWriter
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)

        # Pass the dictionary as an argument to the Writerow()
        dictwriter_object.writerow(dict)

        # Close the file object
        f_object.close()

    time.sleep(0.5)
    return ustaw(y+300)

ustaw(1)
