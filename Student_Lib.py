import tkinter as tk
from tkinter import *
from tkinter import messagebox ,ttk
from turtle import width
from datetime import datetime
from PIL import Image , ImageTk
import mysql.connector
from tkcalendar import DateEntry
class Project:
    def __init__(self,root):
        self.root = root
        self.root.title("Admin Panel")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)

        # -- Image Setting in the Background -- #
        self.bg = ImageTk.PhotoImage(file="loginbg.jpg")
        self.bg_image = Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)
        # -- background image ends --#

        Frame_admin = Frame(self.root, bg="#EDEFF2")
        Frame_admin.place(x=0, y=0, height=600, width=500)
        title_admin = Label(root, text="Welcome Back to Admin Panel ", font=(" 'Raleway',sans-serif", 22, "bold"), fg="#000")
        title_admin.place(x=20, y=380)
        title_admin2 = Label(root, text="Click here to Access Student Portal", font=(" 'Raleway',sans-serif", 10, "bold"), fg="#000",bg="#EDEFF2")
        title_admin2.place(x=20,y=430)
        Button(root, text='Login as a student ', width=20, bg='#D7737A', fg='white', command=self.studentlogin).place(x=20,y=460)

        # -- Admin logo -- #
        photo = Image.open("admin.png")
        resized_image = photo.resize((300,300))
        converted_image = ImageTk.PhotoImage(resized_image)

        title_admin3 = tk.Label(root, image=converted_image)
        title_admin3.photo = converted_image  # Keep a reference to avoid garbage collection
        title_admin3.place(x=50, y=80)

        # -- background image ends --#
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=600, y=140, height=200, width=500)

        title = Label(Frame_login, text="Enter UserId", font=("Goudy old style", 15, "bold"), fg="#000", bg="#fff")
        title.place(x=30, y=60)

        self.entry_1 = Entry(Frame_login, font=("time new roman", 15), bg="lightgray")
        self.entry_1.place(x=170, y=60)

        title2 = Label(Frame_login, text="Enter Password", font=("Goudy old style", 15, "bold"), fg="#000",
                       bg="#fff")
        title2.place(x=30, y=90)

        self.entry_2 = Entry(Frame_login, font=("time new roman", 15), bg="lightgray")
        self.entry_2.place(x=170, y=90)

        Button(Frame_login, text='Login', width=10, bg='#D7737A', fg='white', command=self.login).place(x=170,   y=120)

    def studentlogin(self):
        student_login = Frame(self.root, bg="white")
        student_login.place(x=1, y=0, height=700, width=1200)

        student_logininside = Frame(self.root, bg="black")
        student_logininside.place(x=150, y=150, height=340, width=500)

        title = Label(student_logininside, text="Student Pannel", font=("impact", 35, "bold"), fg="#D7737A", bg="black")
        title.place(x=100, y=30)

        title = Label(student_logininside, text="Student login here", font=("time new roman", 10, "bold"), fg="#fff",
                      bg="black")
        title.place(x=100, y=100)

        title = Label(student_logininside, text="Enter UserId", font=("Goudy old style", 15, "bold"), fg="#fff",
                      bg="black")
        title.place(x=60, y=160)
        self.stu_id = Entry(student_logininside, font=("time new roman", 15), bg="lightgray")
        self.stu_id.place(x=200, y=165)

        title2 = Label(student_logininside, text="Enter Password", font=("Goudy old style", 15, "bold"), fg="#fff",
                       bg="black")
        title2.place(x=60, y=200)
        self.stu_pass = Entry(student_logininside, font=("time new roman", 15), bg="lightgray")
        self.stu_pass.place(x=200, y=200)

        Button(student_logininside, text='Login', width=10, bg='#D7737A', fg='white', command=self.loginstudent).place(x=200,
                                                                                                                y=240)

    def loginstudent(self):
        student_id = self.stu_id.get()
        student_pass = self.stu_pass.get()

        if student_id == "" or student_pass == "":
            messagebox.showerror("Error", "All Fields are Required")
        else:
            db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
            mycursor = db.cursor()
            sql = "SELECT * FROM sms.student where studentid=%s and spassword=%s"
            val = (student_id, student_pass)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            db.close()

            if result:
                student_name = result[0][1]
                messagebox.showinfo("Login", f"Successfully Login! Welcome user: {student_id}")
                self.show_student_data_afterlogin(student_id,student_name)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials. Please check your UserID and Password.")

    def show_student_data_afterlogin(self, student_id,student_name):
        s_data = Frame(self.root, bg="black")
        s_data.place(x=0, y=0, height=700, width=1199)

        title_d = Label(s_data, text=f"Welcome: {student_name} Your Details", font=("impact", 25, "bold"), fg="white", bg="black")
        title_d.place(x=50, y=10)

        tree = ttk.Treeview(s_data, columns=(
        "ID", "Name", "DB", "Password", "Course-Id", "C-Name", "date-Of-Course", "Timing-Of-Course"), show="headings")

        db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
        mycursor = db.cursor()
        sql = "SELECT student.studentid, student.sname, student.sdob, student.spassword, course.courseid, course.coursename, course.coursedate, course.coursetime FROM sms.student JOIN sms.course ON student.studentid = course.studentid WHERE student.studentid = %s"
        mycursor.execute(sql, (student_id,))
        result = mycursor.fetchall()
        db.close()

        tree.column("ID", width=100)
        tree.column("Name", width=150)
        tree.column("DB", width=100)
        tree.column("Password", width=150)
        tree.column("Course-Id", width=100)
        tree.column("C-Name", width=150)
        tree.column("date-Of-Course", width=150)
        tree.column("Timing-Of-Course", width=150)

        tree.heading("ID", text="Student-Id")
        tree.heading("Name", text="Student-Name")
        tree.heading("DB", text="D-O-B")
        tree.heading("Password", text="Student-Password")
        tree.heading("Course-Id", text="Course-Id")
        tree.heading("C-Name", text="Course-Name")
        tree.heading("date-Of-Course", text="Course-Date")
        tree.heading("Timing-Of-Course", text="Course-Timing")

        tree.place(x=10, y=80)

        for row in result:
            tree.insert("", "end", values=row)

    def Register(self):
        # Register new User using this function
        val_id = self.entry_11.get()
        val_name = self.entry_22.get()
        val_dob = self.entry_33.get()
        val_password=self.entry_44.get()
        print(f"Your Student id is: {val_id} and Name is: {val_name}")
        if val_id == "" or val_name == "":
            messagebox.showerror("Error", "All Fields are Required")
        else:
            db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
            mycursor = db.cursor()
            sql = "INSERT INTO sms.student (`studentid`, `sname`,`sdob`,`spassword`) VALUES (%s, %s,%s, %s)"
            val = (val_id, val_name,val_dob,val_password)
            mycursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Data inserted successfully!")
            # Register Function End

    def Delete(self):
        # Get the student ID to be deleted
        val_id = self.entry_11.get()

        if val_id == "":
            messagebox.showerror("Error", "Student ID is Required")
        else:
            try:
                db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
                mycursor = db.cursor()
                sql = "DELETE FROM sms.student WHERE `studentid` = %s"
                val = (val_id,)
                mycursor.execute(sql, val)
                db.commit()
                db.close()
                messagebox.showinfo("Success", "Data deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database Error: {err}")

    def Update(self):
        # Update existing student record using this function
        val_id = self.entry_11.get()
        val_name = self.entry_22.get()
        val_dob = self.entry_33.get()
        val_password = self.entry_44.get()
        print(f"Updating Student with ID: {val_id}")

        if val_id == "" or val_name == "":
            messagebox.showerror("Error", "All Fields are Required")
        else:
            db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
            mycursor = db.cursor()
            sql = "UPDATE sms.student SET `sname` = %s, `sdob` = %s, `spassword` = %s WHERE `studentid` = %s"
            val = (val_name, val_dob, val_password, val_id)
            mycursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Data updated successfully!")
            # Update Function End




    def show_data(self):
        Frame_data = Frame(self.root, bg="black")
        Frame_data.place(x=500, y=0, height=600, width=1199)

        title_d = Label(Frame_data, text="Manage Student", font=("impact", 35, "bold"), fg="white", bg="black")
        title_d.place(x=50, y=10)

        tree = ttk.Treeview(Frame_data, columns=("ID", "Name", "DB", "Password","Course-Id", "C-Name", "date-Of-Course", "Timing-Of-Course"), show="headings")

        # Assuming you have already created the 'tree' widget as described in your code

        db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
        mycursor = db.cursor()
        sql = "SELECT student.studentid,student.sname,student.sdob,student.spassword ,course.courseid,course.coursename,course.coursedate,course.coursetime from sms.student join sms.course"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        db.close()

        # Adjust column widths and set headings
        tree.column("ID", width=60)
        tree.column("Name", width=80)
        tree.column("DB", width=100)
        tree.column("Password", width=90)
        tree.column("Course-Id",width=50)
        tree.column("C-Name", width=120)
        tree.column("date-Of-Course", width=120)
        tree.column("Timing-Of-Course", width=120)

        tree.heading("ID", text="Stu-Id")
        tree.heading("Name", text="Stu-Name")
        tree.heading("DB", text="D-O-B")
        tree.heading("Password", text="S-Password")
        tree.heading("Course-Id",text="C-Id")
        tree.heading("C-Name", text="C-Name")
        tree.heading("date-Of-Course", text="Course-Date")
        tree.heading("Timing-Of-Course", text="C-Timing")

        # Place the treeview widget
        tree.place(x=10, y=80)

        for row in result:
            tree.insert("", "end", values=row)

    def login(self):
        # Right side Start ...
        # Database connection start
        val_id = self.entry_1.get()
        val_name = self.entry_2.get()

        db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
        mycursor = db.cursor()
        sql = "SELECT * FROM sms.student where studentid=%s and spassword=%s"
        val = (val_id, val_name)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        print(f"Your Student id is: {result} and Name is: {result}")
        if val_id == "" or val_name == "":
            messagebox.showerror("Error", "All Fields are Required")
        if result:

            messagebox.showinfo("Login", f"Successfully Login ! Welcome user: {val_id}")
            self.show_data()

            sql = "SELECT * FROM sms.student"
            mycursor.execute(sql)
            result = mycursor.fetchall()
            student_count=len(result)
            db.close()

            Frame_data_left = Frame(self.root, bg="white")
            Frame_data_left.place(x=10, y=0, height=600, width=500)
            lable_for_total_no_of_student=Label(Frame_data_left,text=f"Total Number of Student : {student_count}",font=("Helvetica", 16),fg="white",bg="green")
            lable_for_total_no_of_student.place(x=10,y=10)
            title_left = Label(Frame_data_left, text="Enter Student_Id", font=("Goudy old style", 15), fg="#000", bg="#fff")
            title_left.place(x=10, y=50)
            self.entry_11 = Entry(Frame_data_left, font=("time new roman", 15), bg="lightgray")
            self.entry_11.place(x=10, y=80)
            title_left2 = Label(Frame_data_left, text="Enter Student_Name", font=("Goudy old style", 15), fg="#000", bg="#fff")
            title_left2.place(x=10, y=110)
            self.entry_22 = Entry(Frame_data_left, font=("time new roman", 15), bg="lightgray")
            self.entry_22.place(x=10, y=140)
            title_left3 = Label(Frame_data_left, text="Enter Student D-O-B", font=("Goudy old style", 15),fg="#000",bg="#fff")
            title_left3.place(x=10, y=170)
            self.entry_33 = Entry(Frame_data_left, font=("time new roman", 15), bg="lightgray")
            self.entry_33.place(x=10, y=200)
            title_left4 = Label(Frame_data_left, text="Enter Student Password", font=("Goudy old style", 15), fg="#000", bg="#fff")
            title_left4.place(x=10, y=230)
            self.entry_44 = Entry(Frame_data_left, font=("time new roman", 15), bg="lightgray")
            self.entry_44.place(x=10, y=260)

            Button(Frame_data_left, text='Add Student', width=15, bg='#D7737A', fg='white',  command=self.Register).place(x=10, y=320)
            Button(Frame_data_left, text='Delete Student', width=15, bg='#D7737A', fg='white',  command=self.Delete).place(x=150, y=320)

            Button(Frame_data_left, text='Update Student', width=15, bg='#D7737A', fg='white',   command=self.Update).place(x=10, y=350)
            Button(Frame_data_left, text='Show Result', width=15, bg='#D7737A', fg='white',   command=self.show_data).place(x=150, y=350)

            Button(Frame_data_left, text='Add Course', width=15, bg='#D7737A', fg='white',   command=self.addcourse).place(x=10, y=380)
            Button(Frame_data_left, text='Delete Course', width=15, bg='#D7737A', fg='white',   command=self.delete_course).place(x=150, y=380)



        else:
            messagebox.showinfo("Error", "Password and Username is incorrect!")
        db.close()
        # Database connection close

    def addcourse(self):
        add_course = Frame(self.root, bg="#D7737A")
        add_course.place(x=500, y=0, height=600, width=700)

        courseid = Label(add_course, text="Enter Course-Id", font=("Goudy old style", 15, "bold"), fg="white",       bg="#D7737A")
        courseid.place(x=10, y=5)
        self.course_id = Entry(add_course, font=("time new roman", 15), bg="white")
        self.course_id.place(x=10, y=35)

        coursename = Label(add_course, text="Select Course", font=("Goudy old style", 15, "bold"), fg="white",  bg="#D7737A")
        coursename.place(x=10, y=70)

        # Create a Combobox with course options
        course_options = ["web", "Android", "Html"]
        self.selected_course = StringVar()  # Variable to hold selected course
        course_combobox = ttk.Combobox(add_course, textvariable=self.selected_course, values=course_options,  font=("time new roman", 15))
        course_combobox.place(x=10, y=100)

        coursstudentname = Label(add_course, text="Select student to assign this course",   font=("Goudy old style", 15, "bold"), fg="white", bg="#D7737A")
        coursstudentname.place(x=10, y=130)

        # Retrieve student names and IDs from the database
        db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
        mycursor = db.cursor()
        mycursor.execute("SELECT studentid, sname FROM student")
        student_data = mycursor.fetchall()
        db.close()

        # Create a Combobox with student options
        student_options = [f"{student_id} - {student_name}" for student_id, student_name in student_data]
        self.selected_student = StringVar()  # Variable to hold selected student
        student_combobox = ttk.Combobox(add_course, textvariable=self.selected_student, values=student_options, font=("time new roman", 15))
        student_combobox.place(x=10, y=160)
        # Date Picker
        date_label = Label(add_course, text="Select Course Date", font=("Goudy old style", 15, "bold"), fg="white",
                           bg="#D7737A")
        date_label.place(x=10, y=190)
        self.selected_date = StringVar()
        date_picker = DateEntry(add_course, textvariable=self.selected_date, font=("time new roman", 15),   background='darkblue', foreground='white')
        date_picker.place(x=10, y=220)

        # Time Picker
        time_label = Label(add_course, text="Select Course Time (HH:MM AM/PM)", font=("Goudy old style", 15, "bold"),
                           fg="white", bg="#D7737A")
        time_label.place(x=10, y=250)
        self.selected_time = tk.StringVar()
        time_picker = ttk.Spinbox(add_course, from_=0, to=23, increment=1, width=2, textvariable=self.selected_time)
        time_picker.place(x=10, y=280)

        self.selected_ampm = tk.StringVar()
        ampm_picker = ttk.Combobox(add_course, values=["AM", "PM"], textvariable=self.selected_ampm, state="readonly")
        ampm_picker.place(x=60, y=280)
        save_course_button = Button(add_course, text='Save Course', width=15, bg='#D7737A', fg='white',  command=self.save_course)
        save_course_button.place(x=10, y=320)
        del_course_button = Button(add_course, text='Delete Course', width=15, bg='#D7737A', fg='white',   command=self.delete_course)
        del_course_button.place(x=140, y=320)
        del_course_button = Button(add_course, text='Update Course', width=15, bg='#D7737A', fg='white',  command=self.update_course)
        del_course_button.place(x=280, y=320)
      

    # ... (other code remains unchanged) ...

    def save_course(self):
        course_id = self.course_id.get()  # Retrieve the course_id here after user input
        selected_course = self.selected_course.get()
        selected_student = self.selected_student.get().split(' - ')[0]
        selected_date_str = self.selected_date.get()
        selected_date = datetime.strptime(selected_date_str, '%m/%d/%y')

        # Convert the time format to HH:MM:SS
        selected_time = f"{self.selected_time.get()}:00"
        if self.selected_ampm.get() == "PM":
            hours, minutes = self.selected_time.get().split(":")
            if int(hours) != 12:
                hours = str(int(hours) + 12)
            selected_time = f"{hours}:{minutes}:00"

        db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
        mycursor = db.cursor()
        sql = "INSERT INTO course (`courseid`, `coursename`, `studentid`, `coursedate`, `coursetime`) VALUES (%s, %s, %s, %s, %s)"
        val = (course_id, selected_course, selected_student, selected_date, selected_time)
        mycursor.execute(sql, val)
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Course added successfully!")

    def delete_course(self):
        course_id = self.course_id.get()  # Retrieve the course_id for deletion
        if not course_id:
            messagebox.showwarning("Warning", "Please enter a course ID to delete.")
            return

        db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
        mycursor = db.cursor()
        sql = "DELETE FROM course WHERE courseid = %s"
        val = (course_id,)
        mycursor.execute(sql, val)
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Course deleted successfully!")

    def update_course(self):
        course_id = self.course_id.get()  # Retrieve the course_id for update
        selected_course = self.selected_course.get()
        selected_student = self.selected_student.get().split(' - ')[0]
        selected_date_str = self.selected_date.get()
        selected_date = datetime.strptime(selected_date_str, '%m/%d/%y')

        selected_time = f"{self.selected_time.get()}:00"
        if self.selected_ampm.get() == "PM":
            hours, minutes = self.selected_time.get().split(":")
            if int(hours) != 12:
                hours = str(int(hours) + 12)
            selected_time = f"{hours}:{minutes}:00"

        db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='sms')
        mycursor = db.cursor()
        sql = "UPDATE course SET coursename = %s, studentid = %s, coursedate = %s, coursetime = %s WHERE courseid = %s"
        val = (selected_course, selected_student, selected_date, selected_time, course_id)
        mycursor.execute(sql, val)
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Course updated successfully!")


root = Tk()
obj=Project(root)
root.mainloop()
