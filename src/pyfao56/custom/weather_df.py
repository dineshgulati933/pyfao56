from pyfao56 import Weather
import pandas as pd

class WeatherDF(Weather):

    def customload(self, df, z, lat, wndht):
        self.df = df.copy()
        self.z = z
        self.lat = lat
        self.wndht = wndht

        self.df['Date'] = pd.to_datetime(self.df['Date'], dayfirst=False).dt.strftime('%Y-%j')
        self.df.set_index('Date', inplace=True)

        self.wdata = self.df
        self.wdata.index.name = None
        self.wdata.columns = self.cnames
