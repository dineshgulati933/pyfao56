from pyfao56.tools import SoilWaterSeries
import pandas as pd

class SoilWaterSeriesDF(SoilWaterSeries):


    def customload(self,df,numdpths,par,sol):
        self.df = df.copy()
        self.numdpths = numdpths
        self.par = par
        self.sol = sol

        self.df['date'] = pd.to_datetime(self.df['date'], dayfirst=False).dt.strftime('%Y-%j')
        self.df.set_index('date', inplace=True)

        for idx in df.index:
            mdate = idx
            mvswc = dict()
            for n in range(self.numdpths):
                dpth = int(df.iloc[idx,n+1])
                swc = float(df.iloc[idx,(n+self.numdpths+1)])
                mvswc.update({dpth:swc})
            try:
                Zr = float(df.iloc[idx,-1])
            except:
                Zr = float('NaN')

            swp = self.SoilWaterProfile(mdate,
                                mvswc,
                                par = self.par,
                                sol = self.sol,
                                Zr = Zr)
            self.addprofile(mdate,swp)