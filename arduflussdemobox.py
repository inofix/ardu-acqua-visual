#!/usr/bin/env python

import configargparse

from time import sleep
from libacquavisual import thermometer, hygrometer, glassofwater
from libardurep import datastore, datareporter, serialreader

def demo_run(args):
    temp = thermometer.Thermometer()
    hum = hygrometer.Hygrometer()
    glass = glassofwater.GlassOfWater()
    glass.calibrate(.38, .38)

    # some phantasy-values
    ws = [ .370, .367, .362, .288, .264, .249, .27, .32, .35 ]
    ts = [ 18.8, 19.3, 20, 20.1, 19.4 ]
    hs = [ 60, 61, 62, 61 ]
    # indices
    wi = ti = hi = 0

    while True:
        sleep(1)
        temp.display_value(ts[ti])
        if ti >= len(ts) - 1:
            ti = 0
        else:
            ti += 1
        hum.display_value(hs[hi])
        if hi >= len(hs) - 1:
            hi = 0
        else:
            hi += 1
        glass.display_value(ws[wi])
        if wi >= len(ws) - 1:
            wi = 0
        else:
            wi += 1

def real_data_run(args):
    temp = thermometer.Thermometer()
    hum = hygrometer.Hygrometer()
    glass = glassofwater.GlassOfWater()

    store = datastore.DataStore()
    reader = serialreader.SerialReader(args.device, args.baudrate,\
                                        store, args.rounds)
    reader.start()
    sleep(8)

    glass.calibrate(zero=float(args.water_zero), \
                            value=float(store.data[args.water_key][args.val]))
    while True:
        sleep(1)
        try:
            t = store.data[args.temperature_key][args.val]
            print("T: " + str(t))
            temp.display_value(float(t))
            h = store.data[args.humidity_key][args.val]
            print("H: " + str(h))
            hum.display_value(float(h))
            w = store.data[args.water_key][args.val]
            print("W: " + str(w))
            glass.display_value(float(w))
            print("-------")
        except KeyError as e:
            # Wait for next iter
            print(e)

    reader.halt()

if __name__ == '__main__':
    """Main CLI function for the demobox0"""

    p = configargparse.ArgumentParser(default_config_files=['/etc/ardu_report/demobox0.vis.config', '~/.ardu_report/demobox0.vis.config', './.demobox0.config'], description="Parse data from the flussbad demobox and display it.\n\n")

    p.add_argument('-b', '--baudrate', default=9600, help='baud rate of the serial line')
    p.add('-c', '--config', required=False, is_config_file=True, help='config file path')
    p.add_argument('-d', '--device', default='/dev/ttyACM0', help='serial device the arduino is connected to')
    p.add_argument('-D', '--demo', action="store_true", help='show a demo run')
#   p.add_argument('-j', '--json_input_schema', help='file path to the JSON schema for the data coming from the sensor device.')
#    p.add_argument('-m', '--meta_input_schema', help='file path to the JSON meta schema for the data coming from the sensor device. This will validate the "--json_input_schema."')
    p.add_argument('-r', '--rounds', type=int, default=0, help='how many times to run the serial listener thread (default: 0 (infinite))')
    p.add_argument('--humidity_key', default='env_humidity', help='id of the air humidity measurement in the input JSON from the serial line')
    p.add_argument('--temperature_key', default='env_temperature', help='id of the temperature measurement in the input JSON from the serial line')
    p.add_argument('--water_key', default='water_distance', help='id of the water distance measurement in the input JSON from the serial line')
    p.add_argument('--water_zero', default='.38', help='correct the first measurement with this value and set it as absolute zero.')
    p.add_argument('--val', default='value', help='name of the value key for each measurement')

    a = p.parse_args()

    if a.demo:
        demo_run(a)
    else:
        real_data_run(a)
