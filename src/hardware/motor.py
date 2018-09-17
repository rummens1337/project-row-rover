class Motor:
    _speedLeft = 0
    _speedRight = 0

    def start(self) -> bool:
        pass

    def stop(self) -> bool:
        pass

    def left(self, v: int) -> bool:
        pass

    def right(self, v: int) -> bool:
        pass

    def status(self) -> dict:
        pass

    def get_speed(self) -> int:
        pass
