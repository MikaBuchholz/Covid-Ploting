from numpy.lib.arraysetops import unique
import pandas as pd
import os
import matplotlib.pyplot as plt
from typing import List, Union, NoReturn
import random

class CoronaVisual():
    def __init__(self) -> None:
        self.data: List[str] = [file for file in os.listdir('data')]
    
    def concatData(self) -> NoReturn:
        combinedDF: object = pd.DataFrame()

        for file in self.data:
            newDF: object = pd.read_csv(f'data/{file}')
            combinedDF: object = pd.concat([combinedDF, newDF], axis = 1)
        
        combinedDF.to_csv('italyProvAndReg.csv', index = False)
    
    def getSummedDataPerColumn(self, column: str, dataset: int = 0) -> object:
        dataframe: object = pd.read_csv(f'data/{self.data[dataset]}')
        return dataframe.groupby(column).sum().sort_values(column)
    
    def getUniqueColumnNames(self, column: str, dataset: int = 0) -> List[str]:
        dataframe: object = pd.read_csv(f'data/{self.data[dataset]}')
        return sorted(dataframe[column].unique())

    def getColumns(self, dataset: int = 0) -> List[str]:
        dataframe: object = pd.read_csv(f'data/{self.data[dataset]}')

        return sorted(dataframe.columns)
    
    def getRandomColor(self):
        colors: List[str] = ['r', 'y', 'g', 'b', 'c', 'm']
        
        return random.choice(colors)

    def createMonthCell(self, dataset: int = 1) -> NoReturn:
        dataframe: object = pd.read_csv(f'data/{self.data[dataset]}')
    
        if 'Month' not in dataframe.columns:
            dataframe['Month'] = dataframe['Date'].apply(lambda x: x.split('-')[1])
            dataframe.to_csv(f'data/{self.data[dataset]}', index = None)

    def plotMultipleData(self, uniques: str, data: List[List[Union[object, bool, str]]],size = 8, rotation = 90, yLabel: str = 'Empty', xLabel: str = 'Empty', title = 'Data') -> NoReturn:
        colors: List[str] = ['r', 'y', 'g', 'b', 'c', 'm']
        usedColors: List[str] = []
        #True -> Bar | False -> Plot
        plt.figure(title, figsize = (15, 9), tight_layout = True)
        
        for index in range(len(data)):
            if data[index][1] == True:
                plt.bar(uniques, data[index][0], label = data[index][2])
            
            if data[index][1] == False:
                color = self.getRandomColor()
                if color not in usedColors:
                    usedColors.append(colors)
                
                else:
                    color: str = self.getRandomColor()

                plt.plot(uniques, data[index][0], f'{color}8-', label = data[index][2])
        
        plt.xticks(uniques, size = size, rotation = rotation)
        plt.legend()

        plt.ylabel(yLabel)
        plt.xlabel(xLabel)
    
        plt.show()

    def plotCase1(self) -> NoReturn:
        # Plot all active cases per region in Italy
        totalDataSummed: object = self.getSummedDataPerColumn('RegionName', dataset = 1)
        uniqueRegions: object = self.getUniqueColumnNames('RegionName', dataset = 1)

        totalCases: object = totalDataSummed['CurrentPositiveCases']
        self.plotMultipleData(uniqueRegions, [[totalCases, True, 'Current Cases']], title = 'Cases in Italy', yLabel = 'Cases in million', xLabel = 'Regions')

    def plotCase2(self) -> NoReturn:
        # Plot deaths relative to active cases
        totalDataSummed: object = self.getSummedDataPerColumn('RegionName', dataset = 1)
        uniqueRegions: object = self.getUniqueColumnNames('RegionName', dataset = 1)

        totalCases: object = totalDataSummed['CurrentPositiveCases']
        deaths: object = totalDataSummed['Deaths']

        self.plotMultipleData(uniqueRegions, [[totalCases, True, 'Total Current Cases'], [deaths, False, 'Deaths']], title = 'Death-Case-Relation',
                            yLabel = 'Cases in million', xLabel = 'Regions')

    def plotCase3(self) -> NoReturn:
        # Plot recovered vs deaths, in relation to the month
        self.createMonthCell()
  
        totalDataSummed: object = self.getSummedDataPerColumn('Month', dataset = 1)
      
        months: List[int] = range(2, 13)
 
        recoveredCases: object = totalDataSummed['Recovered']
        deaths: object = totalDataSummed['CurrentPositiveCases']

        self.plotMultipleData(months, [[recoveredCases, False, 'Recovered'], [deaths, False, 'Current Cases']], title = 'Recovered-Deaths-Rate',
                            yLabel = 'Population', xLabel = 'Month', rotation = 0)
    
    def plotCase4(self) -> NoReturn:
        # Plot deaths in relation to hospital patients in relation ICU patients, per month, compared to all cases
        self.createMonthCell()

        totalDataSummed: object = self.getSummedDataPerColumn('Month', dataset = 1)

        months: List[int] = range(2, 13)

        allCases: object = totalDataSummed['CurrentPositiveCases']
        inHospital: object = totalDataSummed['TotalHospitalizedPatients']
        inICU: object = totalDataSummed['IntensiveCarePatients']
        deaths: object = totalDataSummed['Deaths']

        self.plotMultipleData(months, [[allCases, True, 'Current Cases'], [inHospital, False, 'Currently in Hospital'], [inICU, False, 'In ICU'], 
                            [deaths, False, 'Deaths']], title = 'Comparrison', yLabel = 'Cases', xLabel = 'Months')

    def plotCase5(self):
        # Plot cases in relation to home confinement, per region
        totalDataSummed: object = self.getSummedDataPerColumn('RegionName', dataset = 1)

        homeConfinementData: object = totalDataSummed['HomeConfinement']
        allCases: object = totalDataSummed['CurrentPositiveCases']
        uniqueRegions: object = self.getUniqueColumnNames('RegionName', dataset = 1)

        self.plotMultipleData(uniqueRegions, [[homeConfinementData, False, 'In Home Confinement'], [allCases, True, 'Current Cases']], yLabel = 'Current Cases (Million)', xLabel = 'Regions', 
                                title= 'Home Confinement In Relation To Cases', rotation = 45)



if __name__ == '__main__':
    corona = CoronaVisual()
    corona.plotCase5()


"""
 'SNo', 'Date', 'Country', 'RegionCode', 'RegionName', 'Latitude',
       'Longitude', 'HospitalizedPatients', 'IntensiveCarePatients',
       'TotalHospitalizedPatients', 'HomeConfinement', 'CurrentPositiveCases',
       'NewPositiveCases', 'Recovered', 'Deaths', 'TotalPositiveCases',
       'TestsPerformed', 'Month'],
      dtype='object'
"""