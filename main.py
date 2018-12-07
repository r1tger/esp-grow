#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo_pixel import NeoPixel
from ntp import NTPClient
from machine import Pin, reset
from utime import sleep

# NeoPixel constants
NEO_NUM_LEDS = 21                       # Number of LEDs
NEO_ON_COLOUR = (255, 0, 255)           # RGB start
NEO_OFF_COLOUR = (0, 0, 0)              # RGB off


class ESPGrow:
    """ """
    DELAY = 59

    def __init__(self):
        """ """
        print('ESPGrow::__init__()')

        # Interface to NeoPixels string
        self.pixels = NeoPixel(Pin(12, Pin.OUT), NEO_NUM_LEDS)
        # Retrieve the current time by NTP
        self.ntp = NTPClient()
        self.ntp.set_time()

    def run(self):
        """ ESPGrow main loop.
        """
        print('ESPGrow::run()')

        try:
            # Set a starting color
            print('ESPGrow::run(): Set default colour')
            self.set_color(NEO_ON_COLOUR)

            while True:
                # Get the current time (tuple)
                local_time = NTPClient.cet_time()
                hour = local_time[3]
                # Set lights based on current time
                colour = NEO_OFF_COLOUR if hour in [0, 1] else NEO_ON_COLOUR
                print('ESPGrow::run(): Hour: {h} {c}'.format(h=hour, c=colour))
                # Set colour
                self.set_color(colour)
                # Wait
                sleep(self.DELAY)
        finally:
            print('ESPGrow::run(): Giving up')

    def set_color(self, color):
        """ Set the color for the pixels

        :param color: Tuple with rgb color
        """
        self.pixels.fill_rgb(color)
        self.pixels.write()


def main(debug=False):
    """ Main entry point. """
    esp_grow = ESPGrow()

    # Start main loop
    esp_grow.run()


if __name__ == '__main__':
    # Run the main loop
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('main(): Caught exception: {e}'.format(e=e))
        # Try resetting if an unhandled exception is caught
        reset()
