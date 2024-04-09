import json
import time
from py.common.globalstuff import get_now_time_str
import  py.common.excel_save_func as ex
def do_excel_save(gs_obj):
        print("Start to Save excel...")
        excel=ex.excel_record(gs_obj)
        ret=excel.start_record()
        if ret == 1:
                print("File does not exist. create an excel file.")
                create_ret=excel.init_excel_file()
                if create_ret == 1:
                        print("Create Fail.")
                        return "{\"ret\":1}"
                else:
                        ret=excel.start_record()
                        if ret == 1:
                                print("Error for open, Excel file already created.")
                                return "{\"ret\":1}"
                        else:
                                print("Create a new excel file OK, Write Excel OK")
                                return "{\"ret\":0}"
        else:   
                print("Excel file exists, save Excel ok.")                     
                return "{\"ret\":0}"