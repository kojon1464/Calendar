from pandas import DataFrame


class Statistics:
    data_frame: DataFrame
    title: str

    def __init__(self, data_frame, title):
        self.data_frame = data_frame
        self.title = title
