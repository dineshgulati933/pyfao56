from pyfao56.tools import SoilWaterSeries
import pandas as pd

class SoilWaterSeriesDF(SoilWaterSeries):

    def customload(self, df, mdpths, par, sol, mZr=False):
        """
        Load and process soil water data from a DataFrame.

        Args:
            df (pd.DataFrame): Input data with date, depth, and water content.
            mdpths (list): List of depth values for the soil layers.
            par: Soil parameters.
            sol: Solution parameters.
            mZr (bool): Whether to use Zr values from the DataFrame (last column).
        """
        self.df = df.copy()
        self.mdpths = mdpths
        self.par = par
        self.sol = sol
        self.mZr = mZr

        numdpths = len(mdpths)

        # Convert date to YYYY-DOY format and set as index
        self.df['YYYY-DOY'] = pd.to_datetime(self.df.iloc[:, 0], errors='coerce', dayfirst=False).dt.strftime('%Y-%j')
        self.df.set_index('YYYY-DOY', inplace=True)
        self.df.drop(columns=self.df.columns[0], inplace=True)
        
        # Drop rows with NaN in critical columns only
        required_columns = list(range(len(self.mdpths)))  # Columns for soil water contents
        self.df.dropna(subset=self.df.columns[required_columns], inplace=True)


        # Insert depth columns based on mdpths
        for i, v in enumerate(self.mdpths):
            self.df.insert(i, f'dpth{i}', v)

        # Process each SWC profile and add profiles
        for idx, row in self.df.iterrows():
            self._process_profile(idx, row, numdpths)

    def _process_profile(self, idx, row, numdpths):
        """
        Helper method to process a single SWC profile of the DataFrame.

        Args:
            idx: Row index (formatted date).
            row (pd.Series): Row data.
            numdpths (int): Number of soil depths.
        """
        mdate = idx  # Current date (already formatted as index)
        mvswc = {}

        # Collect soil water content at various depths
        for n in range(numdpths):
            try:
                dpth = int(row.iloc[n])  # Depth
                swc = float(row.iloc[n + numdpths])  # Soil water content
                mvswc[dpth] = swc
            except (ValueError, IndexError):
                continue  # Skip invalid entries

        # Extract Zr if available
        try:
            Zr = float(row.iloc[-1]) if self.mZr else float('NaN')  # Last column for Zr
        except (ValueError, IndexError):
            Zr = float('NaN')  # Default to NaN if Zr is missing or invalid

        # Create SoilWaterProfile and add it
        swp = self.SoilWaterProfile(
            mdate,
            mvswc,
            par=self.par,
            sol=self.sol,
            Zr=Zr
        )
        self.addprofile(mdate, swp)



# from pyfao56.tools import SoilWaterSeries
# import pandas as pd

# class SoilWaterSeriesDF(SoilWaterSeries):

#     def customload(self, df, numdpths, par, sol):
#         """
#         Load and process soil water data from a DataFrame.

#         Args:
#             df (pd.DataFrame): Input data with date, depth, and water content.
#             numdpths (int): Number of soil depth layers.
#             par: Soil parameters.
#             sol: Solution parameters.
#         """

#         self.df = df.copy()
#         self.numdpths = numdpths
#         self.par = par
#         self.sol = sol

#         # Convert date to a consistent format and set it as index
#         self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce', dayfirst=False).dt.strftime('%Y-%j')
#         self.df.set_index('date', inplace=True)

#         # Iterate over DataFrame rows
#         for idx, row in self.df.iterrows():
#             mdate = idx  # Current date (already formatted as index)
#             mvswc = {}

#             # Collect soil water content at various depths
#             for n in range(self.numdpths):
#                 try:
#                     dpth = int(row.iloc[n])  # Depth
#                     swc = float(row.iloc[n + self.numdpths])  # Soil water content
#                     mvswc[dpth] = swc
#                 except (ValueError, IndexError):
#                     continue  # Skip invalid entries

#             # Extract Zr if available
#             try:
#                 Zr = float(row.iloc[-1])  # Assuming the last column contains Zr
#             except (ValueError, IndexError):
#                 Zr = float('NaN')  # Default to NaN if Zr is missing or invalid

#             # Create SoilWaterProfile and add it
#             swp = self.SoilWaterProfile(
#                 mdate,
#                 mvswc,
#                 par=self.par,
#                 sol=self.sol,
#                 Zr=Zr
#             )
#             self.addprofile(mdate, swp)