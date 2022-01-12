#MySQLConnection is a class.
#mysql.connector is a module that is a python file which contains a lot of python functions/methods.
#connect() is a function of the mysql.connector module. 
#connect() accepts connection credentials and returns an object of type MySQLConnection 
#connection is a returned object of MySQLConnection class.
#MySQLcursor is a class.
#cursor object can be created through the cursor() method of the connection object(connection): cursor1 = connection.cursor()
# OR it can be created through MySQLCursor class directly : cursor2 = MySQLCursor(connection.)




import mysql.connector  
from mysql.connector import Error


connection = mysql.connector.connect(host='localhost', 
                                    database='project2', 
                                    user='root',
                                    password='Stigma@18')
    
cursor = connection.cursor(prepared=True)
       
#1_this sql code all the records of publishers
publisher_query= "select * from publishers"  
    
#executing the sql qcommand inside the execute  
cursor.execute(publisher_query)
    
#saving all the data from the cursor object into records.  
pub_records = cursor.fetchall() 
    
#looping through the publishers records
for row in pub_records: 
    print(row) 
    

#2_this function creates the customers table.
    
customer_table= """CREATE TABLE customers (
                    custID int primary key AUTO_INCREMENT, 
                    custName varchar(70),
                    zip varchar(10),
                    city varchar(30),
                    state_name varchar(15)) """

cursor.execute(customer_table)
print("customers Table created successfully ")

#this prints out the colums of customers table.
cursor.execute("SHOW columns FROM customers")
print ([column[0] for column in cursor.fetchall()])

    
#3_inserting data into customer table

customer_query = """INSERT INTO customers (custName, zip, city, state_name) 
                    VALUES (%s, %s, %s, %s) """


customer_data = [('STEPHEN WALTHER', 'NULL', 'NULL', 'NULL'),
                     ('JAMES GOODWILL', 'NULL', 'NULL', 'NULL'),
                     ('CALVIN HARRIS', 'NULL', 'NULL', 'NULL'),
                     ('MARTIN GARRIX', 'NULL', 'NULL', 'NULL'),
                     ('PAMELA REIF', 'NULL', 'NULL', 'NULL')
                ]

#This executes data insetion into customer table.
cursor.executemany(customer_query, customer_data)
    
#confirming the changes made to the table
connection.commit()
print(cursor.rowcount, "Record inserted successfully into customer table")

#this function prints out the colums of customers table.
cursor.execute("SHOW columns FROM customers")
print ([column[0] for column in cursor.fetchall()])

#this prints out the records of the customer table
cursor.execute(" select * from customers")
customer_records = cursor.fetchall()

for value in customer_records:
    print(value)
    
    
#4_SQL code thart print the names of those who appear in both “author” and “customer.”

sql_command1= " select aName from customers as c, authors as a where c.custName=a.aname "

#using cursor to execute sql command.
cursor.execute(sql_command1)
common_name= cursor.fetchall()
for row in common_name:
    print(row)
        
#5_sql code to select price between 400 and 550

sql_command2= " select price from subjects as s, titles as t where s.subID=t.subID and price >= 400 and price<=550 "
cursor.execute(sql_command2)
command2_result= cursor.fetchall()
for row in command2_result:
    print(row)
    

    
#6_this sql code inside the execute fuction prints out the price of the latest published book.

cursor.execute("""
         select price
         from titles
         order by pubDate desc
         limit 1 """)

book_price = cursor.fetchall()
book_price1 = book_price[0]
    
#python string was assigned a sql command to update the titles query
update_price= """ update titles set price = %s where titleID = 1001  """
    
#python function is being used to update the query 
cursor.execute(update_price, book_price1)
    
#commiting the changes that has been made.
connection.commit()
print(" titles table has been updated ")

cursor.execute("""
    select * from titles """)
    
#getting the records from the updated titles table.
new_tiles_records= cursor.fetchall()
    
#looping through the records of titles table.
for row in new_tiles_records: 
    print(row)
    


#7_sql code that prints out the publisher's name contains a T.

cursor.execute( """
        select title
        from titles as t, publishers as p
        where t.pubID=p.pubID and p.pname like '%T%' """)
    
    
command3_result = cursor.fetchall()
for row in command3_result:
    print(row)

    
#8_sql query that to find titleId of the title name 'java.comp.ref’ from titles

cursor.execute("""
        select titleID
        from titles 
        where title= 'JAVA COMP. REF' """)
#getting the first tuple as a list
list_title_Id= cursor.fetchall()
#getting the first string element from the list 
tuple_title_ID= list_title_Id[0]
#getting the first integer element from the tuple
integer_title_ID= tuple_title_ID[0]
    
#sql query that to find auID of 'David hunter'from authors
cursor.execute( """
        select auID
        from authors 
        where aName= 'DAVAID HUNTER' """)
#getting the first tuple as a list
author_id = cursor.fetchall()
#getting the first string element from the list 
tuple_author_ID= author_id[0]
#getting the first integer element from the tuple
integer_author_ID= tuple_author_ID[0]



# creating a function to insert data as a row into the titleauthors table.
def insert_varibles_into_table(titleId, auID, importance):
    
    mySql_insert_query = """INSERT INTO titleauthors (titleId, auID, importance) 
                            VALUES (%s, %s, %s) """

    record = (titleId, auID, importance)
    cursor.execute(mySql_insert_query, record)
    connection.commit()
    print("Record inserted successfully into titleauthors table")
#passing the values of integer_title_ID and integer_author_ID into the function.
insert_varibles_into_table(integer_title_ID, integer_author_ID, 7)
   
#executing the sql code inside the execute function to get all the records of titleauthors table.
cursor.execute("""
        select * from titleauthors """)

titleauthors_records= cursor.fetchall()
    
#looping through the records
for row in titleauthors_records: 
    print(row) # printing the result.
    

    
#9_this sql command inside the execute() prints out the names of the authors that coauthored with 'HERBERT SCHILD'.

cursor.execute("""
        
        select aName
        from authors natural join titleauthors as N1
        where N1.titleID = (select M1.titleId
                    from authors natural join titleauthors as M1
                    where M1.auID= '101'
                    );
    
    """)
#getting coauthors records from the cursor with the help of fetch()
author_records= cursor.fetchall()
print( "The authors who coauthored with HERBERT SCHILD are following")
for row in author_records: 
    print(row)


#10_decreasing the prices of certain books 

cursor.execute("""
        update titles
        set price = case 
                        when year(pubDate) <'2004' then price*.70
                        else price*.85
                    end
    """)
#confirming the price changes.
connection.commit()
    
#getting all the records of titles table
cursor.execute("""
        select * from titles """)
    
updated_price= cursor.fetchall()

print("The updated prices of the books are the following: ")

for row in updated_price: 
    print(row)
    
cursor.close()
connection.close()


