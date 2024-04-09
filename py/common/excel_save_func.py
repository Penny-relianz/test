# -*- coding: UTF-8 -*-
import xlwings as xw
#import openpyxl
import datetime
import json
import os,sys
from py.common.globalstuff import transfer_string_from_iso88591_to_utf8
def get_cell_index(row,col_idx):
    #col=A B C.... AA AB AC... BA BB BC...
    
    try:
        col_idx=int(col_idx)
        row=str(row)
    except:
        pass
    if col_idx <= 26:
        ret=chr(col_idx+64)+row
    else:
        first_chr=chr(int(col_idx/26)+64)
        last_chr=chr(col_idx%26+64)
        ret=first_chr+last_chr+row
    #print("row:%s col:%d =%s"%(row,col_idx,ret))
    return ret #Example: A1 B2 C3 AA1 AA10 AA12  string
class excel_record():
    def __init__(self,gs):
        self.sheetsname=["被摸","將數","放槍","胡牌","自摸","點數"]
        self.filepath=r'D:\Dropbox\python\venv\autosave.xlsx'
        self.gs=gs
        for player in list(self.gs['player_today_record']):
            tmp=transfer_string_from_iso88591_to_utf8(player)
            self.gs['player_today_record'][tmp]=self.gs['player_today_record'][player]
            self.gs['player_today_record'][tmp]['name']=tmp
            del self.gs['player_today_record'][player]
    def start_record(self):
        print("Start start_record.")
        if os.path.exists(self.filepath):
            print("open %s"%self.filepath)
            self.open_excel_file()
            self.record_all()
            self.close_excel()
            return 0
        else:
            print("No excel file exist.")
            return 1
    def init_excel_file(self):
        try:
            if not os.path.exists(self.filepath):
                self.wb = xw.Book()
                self.init_sheet()
                self.get_sheets()
                self.init_cell_title()
                self.close_excel()
                print("Create Excel Done.")
        except:
            print("Create Excel Fail.")
            return 1    
        return 0
    def init_sheet(self):
        for s in self.sheetsname:
            self.wb.sheets.add(s) 
        for sheet in self.wb.sheets:
            if 'Sheet' in sheet.name: 
                sheet.delete()
    def init_cell_title(self):
        for s in self.sheets:
            s.range('A1').value='Check'
            s.range('B1').value='Date'
            s.range('B2').value='Total'
            s.range('B1').api.ColumnWidth=15
            s.range('A1:BZ1').api.Font.bold=True
            s.range('A2:BZ2').api.Font.bold=True
            s.range('A1:BZ1000').api.HorizontalAlignment=-4108#置中
            
            s.range('A1:BZ1').color=(253,233,217)#color
            s.range('A1:BZ1').api.Borders(9).LineStyle=1
            s.range('A1:BZ1').api.Borders(11).LineStyle=1
            
            s.range('A2:BZ2').color=(184,204,228)#color
            s.range('A2:BZ2').api.Borders(9).LineStyle=1
            s.range('A2:BZ2').api.Borders(11).LineStyle=1
    def get_sheets(self):
        self.sheets=[]
        for s in self.sheetsname:
            self.sheets.append(self.wb.sheets[s])
        print (self.sheets)
    def open_excel_file(self):
        print("Start open_excel_file.")
        #self.wb = self.app.books.open(self.filepath)
        self.wb = xw.Book(self.filepath)
        self.get_sheets()
        self.get_last_row()
        self.create_date()
        self.get_cell_idx_of_player()
        self.record_all()
        self.close_excel() 
    def close_excel(self):
        print("Start close_excel.")
        try:
            
            self.wb.save(self.filepath)
            self.wb.app.quit()
            self.wb.close()
            
            #self.app.quit()
            #self.app.kill()
        except:
            pass
    def get_last_row(self):
        self.mainsht=self.wb.sheets['點數']
        self.last_row=str(int(self.mainsht.range("B1").end('down').row)+1)
        print("self.last_row:%s"%(self.last_row))
    def create_date(self):
        d=datetime.datetime.now()
        for s in self.sheets:
            s.range('B'+self.last_row).value=d
    def get_cell_idx_of_player(self):
        self.cell_idx={}
        sht=self.wb.sheets['點數']
       # print(self.gs)
        print(json.dumps(self.gs, indent=4))
        for player in self.gs['player_today_record']:
            #player=transfer_string_from_iso88591_to_utf8(player)
            try:

                self.cell_idx[player]=get_cell_index(self.last_row,sht.range('A1:BZ1').value.index(player)+1)
            except:
                for sht in self.sheets:
                    self.append_new_player(sht,player)
                self.cell_idx[player]=get_cell_index(self.last_row,sht.range('A1:BZ1').value.index(player)+1)
        print (self.cell_idx)
    def append_new_player(self,sht,player):
        #print (sht.cells_last_cell.row)
        name_cell=get_cell_index(1,sht.range("A1").end('right').column+1)
        sht.range(name_cell).value=player
        col=''.join([i for i in name_cell if not i.isdigit()])
        sht.range(get_cell_index(2,sht.range("A1").end('right').column)).formula='=SUM('+col+'3:'+col+'10000)'
    def record_all(self):
        print("Start record_all.")
        print(self.cell_idx)
        try:
            self.record_point()
            self.record_jiang()
            self.record_zhmo()
            self.record_gun()
            self.record_hu()
            self.record_bai_mo()
        except Exception as e:
            #print(e)
            pass
    def record_point(self):
        sht=self.wb.sheets['點數']
        for player,cell in self.cell_idx.items():
            sht.range(cell).value=self.gs['player_today_record'][player]['point']
    def record_jiang(self):
        sht=self.wb.sheets['將數']
        for player,cell in self.cell_idx.items():
            sht.range(cell).value=self.gs['player_today_record'][player]['playjiang']
    def record_zhmo(self):
        sht=self.wb.sheets['自摸']
        for player,cell in self.cell_idx.items():
            sht.range(cell).value=self.gs['player_today_record'][player]['zhmo']
    def record_gun(self):
        sht=self.wb.sheets['放槍']
        for player,cell in self.cell_idx.items():
            sht.range(cell).value=self.gs['player_today_record'][player]['gun']
    def record_hu(self):
        sht=self.wb.sheets['胡牌']
        for player,cell in self.cell_idx.items():
            sht.range(cell).value=self.gs['player_today_record'][player]['hu']
    def record_bai_mo(self):
        sht=self.wb.sheets['被摸']
        for player,cell in self.cell_idx.items():
            sht.range(cell).value=self.gs['player_today_record'][player]['bai_mo']        
