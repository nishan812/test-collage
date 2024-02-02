from tkinter import *
import sqlite3

root = Tk()
lbl = Label(root,text="Employee Management system",font=("Arial Bold",50))
lbl.place(x=100,y=0)
root.geometry("1200x800")
root.resizable(0,0)



connect = sqlite3.connect('employee.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS employee(
               ID INTEGER PRIMARY KEY AUTOINCREMENT,

               uname        TEXT,
               adr          TEXT,
               rl           TEXT,
               slr          INT
)""")

connect.commit()
connect.close()


# function to add data in database
def add():
    conn=sqlite3.connect("employee.db")
    c = conn.cursor()
    c.execute("INSERT INTO employee(uname,adr,rl,slr)VALUES(?,?,?,?)",
              (username.get(),address.get(),role.get(),salary.get()))
    conn.commit()
    conn.close()
    username.delete(0,END)
    address.delete(0,END)
    role.delete(0,END)
    salary.delete(0,END)




#function to retrieve data from database
def retrieve():
    conn = sqlite3.connect("employee.db")
    c = conn.cursor()
    # execute a SELECT query to  retrieve all records from the 'employee' table
    c.execute("SELECT *FROM employee")

    # fetch all records returned by the query

    records = c.fetchall()
    print_records=''
    
    for record in records:
        print_records+=str(record[0])+' '+\
        str(record[1]) + ' '+ str(record[2]) + ' '+ str(record[3]) +\
        ' '+ str(record[4]) + "\n"

    query_label = Label(root, text=print_records)
    query_label.place(x=700, y=200)
    conn.close()


#function to delete data from database
def delete():
    conn = sqlite3.connect("employee.db")
    c = conn.cursor()
    c.execute("DElETE FROM employee WHERE ID="+delete_record.get())
    conn.commit()
    delete_record.delete(0,END)
    retrieve()

#function to edit the data of already existing users
def edit():
    global editor 
    editor =Tk()
    editor.title('Update Data')
    editor.geometry('500x500')
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    record_id = update_record.get()
    c.execute("SELECT * FROM employee WHERE ID=?",(record_id,))
    records = c.fetchall()
    print(records)
    
    #creating global variables for all text boxes
    global username_editor
    global address_editor
    global role_editor
    global salary_editor

    username_editor = Entry(editor,width=30)
    username_editor.grid(row=0, column=1,padx=20,pady=(10,0))

    address_editor = Entry(editor,width=30)
    address_editor.grid(row=1,column=1)

    role_editor = Entry(editor,width=30)
    role_editor.grid(row=2,column=1)

    salary_editor = Entry(editor,width=30)
    salary_editor.grid(row=3,column=1)


    #creating textbox labels

    usernameIn_label = Label(editor, text="Username")
    usernameIn_label.grid(row=0,column=0,pady=(10,0)) 

    addressIn_label = Label(editor,text="Address")
    addressIn_label.grid(row=1,column=0)

    roleIn_label = Label(editor,text="Role")
    roleIn_label.grid(row=2,column=0)


    salaryIn_label = Label(editor,text="Salary",width=30)
    salaryIn_label.grid(row=3,column=0)


    #looping through the results
    for record in records:
        username_editor.insert(0,record[1])
        address_editor.insert(0,record[2])
        role_editor.insert(0,record[3])
        salary_editor.insert(0,record[4])


    update_record.delete(0,END)

    #creating a update button
    

    edit_btn = Button(editor, text=" SAVE",command=lambda:update(record_id))
    edit_btn.grid(row=6,column=0,columnspan=2,pady=10,padx=10,ipadx=125)




def update(record_id):
    #creating a databases or connect to one
    conn= sqlite3.connect('employee.db')
    #Create cursor
    c = conn.cursor()
    c.execute("""
        UPDATE employee SET
        uname =:u,
        adr=:a,
        rl=:r,
        slr=:s
        WHERE ID = :id""",
        {
            "u":username_editor.get(),
            "a":address_editor.get(),
            "r":role_editor.get(),
            "s":salary_editor.get(),
            "id":record_id
        }
)
    
    conn.commit()
    conn.close()

    #Destroying editor window and displaying updated data by calling retrieve function
    editor.destroy()
    retrieve()






# Labels
username_label = Label(root,text="Username",font=("Arial Bold",16))
username_label.place(x=0,y=100)

address_label = Label(root,text="Address",font=("Arial Bold",16))
address_label.place(x=0,y=200)

role_label = Label(root,text="Role",font=("Arial Bold",16))
role_label.place(x=0,y=300)

salary_label = Label(root,text="Salary",font=("Arial Bold",16))
salary_label.place(x=0,y=400)


delete_record_label = Label(root,text="Delete_Record",font=("Arial Bold",16))
delete_record_label.place(x=0,y=600)


update_record_label = Label(root,text="Update_Record",font=("Arial Bold",16))
update_record_label.place(x=0,y=700)

username = Entry(root,width=30)
username.place(x=250,y=100,height=30)

address = Entry(root,width=30)
address.place(x=250,y=200,height=30)

role = Entry(root,width=30)
role.place(x=250,y=300,height=30)

salary = Entry(root,width=30)
salary.place(x=250,y=400,height=30)

delete_record = Entry(root,width=30)
delete_record.place(x=200,y=600,height=30)

update_record = Entry(root,width=30)
update_record.place(x=200,y=700,height=30)



# Buttons 
add_button = Button(root,text="Add",font=("Arial Bold",16),command=add)
add_button.place(x=80,y=500)

retrieve_button = Button(root,text="Retrieve",font=("Arial Bold",16),command=retrieve)
retrieve_button.place(x=200,y=500)

delete_button = Button(root,text="Delete",font=("Arial Bold",16),command=delete)
delete_button.place(x=400,y=595)

upadate_button = Button(root,text="Upadate",font=("Arial Bold",16),command=edit)
upadate_button.place(x=400,y=695)

root.mainloop()