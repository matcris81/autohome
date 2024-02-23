class ACSettings:
    def __init__(self, power="Off", mode="Auto", temperature=25, fan_speed="Auto", swing_vertical="Auto",
                 swing_horizontal="Auto", quiet="Off", powerful="Off", ion="Off", clock=None, on_timer=None, off_timer=None):
        self.power = power
        self.mode = mode
        self.temperature = temperature
        self.fan_speed = fan_speed
        self.swing_vertical = swing_vertical
        self.swing_horizontal = swing_horizontal
        self.quiet = quiet
        self.powerful = powerful
        self.ion = ion
        self.clock = clock
        self.on_timer = on_timer
        self.off_timer = off_timer