from data.EventEntity import EventEntity


class ObjectDetailsDTO:

    def __init__(self, event: EventEntity = None):
        self.event = event
