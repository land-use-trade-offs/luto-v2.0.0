
import shutil
import pandas as pd
from glob import glob


from tools.helper_func import add_data_2_html


####################################################
#         setting up working variables             #
####################################################

# setting up working directory to root dir
if  __name__ == '__main__':
    os.chdir('../../..')

# Get the output directory
with open('output/working_dir.txt') as f:
    RAW_DATA_ROOT = os.path.abspath(f.readline().strip())
    RAW_DATA_ROOT = os.path.normpath(RAW_DATA_ROOT).replace("\\", "/")

# Set the save directory    
REPORT_DIR = f'{RAW_DATA_ROOT}/DATA_REPORT'
if not os.path.exists(REPORT_DIR):
    raise Exception(f"Report directory not found: {REPORT_DIR}")
    


####################################################
#        Copy report html to the REPORT_DIR        #
####################################################  

shutil.copytree('luto/tools/report/tools/tempelate_html', 
                f'{REPORT_DIR}/REPORT_HTML',
                dirs_exist_ok=True)


####################################################
#                Write data to HTML                #
####################################################  

# Get all html files needs data insertion
html_df = pd.DataFrame([['production',f"{REPORT_DIR}/REPORT_HTML/pages/production_profit.html"],
                        ["area",f"{REPORT_DIR}/REPORT_HTML/pages/area_change.html"],
                        ["GHG",f"{REPORT_DIR}/REPORT_HTML/pages/GHG Emmisions.html"],
                        ["water",f"{REPORT_DIR}/REPORT_HTML/pages/water_usage.html"]])

html_df.columns = ['name','path']

# Get all data files
all_data_files = glob(f"{REPORT_DIR}/data/*")
# # Exclude html files
# all_data_files = [i for i in all_data_files if 'html' not in i]

# Add data path to html_df
html_df['data_path'] = html_df.apply(lambda x: [i for i in all_data_files if x['name'] in i ],axis=1)


# Parse html files
for idx,row in html_df.iterrows():
    
    html_path = row['path']
    data_pathes  = row['data_path']

    # Add data to html
    add_data_2_html(html_path,data_pathes)