def test():
    #print(get_cell_index(20,27))
    #return
    app = xw.App(visible=False,add_book=False)
    wb = app.books.add()
    wb = app.books.open('c.xlsx')
    sht = wb.sheets['點數']
    col= (sht.range("A1").end("right").column)
    row= (sht.range("B1").end("down").row)

    print (sht.range("A1").end("right").column)
    print (sht.range("B1").end("down").row)

    sht.range(get_cell_index(1,col+1)).value="X"

    print (sht.range("A1").end("right").column)
    print (sht.range("B1").end("down").row)
    #sht.range('A10').value=
    #print(sht.range('A8').options(pd.DataFrame, index=False).value )
    #sht.range('A10').value=['A10','B10','C10','D10','E10']  OK 
    #sht.range('A11').value=['A11','B11','C11','D11','E11']  OK
    wb.save()
    wb.close()
    app.quit()
    app.kill()
    '''
    sht=wb.sheets["點數"]
    print (sht.range('B1:B1000').value)
    sht.range('A1').expand().value
    sht.range('A1:BZ1').value.index('菜狗') #=3 
    sht.range('B:B')[1:].value #select B column
    sht.range('A2').expand().value#取的A2一整列
    sht.range('A2').expand()[1].value#取得B2  A=0 B=1 C=2....
    sht.range('A1').expand()[3].value#=D1
    sht.range('A4').expand()[5].value#=F4
    ''' 
if __name__ == "__main__":
    gs={
        "player_today_record":{
            "威爾":{
                "bai_mo": 12,
                "gun": 14,
                "hu": 12,
                "name": "威爾",
                "nothing": 25,
                "playjiang": 3,
                "point": 100,
                "zhmo": 5
            },
            "碰碰":{
                "bai_mo": 12,
                "gun": 14,
                "hu": 12,
                "name": "菜狗",
                "nothing": 25,
                "playjiang": 3,
                "point": 200,
                "zhmo": 5
            },
            "榮恩":{
                "bai_mo": 12,
                "gun": 14,
                "hu": 12,
                "name": "榮恩",
                "nothing": 25,
                "playjiang": 3,
                "point": 300,
                "zhmo": 5
            },
            "國國":{
                "bai_mo": 12,
                "gun": 14,
                "hu": 12,
                "name": "國國",
                "nothing": 25,
                "playjiang": 3,
                "point": 400,
                "zhmo": 5
            }
        }
    }
    #print (gs)
    try:
        flag=sys.argv[1]
    except:
        flag="0"
    print (flag)
    ex=excel_record(gs)
    if flag == "test":
        test()
        sys.exit(0)
    elif flag=="open":
        ex.start_record()
    elif flag=="create":
        ex.init_excel_file()
        