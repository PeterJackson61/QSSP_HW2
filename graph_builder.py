import pandas as pd
from data_converter import *
import os
import matplotlib.pyplot as plt
from mystartdefaults import *

show_graph_option = False

def plot_and_save(material_name):
    file_path = output_data+material_name+'_Bands.csv'
    df = pd.read_csv(file_path)
    x_column = df.columns[0]
    y_columns = df.columns[2:18]
    shift = df[df[x_column]<1]['Band_3'].max()
    plt.figure(figsize=(6.8, 6))
    for col in y_columns:
        plt.plot(df[x_column], df[y_columns][col]-shift, label=col)
    plt.title(f'Band structure of ' + material_name, fontsize = 18)
    plt.xlabel('q (2π/a)', fontsize = 16)
    plt.ylabel('Energy eV', fontsize = 16)
    plt.ylim(ylim_dict[material_name])
    # plt.legend()
    plt.margins(x = 0.0, y = 0.0)

    xticks_values = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5]
    xticklabels = ['L', '0.25', 'Γ', '0.25', '0.5', '0.75', 'X', 'K', '0.5', '0.25', 'Γ']
    indices_to_pick = [2, 6, 7]
    selected_elements = [xticks_values[i] for i in indices_to_pick]
    for xtick_val in selected_elements:
        plt.axvline(x = xtick_val, color = 'black', label = 'axvline - full height')

    plt.axhline(y=0, color='black', linestyle='--')
    plt.xticks(xticks_values, xticklabels, fontsize = 14)

    plt.savefig('./Graphs_Simulation/'+material_name + '.png')
    # plt.text(0.5, 0.5, material_name, color='blue', fontsize=15, ha='center', transform=plt.gca().transAxes)
    # plt.show()

material_list = ['Si', 'Ge', 'Sn', 'GaP', 'GaAs', 'AlSb', 
                 'InP', 'GaSb', 'InAs', 'InSb', 'ZnS', 
                 'ZnSe', 'ZnTe', 'CdTe']
ylim_dict = {'Si'  :(-5.5,6.5),
             'Sn'  :(-4,6),
             'ZnS' :(-3,10),
             'ZnSe':(-3,9),
             'ZnTe':(-3,8.5),
             'AlSb':(-4,7),
             'CdTe':(-3.5,8),
             'GaAs':(-4,7),
             'GaP' :(-4,7),
             'GaSb':(-3,6.5),
             'Ge'  :(-5,7),
             'InAs':(-4,7),
             'InP' :(-4,7),
             'InSb':(-3,6),
            }
if len(os.listdir('./Bands_converted_csv/')) == 0:
    data_convert('bands')
    data_convert('fourier')
coeff_output_filenames = os.listdir(output_coeff)
bands_output_filenames = os.listdir(output_data)


for material in material_list:
    print(f"Generating band structure of {material}")
    plot_and_save(material)