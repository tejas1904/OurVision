from time import sleep
from state import State

class Test:
    # Cycle test
    @classmethod
    def cycleTest(cls, handler):
        print(f"Currently in {State.name(handler.state)} mode")
        print("Cycle once")
        handler.cycle()

    # Select and Cancel test
    @classmethod
    def selectAndCancelTest(cls, handler):
        print(f"Started {State.name(handler.state)} process")
        handler.select()
        sleep(1)
        handler.cancel()
        print("Cycle once")
        handler.cycle()