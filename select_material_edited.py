import pandas

class material:

    def __init__(self, k=398, rho=8970, cp=380, name='material'):

        self.name = name
        self.k, self.rho, self.cp = k, rho, cp
        self.a = k / rho / cp

class material_database:

    def __init__(self, xls='materiais_edited.xls'):

        self.dataframe = pandas.read_excel(xls, index_col='Material')

    def select(self, name):

        try:

            k = self.dataframe.loc[name, 'k']
            rho = self.dataframe.loc[name, 'rho']
            cp = self.dataframe.loc[name, 'cp']
            return material(k, rho, cp, name)

        except KeyError as key:

            print(f'*** KeyError: unknown material ({key}) ***')
            raise

class fluid:
    
    def __init__(self, h=2000, name='fluid'):
        self.name = name
        self.h = h

class fluid_database:

    def __init__(self, xls='materiais_edited.xls'):

        self.dataframe = pandas.read_excel(xls, index_col='Fluid')

    def select(self, name):
        
        try:
            h = self.dataframe.loc[name, 'h']
            return fluid(h, name)

        except KeyError as key:

            print(f'*** KeyError: unknown fluid ({key}) ***')

            raise
