from myCsvParser import myCsvParser


class dataReader():
    @classmethod
    def create_dataset(self,path, ignoreColumn=[], hasHeader=False, removeHeader=False):
        p = myCsvParser()
        data = p.getData(path)
        tempHeader = data[0] if hasHeader and not removeHeader else None

        if hasHeader:
            data.pop(0)
        for row in data:
            for item in ignoreColumn:
                row.pop(item)

        import random
        random.shuffle(data)
        # random.seed(997)
        length = len(data)
        train_length = int(round(length * 1/3))
        test_length = length - train_length
        train_data = data[train_length:]
        test_data = data[-test_length:]

        if hasHeader and not removeHeader:
            train_data.insert(0, tempHeader)

        return (train_data, test_data)

    @classmethod
    def read_data(self,path, ignore_columns=[]):
        p = myCsvParser()
        data = p.getData(path, ignore_items=ignore_columns, is_set=True)

        import random
        random.seed(10)
        random.shuffle(data)
        data = data[:12000]
        return data