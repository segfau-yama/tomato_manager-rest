def get_red_data(self):
    # Read each color register.
    r = self._readU16LE(TCS34725_RDATAL)
    # Delay for the integration time to allow for next reading immediately.
    time.sleep(INTEGRATION_TIME_DELAY[self._integration_time])
    return r
