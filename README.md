# sqlite3_python
My wrapper for sqlite3

Stupid abstraction over sqlite so you don't have to remember the syntax 

How it work? 
I dont know (joke) 

1. you are initializing the class "DB = Data_Base("BASE.db",string)"
   the first argument is the name of the database file (and the path to it if it is not in the same folder as the file)
   the second argument should get a string to create tables (there is an example in the code)
   p.s. please use only INT and TEXT types in your tables because i was too lazy to do a proper type check
   
2. methods....
   class Data_Base have 6 public methods 
   1. Add_to_base(table_name:str, elements:list)
     table_name: is the table name, it stupid and easy 
     elements: is list of arguments, i dont know how many colums in your table That's why I put them on the list.
     for exemple:
       your table look like 
       name: phone_num: job: adress:
       and now you need to add an item to your table, you call the Add_to_base method and pass the list as the elements argument
       you MUST specify in the list all data of the same type that is specified in the table

   2. Get_from_base(table_name:str, column:str="*", condition:str=None)
     table_name: is the table name
     column: this is what you want to get. If you do not change the argument you will get all lines
     condition: It's kind of like a filter.
     for exemple:
         Recall the table from the last example
         name: phone_num: job:     adress:
         ivan  123456789  manager  russia
         egor  987654321  admin    russia
         we want get name and number of admin to call him and ask him to fix the toaster
         Get_from_base("stuff", "name, phone_num", "job = 'admin'")
      




