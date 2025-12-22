from pathlib import Path
import pandas as pd


class ExcelLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        try:
            if not self.file_path.exists():
                raise FileNotFoundError

            # Cuts out those annoying rows given by Excel exports
            df = pd.read_excel(self.file_path, header=11)
            df = df.iloc[:, 1:]
            df = df.iloc[10:, :]

            if df.empty:
                raise ValueError

            return df

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")

        except ValueError:
            raise ValueError("Loaded Excel file is empty")

        except Exception as e:
            raise RuntimeError(f"Failed to load Excel file: {e}")


if __name__ == "__main__":
    loader = ExcelLoader("samples/sales-2.xlsx")
    df = loader.load()
    print(df.head())
