
from File_Package.sj_file_system import CsvManager
import os

csv_m = CsvManager(os.getcwd(), "ANIMAL_INS")
csv_m.write_header(["ANIMAL_ID", "ANIMAL_TYPE", "DATETIME"])
csv_m.write_row([1, "Dog", '2020-10-14 15:38:00'])
csv_m.write_row([2, "Dog", '2020-10-23 11:42:00'])
csv_m.write_row([3, "Dog",'2020-11-03 15:04:00'])
csv_m.write_row([4, "Dog", '2020-11-18 17:03:00'])
csv_m.write_row([5, "Iguana", '2021-01-18 13:00:00'])
csv_m.write_row([6, "Snake", '2021-03-18 12:00:00'])
csv_m.write_row([7, "Dog", '2021-03-18 09:03:00'])
csv_m.write_row([8, "Iguana", '2021-03-31 09:00:00'])
csv_m.write_row([9, "Dog", '2021-03-21 09:00:00'])

csv_m = CsvManager(os.getcwd(), "ANIMAL_INFO")
csv_m.write_header(["ANIMAL_ID", "INTAKE_CONDITION", "ANIMAL_NAME", "SEX_UPON_INTAKE"])
csv_m.write_row([1, 'Normal', 'Jack', 'Neutered Male'])
csv_m.write_row([2, 'Normal', 'Disciple', 'Intact Male'])
csv_m.write_row([3, 'Normal', 'Katie', 'Spayed Female'])
csv_m.write_row([4, 'Normal', 'Anna', 'Spayed Female'])
csv_m.write_row([5, 'Wounded', 'Cherry', 'Intact Male'])
csv_m.write_row([6, 'Normal', 'Abo', 'Intact FeMale'])
csv_m.write_row([7, 'Normal', 'Perry', 'Intact FeMale'])
csv_m.write_row([8, 'Wounded', 'Uri', 'Intact FeMale'])
csv_m.write_row([9, 'Normal', 'Sun', 'Neutered Male'])