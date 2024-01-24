import numpy as np
import pandas as pd
import os

bands_path = './Bands_data_dat/'
fourier_coeff_path = './Coeff_Fourier/'
output_data = './Bands_converted_csv/'
output_coeff = './Coeff_converted_csv/'

fourier_file_names = os.listdir(fourier_coeff_path)
bands_file_names = os.listdir(bands_path)

def data_convert(type_file):
        file_path = fourier_coeff_path
        if 'bands' in type_file:
            type_file = 'bands' 
            file_path = bands_path
            file_names = os.listdir(file_path)
        file_names = os.listdir(file_path)
        for name in file_names:
            filename=file_path+name
            name_file_csv = name.split('.')[0] + '.csv'
            data = []
            print(f'Converting dat files to csv file of datafile {name}')
            with open(filename, 'r') as f:
                if type_file == 'fourier':
                    f.readline()
                    f.readline()
                # Read and process lines until there are no more lines left
                while True:
                    line = f.readline().strip()
                    if not line:  # Break the loop if there are no more lines
                        break
                    line_to_data = line.split(' ')
                    temp = []
                    for element in line_to_data:
                        if element != '':
                            temp.append(element)
                    data.append(temp)
                f.close()
                
                if type_file == 'fourier':
                    df = pd.DataFrame(data)
                    df.to_csv(output_coeff + name_file_csv, index=False, header=False)
                else:
                    column_names = ['Linear Coordinates', 'Reciprocal Lattice']
                    for i in range(len(data[0])-2):
                        column_band_names = f'Band_{i+1}'
                        column_names.append(column_band_names)
                    # print(column_names)
                    df = pd.DataFrame(data)
                    df.columns = column_names
                    df.to_csv(output_data + name_file_csv, index=False)
        print("File conversion to csv completed")
data_convert('bands')
data_convert('fourier')