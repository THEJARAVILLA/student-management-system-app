import pandas as pd
import streamlit as st
import sqlite3 as sq
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://wallpapercave.com/wp/wp2508260.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-image: url("https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1170");
        background-size: cover;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)
con = sq.connect("students.db")
cur=con.cursor()
def create_student_table():
    cur.execute("""
        create table if not exists stu (
            id text primary key,
            name text not null,
            phono integer unique not null check(length(phono)=10),
            age integer not null,
            gender text not null,
            course text not null,
            address text not null
        )
    """)
st.title("STUDENT MANAGEMENT SYSTEM")
if'is_logged' not in st.session_state:
    st.session_state.is_logged= False
if not st.session_state.is_logged:
    u_n=st.text_input("enter your user name")
    password=st.text_input("enter your password",type="password")
    login=st.button("login")
    if login:
        if u_n=="Admin" and password == "Admin@123":
            st.session_state.is_logged=True
            st.success("SUCCESSFULLY ADMIN LOGIN")
            st.rerun()
        else:
            st.error("Invalid username or password!")
elif st.session_state.is_logged:
    option=st.sidebar.selectbox("Choose an option:",["Add the student","Remove the student","Update the student_course","Display All student details","Logout"])
    st.write(option)
    if option == "Add the student":
        student_name=st.text_input("Enter The Name")
        student_phono=st.number_input("Enter The Phone Number",min_value=0)
        student_age=st.number_input("Enter The Age",min_value=0)
        gender=st.radio("Select Gender",["Male","Female"])
        student_course=st.text_input("Enter The Course")
        student_Address = st.text_input("enter the current address:")
        query="select count(rowid) from stu"
        cur.execute(query)
        res=cur.fetchall()[0][0]
        ids='QSP'+student_name[:3]+str(res+1)
        button=st.button("SUBMIT",type="primary")
        if button:
            q="insert into stu values(?,?,?,?,?,?,?)"
            cur.execute(q,(ids,student_name,student_phono,student_age,gender,student_course,student_Address))
            con.commit()
            st.success("SUCCESSFULLY ADDED YOUR DETAILS")
            st.balloons()
    elif option == "Remove the student":
        phono=st.number_input("enter the phone number",min_value=0)
        enter=st.button("DELETE",type="primary")
        if enter:
            query="delete from stu where phono=?"
            cur.execute(query,(phono,))
            con.commit()
            st.error("SUCCESSFULLY REMOVED YOUR DETAILS")
    elif option == "Update the student_course":
        phono=st.number_input("Enter The Phone Number",min_value=0)
        course=st.text_input("Enter The New Course")
        enter=st.button("SUBMIT HERE",type="primary")
        if enter:
            query="update stu set course=? where phono=?"
            cur.execute(query,(course,phono))
            con.commit()
            st.success("SUCCESSFULLY UPDATED YOUR NEW COURSE!")

    elif option == "Display All student details":
        query="select*from stu"
        cur.execute(query)
        res=cur.fetchall()
        # r=pd.DataFrame(res,columns=['id','student_name','phono','age','gender','course','address'])
        st.table(res)
    else:
        if st.sidebar.button("Logout"):
            st.session_state.is_logged = False
            st.rerun()
# create_student_table()