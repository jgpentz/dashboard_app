from pathlib import Path
import os
import rftools as rf
import pandas as pd
import glob

class GainProcessor:
    def __init__(self):
        self._dataframes = {
            "rx_br": pd.DataFrame(),
            "rx2_br": pd.DataFrame(),
            "rx_fw": pd.DataFrame(),
            "rx2_fw": pd.DataFrame(),
            "tx_br": pd.DataFrame(),
            "tx_fw": pd.DataFrame(),
        }

        self.json_data = None
        self.location = "D:\FRF-35600_Gogo_MBC\Production\data\FRF-51191_AntennaCardPrimary/*"
        self.ingest()


    def ingest(self):
        sn_dirs = glob.glob(self.location)
        gain_paths = []
        print("Attempting to pull data from directories...")
        for sn in sn_dirs:
            if int(Path(sn).name) >= 22193318:
                try:
                    test_dirs = glob.glob(str(sn) + r"\01_atp_primary\*")
                    test_dir = test_dirs[len(test_dirs) - 1]
                    test_file = test_dir + r"\test_rf_gain.frd.bz2"
                    gain_paths.append(Path(test_dir + r"\test_rf_gain.frd.bz2").resolve(strict=True))
                except FileNotFoundError as e:
                    #print(e)
                    pass
                except Exception as e:
                    #print(e)
                    pass
        print("Finished pulling data")

        gain_paths = gain_paths[1:10]
        for path in gain_paths:
            # Store the data
            da = rf.frd2xarray(path)

            # Convert complex voltage to db (coords are: trm x mode x freq)
            da[:][:][:] = rf.db20(da[:][:][:])
            da = da.real

            # Convert to dataframe for plotting, remove unnecessary columns
            df = da.to_dataframe()
            df = df.drop(columns=['power', 'temperature'])
            df = df.reset_index()
            df = df.rename(columns={'noname': 'db'})

            # Gather only the s21 data
            mask_rx_broadside = (
                (df['mode'] == "rx") &
                ((df['frequency'] > 2.429e9) & (df['frequency'] <= 2.495e9)) &
                ((df['m'] == 1) & (df['n'] == 2)) &
                (df['trm'] <= 4))

            mask_rx_fwd = (
                (df['mode'] == "rx") &
                ((df['frequency'] > 2.425e9) & (df['frequency'] <= 2.495e9)) &
                ((df['m'] == 1) & (df['n'] == 2)) &
                (df['trm'] > 4))

            mask_rx2_broadside = (
                (df['mode'] == "rx2") &
                ((df['frequency'] > 2.429e9) & (df['frequency'] <= 2.495e9)) &
                ((df['m'] == 1) & (df['n'] == 2)) &
                (df['trm'] <= 4))

            mask_rx2_fwd = (
                (df['mode'] == "rx2") &
                ((df['frequency'] > 2.425e9) & (df['frequency'] <= 2.495e9)) &
                ((df['m'] == 1) & (df['n'] == 2)) &
                (df['trm'] > 4))

            mask_tx_broadside = (
                (df['mode'] == "tx") &
                ((df['frequency'] > 2.429e9) & (df['frequency'] <= 2.465e9)) &
                ((df['m'] == 2) & (df['n'] == 1)) &
                (df['trm'] <= 4))

            mask_tx_fwd = (
                (df['mode'] == "tx") &
                ((df['frequency'] > 2.429e9) & (df['frequency'] <= 2.465e9)) &
                ((df['m'] == 2) & (df['n'] == 1)) &
                (df['trm'] > 4))

            # Add a date for sorting data by week
            df['date'] = pd.to_datetime(da.date)

            # Concat the new dataframe to the main dataframes used
            self._dataframes['rx_br'] = pd.concat([self._dataframes['rx_br'], df.loc[mask_rx_broadside]])
            self._dataframes['rx_br'].set_index('date')

            self._dataframes['rx_fw'] = pd.concat([self._dataframes['rx_fw'], df.loc[mask_rx_fwd]])
            self._dataframes['rx_fw'].set_index('date')

            self._dataframes['rx2_br'] = pd.concat([self._dataframes['rx2_br'], df.loc[mask_rx2_broadside]])
            self._dataframes['rx2_br'].set_index('date')

            self._dataframes['rx2_fw'] = pd.concat([self._dataframes['rx2_fw'], df.loc[mask_rx2_fwd]])
            self._dataframes['rx2_fw'].set_index('date')

            self._dataframes['tx_br'] = pd.concat([self._dataframes['tx_br'], df.loc[mask_tx_broadside]])
            self._dataframes['tx_br'].set_index('date')

            self._dataframes['tx_fw'] = pd.concat([self._dataframes['tx_fw'], df.loc[mask_tx_fwd]])
            self._dataframes['tx_fw'].set_index('date')


        self._dataframes['rx_br'] = self._dataframes['rx_br'].sort_values('date')
        self._dataframes['tx_fw'] = self._dataframes['tx_fw'].sort_values('date')
        self._dataframes['rx_fw'] = self._dataframes['rx_fw'].sort_values('date')
        self._dataframes['rx2_br'] = self._dataframes['rx2_br'].sort_values('date')
        self._dataframes['tx_br'] = self._dataframes['tx_br'].sort_values('date')
        self._dataframes['rx2_fw'] = self._dataframes['rx2_fw'].sort_values('date')

        self._dataframes['rx_br']['date'] = pd.to_datetime(self._dataframes['rx_br']['date'], utc=True)
        self._dataframes['rx_br']['week'] = (self._dataframes['rx_br'].apply(lambda x: self.to_calendar(x['date']), axis=1))
        self._dataframes['rx_br'] = self._dataframes['rx_br'][self._dataframes['rx_br']['week'].isin((self._dataframes['rx_br']['week'].unique())[-4:])]

        self._dataframes['rx_fw']['date'] = pd.to_datetime(self._dataframes['rx_fw']['date'], utc=True)
        self._dataframes['rx_fw']['week'] = (self._dataframes['rx_fw'].apply(lambda x: self.to_calendar(x['date']), axis=1))
        self._dataframes['rx_fw'] = self._dataframes['rx_fw'][self._dataframes['rx_fw']['week'].isin((self._dataframes['rx_fw']['week'].unique())[-4:])]

        self._dataframes['rx2_br']['date'] = pd.to_datetime(self._dataframes['rx2_br']['date'], utc=True)
        self._dataframes['rx2_br']['week'] = (self._dataframes['rx2_br'].apply(lambda x: self.to_calendar(x['date']), axis=1))
        self._dataframes['rx2_br'] = self._dataframes['rx2_br'][self._dataframes['rx2_br']['week'].isin((self._dataframes['rx2_br']['week'].unique())[-4:])]

        self._dataframes['rx2_fw']['date'] = pd.to_datetime(self._dataframes['rx2_fw']['date'], utc=True)
        self._dataframes['rx2_fw']['week'] = (self._dataframes['rx2_fw'].apply(lambda x: self.to_calendar(x['date']), axis=1))
        self._dataframes['rx2_fw'] = self._dataframes['rx2_fw'][self._dataframes['rx2_fw']['week'].isin((self._dataframes['rx2_fw']['week'].unique())[-4:])]

        self._dataframes['tx_br']['date'] = pd.to_datetime(self._dataframes['tx_br']['date'], utc=True)
        self._dataframes['tx_br']['week'] = (self._dataframes['tx_br'].apply(lambda x: self.to_calendar(x['date']), axis=1))
        self._dataframes['tx_br'] = self._dataframes['tx_br'][self._dataframes['tx_br']['week'].isin((self._dataframes['tx_br']['week'].unique())[-4:])]

        self._dataframes['tx_fw']['date'] = pd.to_datetime(self._dataframes['tx_fw']['date'], utc=True)
        self._dataframes['tx_fw']['week'] = (self._dataframes['tx_fw'].apply(lambda x: self.to_calendar(x['date']), axis=1))
        self._dataframes['tx_fw'] = self._dataframes['tx_fw'][self._dataframes['tx_fw']['week'].isin((self._dataframes['tx_fw']['week'].unique())[-4:])]

        self.drop_columns()

        self.dataframe_to_json()

    def to_calendar(self, d):
        return d.isocalendar()[1]  # the 2nd index of the tuple is the 'week'

    def drop_columns(self):
        for key, value in self._dataframes.items():
            value.drop(['date','trm', 'mode', 'm', 'n', 'frequency'], axis=1, inplace=True)
            value.reset_index(drop=True,  inplace=True)

    def dataframe_to_json(self):
        obj = {}

        for key, value in self._dataframes.items():
            tmp_arr = []
            for element in value.to_numpy():
                tmp_arr.append({
                    "week": element[1],
                    "gain": element[0]
                })

            obj[key] = tmp_arr

        self.json_data = obj




    def get_dataframes(self):
        return self.json_data

if __name__ == "__main__":
    gainprocessor = GainProcessor()
    dfs = gainprocessor.get_dataframes()
    # print(dfs)