import pandas as pd
import os


class DataFeriado:
    def __init__(self, module_dir:str = None) -> None:
        self.module_dir = module_dir or os.path.dirname(os.path.abspath(__file__))

    def feriados_sp(self) -> list:
        path = f"{self.module_dir}/files/feriados_sp.xlsx"
        df = pd.read_excel(path)
        df["Data"] = pd.to_datetime(df["Data"]).apply(lambda x: x.date())
        dates = df.Data.values.tolist()
        return dates

    def feriados_br(self) -> list:
        path = f"{self.module_dir}/files/feriados_br.xlsx"
        df = pd.read_excel(path)
        df["Data"] = pd.to_datetime(df["Data"]).apply(lambda x: x.date())
        dates = df.Data.values.tolist()
        return dates
    
    def feriados_di(self) -> list:
        path = f"{self.module_dir}/files/feriados_di.xlsx"
        df = pd.read_excel(path)
        df["Data"] = pd.to_datetime(df["Data"]).apply(lambda x: x.date())
        dates = df.Data.values.tolist()
        return dates

    def feriados_nyse(self) -> list:
        path = f"{self.module_dir}/files/feriados_nyse.xlsx"
        df = pd.read_excel(path)
        df["Data"] = pd.to_datetime(df["Data"]).apply(lambda x: x.date())
        dates = df.Data.values.tolist()
        return dates
