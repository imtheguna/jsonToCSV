import urllib, json
import math
import flet as ft
from flet import *
import requests
import json,csv
class Headerinput():
    def __init__(self) -> None:
        self.oldheader = []
        self.newheader = []
        self.status = False
    def getNewHeader(self):
        return self.newheader
    def setNewheader(self,header=[]):
        self.newheader = header
    def getOldHeader(self):
        return self.oldheader
    def setOldheader(self,header=[]):
        self.oldheader = header
    def getUpdateStatus(self):
        return self.status
    def setUpdateStatus(self,ststus=False):
        self.status = ststus
    
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])  

isFile = True
fileName = ''
fileSize= ''
filePath=''
isDataRead = False
out={}
CheckOn = ft.Checkbox(label='Remove Root Node', value=False)
isHeaderUpdate = False
auto_header_listdata = Column([],scroll=ScrollMode.ALWAYS)
header_md5_columns = Column([],)
def main(page: ft.Page):

    auto_header = []
    fileDetails = Column([])
    JsonData=''
    headerinput = Headerinput()
    headerinput.setOldheader(header=['Name','addressaddressaddressaddress','f','k','k','k'])
    headerinput.setNewheader(header=['Column_0'])
    def headerUpdate(i):
        try:   
            column = tb2.value.strip()
            if(len(column)!=0):
                on_click(1,'Reading Json to get the Columns')
                headerinput.setNewheader(column.split(','))
                readjSON()
            else:
                on_click(1,'Enter the Header')
                return
            if(headerinput.getUpdateStatus()==False):
                #setOldheaderInput(header=headerinput.getOldHeader())
                setNewheaderInput(newheader=headerinput.getNewHeader(),oldheader=headerinput.getOldHeader())
                headerinput.setUpdateStatus(ststus=True)
            return page.go("/header")
        except Exception as e:
            print(e)
            on_click(1,e)
    def textbox_changed2(e):
        tb2.value = e.control.value
        page.update()
    def textbox_changed3(e):
        tb3.value = e.control.value
        page.update()
    tb2 = ft.TextField(label="Enter Header (Comma Delimited)",color=ft.colors.WHITE,border_color=ft.colors.WHITE54,
                       on_change=textbox_changed2)
    tb3 = ft.TextField(label="Enter Root Node(Optional)",color=ft.colors.WHITE,border_color=ft.colors.WHITE54,
                       on_change=textbox_changed3)
    headerUserInput = Column([Text('Header(Optional)',weight=FontWeight.BOLD),tb2])

    def flatten_json(data):
        output=[]
        global out, JsonData
        def flatten(x,name=''):
            global out
            if type(x) is dict:
                for a in x:
                    flatten(x[a],name+a+'_')
            elif type(x) is list:
                i=0
                for a in x:
                    flatten(a,name+str(i)+'_')
                    i+=1
            else:
                out[name[:-1]]=x
            
        if type(data) is not list:
            data = [data]
        for i in data:
            flatten(i)
            output.append(out)
            out={}

        column_list = output[0].keys()
        
        headerinput.setOldheader(header=list(column_list))
        return output
    
    def writeCSV(data):
        try:
            with open(tb4.value+tb5.value,'w') as outfile:
                writer = csv.writer(outfile)
                if(isHeaderUpdate):
                    headers=headerinput.getNewHeader()
                else:
                    headers = headerinput.getOldHeader()
                writer.writerow(headers)
                for rec in data:
                    writer.writerow(rec.values())
                on_click(1,'CSV Created')
        except Exception as e:
            print(e)
            on_click(1,e)   

    def readjSON():
        try:
            global JsonData,isDataRead
            isDataRead=True
            if(isFile):
                j = json.load(open(filePath))
            else:
                j=JsonData
            root_node = tb3.value.strip()
            
            if(CheckOn.value):
                root = list(j.keys())
                print(root)
                data = flatten_json(data=j[root[0]])
            elif(len(root_node)!=0):
                if root_node not in j:
                    on_click(1,'Invalid Root Node')
                    return False
                data = flatten_json(data=j[root_node])
            else:
                data = flatten_json(data=j)
            JsonData = data
            
            setOldheaderInput(header=headerinput.getOldHeader())
            return data
        except Exception as e:
            print(e)
            on_click(1,e)
    
    def submit(i):
        if(len(tb4.value)==0 or len(tb5.value)==0):
            on_click(1,'Enter the out file details')
            return
        global JsonData
        isRoot = True
        if(isDataRead==False):
            isRoot = readjSON()
        if(isRoot==False):
            return
        writeCSV(JsonData)
        return True

    def on_click(e,msg):
            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True
            page.update()
    def pick_files_result(e: ft.FilePickerResultEvent):
        global fileName,filePath,fileSize,isFileSelect
        if e.files:
            file = e.files[0]
            fileName = file.name
            filePath = file.path
            fileSize = convert_size(file.size)
            isFileSelect=True
            fileDetails.controls=[Container(content=Text('Source File',weight=FontWeight.BOLD),padding=6,),
            Row([Container(content=Text('File Name',weight=FontWeight.W_400),padding=6),
                Container(content=Text(fileName,weight=FontWeight.W_400),)]),        
            Row([Container(content=Text('File Size',weight=FontWeight.W_400),padding=6),
                Container(content=Text(fileSize,weight=FontWeight.W_400),)]),headerUserInput,tb3,CheckOn,subbt
            ]
            page.update()
            on_click(1,'File Selected')
            return True
        else:
            return False
    def textbox_changed(e):
        tb1.value = e.control.value
        page.update()
    def textbox_changed4(e):
        tb4.value = e.control.value
        page.update()
    def textbox_changed5(e):
        tb5.value = e.control.value
        page.update()
    def md5fun(i):
        readjSON()
        global header_md5_columns
        #setOldheaderInput(header=headerinput.getOldHeader())
        header_md5_columns = auto_header_listdata
        for i in range(0,len(header_md5_columns.controls)):
            header_md5_columns.controls[i] = Row([ft.Checkbox(value=False)
                                                  , header_md5_columns.controls[i]])

        page.go("/md5")
        #ft.ElevatedButton("Apply MD5", on_click=md5fun,color=ft.colors.WHITE),
    subbt =  Row([ft.ElevatedButton("Rearrange Header", on_click=headerUpdate,color=ft.colors.WHITE),
                  ElevatedButton(
                text="Submit And Process", on_click=submit, color=ft.colors.WHITE,)])
    
    tb1 = ft.TextField(label="Enter API Link",color=ft.colors.WHITE,border_color=ft.colors.WHITE54,value='',
                       on_change=textbox_changed)
    tb4 = ft.TextField(label="Enter Out File Path",color=ft.colors.WHITE,border_color=ft.colors.WHITE54,value='',
                       on_change=textbox_changed4)
    tb5 = ft.TextField(label="Enter Out Name",color=ft.colors.WHITE,border_color=ft.colors.WHITE54,value='',
                       on_change=textbox_changed5)
    
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    
    listdata = Column([],scroll=ScrollMode.ALWAYS)

    page.title = "Json To CSV"
    page.theme = ft.Theme(
    scrollbar_theme=ft.ScrollbarTheme(
        thickness=30,
        radius=10,
        main_axis_margin=5,
        cross_axis_margin=10,
    ))

    def willdrag(e:DragTargetAcceptEvent):
        src = page.get_control(e.src_id)
        #src.content.bgcolor='blue'
        source_val = src.content.content.value
        e.control.content.content.bgcolor='blue200'
        dest_index = listdata.controls.index(e.control)
        source_inx = None

        for i,x in enumerate(listdata.controls):
            if x.content.content.content.value == source_val:
                source_inx = i

        listdata.controls[source_inx],listdata.controls[dest_index]=listdata.controls[dest_index],listdata.controls[source_inx]
        page.update()

    def setOldheaderInput(header):
        print('Header Adding')
        global auto_header_listdata 
        auto_header_listdata = Column([],scroll=ScrollMode.ALWAYS)
        for x in range(0,len(header)):
            auto_header_listdata.controls.append(
                Container(
                        bgcolor='orange200',
                        padding=10,
                        width=200,
                        content=Text(header[x],size=11,expand=True,color='black')  
            )
        )
    def setNewheaderInput(oldheader,newheader):

        if(len(oldheader)!=len(newheader) and len(oldheader)>len(newheader) ):
            for i in range(1,len(oldheader)-len(newheader)+1):
                newheader.append('Column_'+str(i))
        for x in range(0,len(oldheader)):
            listdata.controls.append(
            DragTarget(
                on_accept=willdrag,
                content=Draggable(
                    content=Container(
                        bgcolor='green200',
                        padding=10,
                        width=200,
                        content=Text(newheader[x],size=11,expand=True,color='black')
                    )
                )
            )
        )

   
   

    def srcInput(i):
        files = pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
        page.update()

    def JSONFromAPI(i):
        try:
            global JsonData,isFile
            isFile=False
            if(tb1.value==''or tb1.value is None):
                on_click(1,'Invalid API Link')
                return
            on_click(1,'Reading Data From API')
            r = requests.get(tb1.value)
            JsonData = r.json()
            on_click(1,'Data Fetched')
            fileDetails.controls=[Column([Row([Container(content=Text('API Status :',weight=FontWeight.W_400),padding=6),
                    Container(content=Text('Complated',weight=FontWeight.W_400),)]),
                    headerUserInput,tb3,CheckOn,subbt
                    ])]
            page.update()
            return JsonData
        except Exception as inst:
            on_click(1,inst)
    
    def getView():
        return [
        ft.AppBar(title=ft.Text("Home"), bgcolor=ft.colors.SURFACE_VARIANT),
        Row([ft.Container(
        Column([
        Row([
            GestureDetector(content=Container(Column([
            Text(r"{}",size=60,color=ft.colors.WHITE12),
            Text(r"Select JSON",size=20,color=ft.colors.WHITE12),
            #Icon(name=icons.File, color=colors.WHITE12),
            ],
                  alignment=ft.alignment.center,
                  horizontal_alignment=CrossAxisAlignment.CENTER),
                  bgcolor=ft.colors.WHITE10,
                  margin=10,
                  height=150,
                  width=150,
                  border_radius=8,
                  ),on_tap=srcInput),
        GestureDetector(content=Container(Column([
            Icon(name=icons.BROWSER_UPDATED,color=ft.colors.WHITE12,size=30),
            Text(r"From API",size=20,color=ft.colors.WHITE12)
            ],
                  alignment=MainAxisAlignment.CENTER,
                  horizontal_alignment=CrossAxisAlignment.CENTER),
                  bgcolor=ft.colors.WHITE10,
                  margin=10,
                  height=150,
                  width=150,
                  border_radius=8,
                  ),on_tap=JSONFromAPI),
            ]),Container(content=tb1,padding=10),
            fileDetails
                      
            ],
            alignment=MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        expand=True,
        margin=10,
        padding=6,
        #bgcolor=ft.colors.WHITE10,
        border_radius=8,
        alignment=ft.alignment.top_left,),ft.Container(
        Column([Text('Output File Details'),tb4,tb5],alignment=MainAxisAlignment.START),
        expand=True,
        #header=page.height,
        margin=10,
        padding=6,
        
        border_radius=8,
        alignment=ft.alignment.top_left,)
        ],alignment=MainAxisAlignment.START,vertical_alignment=CrossAxisAlignment.START)
    ]
    def save_header(i):
        list = []
        global isHeaderUpdate
        for i,x in enumerate(listdata.controls):
            list.append(x.content.content.content.value)
        headerinput.setNewheader(list)
        isHeaderUpdate=True
        on_click(1,'Header Updated')
        page.go("/")

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    getView(),
                )
            )
        if page.route == "/header":
            page.views.append(
            ft.View(
                "/header",
                [
                    ft.AppBar(title=ft.Text("Rearrange Header"), bgcolor=ft.colors.SURFACE_VARIANT),
                    Column([Text('Drag and drop the column'),Row([
                                Container(content=Column([Text('Defalut Header'),auto_header_listdata]),padding=16),
                                Container(content=Column([Text('New header'),listdata]),padding=16),]),],
        expand=True,
        scroll=ScrollMode.ALWAYS,alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.START),
                    Row([ft.ElevatedButton("Close", on_click=lambda _: page.go("/")),ft.ElevatedButton("Save", on_click=save_header),])
                ],
            )
        )
        if page.route == "/md5":
            page.views.append(
            ft.View(
                "/md5",
                [
                    ft.AppBar(title=ft.Text("Apply MD5"), bgcolor=ft.colors.SURFACE_VARIANT),
                    Column([Text('Select Columns'),Row([
                                Container(content=Column([Text('Defalut Header'),header_md5_columns]),padding=16),
                                ]),],
        expand=True,
        scroll=ScrollMode.ALWAYS,alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.START),
                    Row([ft.ElevatedButton("Close", on_click=lambda _: page.go("/")),ft.ElevatedButton("Save", on_click=save_header),])
                ],
            )
        )
       
       
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.theme_mode = ft.ThemeMode.DARK
    page.overlay.append(pick_files_dialog)
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, view=ft.AppView.WEB_BROWSER,port=8502)