from tkinter import *
from tkinter import ttk 
import datetime as dt 
from mydb import *
from tkinter import messagebox

#object 
data = database(db='myexpenses.db')

#Global variable 
count = 0
slected_rowid = 0

def saveRecord():
    global data 
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count 
    for rec in f:
        tv.insert(parent='', index='0', iid=count, value=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid 
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass

def update_record():
    global selected_rowid

    selected = tv.focus()
    #update record 
    try:
        data.updateRecord(namevar.get(), amtvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)

    #clear entry boxes 
    item_name.delete(0,END)
    item_amt.delete(0,END)
    transaction_date.delete(0,END)
    tv.after(400,refreshData)
     
def totalBalance():
    f = data.fetchRecord(query="select sum (item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance: ', f"Total Expense: ' {j} \nBalance Remaining: {5000 - j}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)           
    fetch_records()

def deleteRow():
    global  selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()


ws=Tk()
ws.title('Daily Expenses')

f = ('Time new roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

#frame widget
f2 = Frame(ws)
f2.pack()

f1 = Frame(
    ws,
    padx = 10,
    pady = 10,
)
f1.pack(expand=True, fill=BOTH)


#lable widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)


#entry widget
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)


#grid placment 
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))


#buttons 
cur_date = Button(
    f1,
    text='Current Date',
    font=f,
    bg='#04C4D9',
    command=setDate,
    width=15
)

submit_btn = Button(
    f1,
    text='Save Record',
    font=f,
    bg='#42602D',
    command=saveRecord,
    fg='white'
)

clr_btn = Button(
    f1,
    text='Clear Entry',
    font=f,
    bg='#04C4D9',
    command=clearEntries,
    fg='white'
)

quit_btn = Button(
    f1,
    text ='Exit',
    font=f,
    bg='#D33532',
    command= lambda:ws.destroy(),
    fg='white'
)

total_bal = Button(
    f1,
    text= 'Total Balance',
    font =f,
    bg='#486966',
    command=totalBalance
)

update_btn = Button(
    f1,
    text='Update',
    bg='#C2BB00',
    command=update_record,
    font=f
)

del_btn = Button(
    f1,
    text='Delete',
    bg='#BD2A2E',
    command=deleteRow,
    font=f
)

#grid placement 
cur_date.grid(row=3, column=1, sticky=EW, padx=(10,0))
submit_btn.grid(row=0, column=2,sticky=EW, padx=(10,0))
submit_btn.grid(row=0, column=2,sticky=EW, padx=(10,0))
submit_btn.grid(row=0, column=2,sticky=EW, padx=(10,0))
submit_btn.grid(row=0, column=2,sticky=EW, padx=(10,0))
submit_btn.grid(row=0, column=2,sticky=EW, padx=(10,0))
submit_btn.grid(row=0, column=2,sticky=EW, padx=(10,0))

#treeview 
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show ='headings', height=8)
tv.pack(side="left")

#add heading 
tv.column(1, anchor=CENTER, strech=NO, widht=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name",)
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

#binding treeview
tv.bind("<ButtonRelease-1>", select_record)

#style for treeview 
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

#vertical scrollbar
scrollbar = Scrollbar(f2, orient = 'vertcial')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.configure(yscrollcommand=scrollbar.set)

#calling function 
fetch_records()

#infinity loop 
ws.mainloop()
