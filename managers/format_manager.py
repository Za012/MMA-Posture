# This Python file uses the following encoding: utf-8
import numpy as np
import pandas as pd


class FormatManager:

    @staticmethod
    def format_dataset(data_file, path=True):

        dataset = []
        count = 0

        if path is True:
            data = [pd.read_csv(data_file).values]
        else:
            data = data_file

        for pose in data:
            for row in pose:
                dataset.append([])  # Person (useless dimension, but needed to get 4d)
                personCount = 0
                for person in range(1):
                    dataset[count].append([])  # Frame (This is the actual keypoint array (aka 1 row in the excel))
                    for cell in row:  # The cell is a string (aka xyc) so we'll split by comma and format each number we get
                        if cell == "0":
                            cell = "0,0,0"
                        if type(cell) != float:
                            buffer = cell.split(',')
                            array = np.empty(shape=len(buffer))  # Was necessary due to it being a float or something
                            i = 0
                            for number in buffer:
                                array[i] = float(number)
                                i += 1
                            # print(array)
                            dataset[count][personCount].append(array)  # Put it in the main dataset
                    personCount += 1
                count += 1

        return np.array(dataset)  # Parse it into a numpy array and return!
        # (It was a Python array in the beginning)
        # Reason why it's like this is due to the 'efficency' of numpy arrays makes them not able to
        # have data appended to them, the size of the array has to be known.
        # But Python array is easier to work with in this case
