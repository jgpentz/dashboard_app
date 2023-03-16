from pymongo import MongoClient
import pandas as pd

# Hopefully we don't care about this being secret for now
FRF_MONGO_USER = "engineering"
FRF_MONGO_PASS = "microwave"
FRF_MONGO_PORT = 27017
FRF_MONGO_HOST = f"mongodb://{FRF_MONGO_USER}:{FRF_MONGO_PASS}@mongodb-test.firstrf.local:{FRF_MONGO_PORT}"

class FailureTypes:
    def __init__(self):
        client = MongoClient(FRF_MONGO_HOST)
        funit_db = client.funit_results
        self.mb13_collection = funit_db.mb13

        self._dataframe = None
        self.data = None

        self.ingest()
        self.dataframe_to_json()


    def ingest(self):
        failure_results = []

        for _, item in enumerate(self.mb13_collection.aggregate([
            {
                '$match': {
                    '$or': [
                        {
                            '$and': [
                                {
                                    'name': 'TestLoadFirmware'
                                }, {
                                    'result': False
                                }
                            ]
                        }, {
                            '$and': [
                                {
                                    'name': 'TestWriteProductInfo'
                                }, {
                                    'result': False
                                }
                            ]
                        }, {
                            '$and': [
                                {
                                    'name': 'TestPost'
                                }, {
                                    'result': False
                                }
                            ]
                        }
                    ]
                }
            }
        ])):
            # Create a list of all failure types
            failure_results.append({"test": item['name']})

        # Fake data
        for i in range(2):
            failure_results.append({"test": "TestLoadFirmware"})

        # Fake data
        for i in range(5):
            failure_results.append({"test": "TestWriteProductInfo"})

        # Group the failure types together
        self._dataframe = pd.DataFrame(failure_results)
        self._dataframe = self._dataframe.groupby(['test']).size()
        self._dataframe = pd.DataFrame({'failures':self._dataframe.values}, index=self._dataframe.index)
        self._dataframe.reset_index(inplace=True)

    def dataframe_to_json(self):
        arr = []

        for element in self._dataframe.to_numpy():
            arr.append({'test': element[0], 'value': element[1]})

        self.data = arr

    def get_data(self):
        return self.data


if __name__ == "__main__":
    ftypes = FailureTypes()
    data = ftypes.get_data()
    print(data)