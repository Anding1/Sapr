import pandas as pd
import sys

def task1(file_path, row_number, column_number):
    # ������ CSV ���� � DataFrame
    df = pd.read_csv(file_path)

    # ���������, ��� ������ ����� � ������� ��������� � ���������� ��������
    if row_number < 0 or row_number >= len(df):
        print(f"������: ����� ������ {row_number} ��� ���������.")
        return
    if column_number < 0 or column_number >= len(df.columns):
        print(f"������: ����� ������� {column_number} ��� ���������.")
        return

    # �������� �������� ������
    cell_value = df.iat[row_number, column_number]
    print(f"�������� ������ � ������ {row_number + 1}, ������� {column_number + 1}: {cell_value}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("�������������: python script.py <����_�_csv> <�����_������> <�����_�������>")
    else:
        file_path = sys.argv[1]
        row_number = int(sys.argv[2]) - 1  # ����������� � 0-����������
        column_number = int(sys.argv[3]) - 1  # ����������� � 0-����������
        task1(file_path, row_number, column_number)

