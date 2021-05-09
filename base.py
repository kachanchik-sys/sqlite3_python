#import sys                                                                      # это для
#sys.path.insert(0, "/home/tomoko/project/anekbotv/lib/python3.8/site-packages") # работы pypy ибо он сам не видит либы
import sqlite3

class BaseException(Exception):
   pass

class Data_Base():
    def __init__(self, base_name:str, code:str = None) -> None:
        DB = sqlite3.connect(base_name)
        Sql = DB.cursor()
        """запуск инициализации таблиц"""
        if code != None:
            exec(code)
            DB.commit()
        """очень нужные атребуты"""
        self.DB = DB
        self.Sql = Sql



    def Add_to_base(self, table_name:str, elements:list)->None:
        """Add elements into table\n
        Elements look like [name, job, sallary]"""

        self._check("Add_to_base", table_name, elements)
        # Временные переменные 
        question_marks = ""
        args_string = ""
        i = 0 
        # Генератор SQL комманды
        while i < len(elements):
            question_marks = question_marks + "?, "
            args_string = args_string + f"elements[{i}],"
            i = i + 1
        # Вызов
        exec(f'self.Sql.execute("INSERT INTO {table_name} VALUES ({question_marks[0:-2]})",({args_string[0:-1]}))' )
        self.DB.commit()



    def Get_from_base(self, table_name:str, column:str="*", condition:str=None)->tuple:
        """Get lines or values from data base\n
        with condition get values from cell\n
        without condition get line or all lines (if not fill argument 'column')"""

        self._check("Get_from_base", table_name, column)
        if condition:
            return(tuple(self.Sql.execute(f"SELECT {column} FROM {table_name} WHERE {condition}")))
        else:
            return(tuple(self.Sql.execute(f"SELECT {column} FROM {table_name}")))



    def Delete_from_base(self, table_name:str, condition:str)->None:
        """Deletes lines according to the specified condition\n
        If you specify 'ALL' as a condition, all values in the table will be deleted"""

        self._check("Delete_from_base", table_name)
        if condition != "ALL":
            self.Sql.execute(f"DELETE FROM {table_name} WHERE {condition}")
        else:
            self.Sql.execute(f"DELETE FROM {table_name}")
        self.DB.commit()



    def Update_base(self, table_name:str, column:str, condition:str, new_value)->None:
        """Updates the values in the cells of the lines according to the condition"""
        self._check("Update_base", table_name, column, new_value)
        self.Sql.execute(f'UPDATE {table_name} SET {column} = {new_value} WHERE {condition}')
        self.DB.commit()
        


    def Get_count(self, table_name:str)->int:
        """Gets the count of lines"""
        self._check("Get_count",table_name)
        return(tuple(self.Sql.execute(f"SELECT count(*) FROM {table_name}")))[0][0]



    def Exists_in_base(self,table_name:str, column:str, value:str)->bool:
        """Checks if there is an argument in the database"""
        self._check("Exists_in_base",table_name,column)
        if tuple(self.Sql.execute(f"SELECT {column} FROM {table_name} WHERE {column} = '{value}'")):
            return(True)
        else:
            return(False)



    def _check(self,context:str, argc = None, argv = None, argz = None): # Защита от дуры маши
        """Foolproof"""
        if context == "Add_to_base":
            table_name = argc
            elements = argv
            tabs = tuple(self.Sql.execute(f'pragma table_info({table_name});'))

            self._check_table(table_name)

            if len(elements) != len(tabs): # Проверка на совпадение количество переданных аргументов и требуемых 
                tmp = ""
                for item in tabs:
                    tmp = tmp + f"{item[1]}-{item[2]}, "
                tmp = tmp[0:-2]
                raise BaseException(f"Count of gived elements not equal count of needed elements.\nFor this table need '{tmp}'")
            
            i = 0
            while i < len(elements): # проверка на совпадение типов
                if not str(type(elements[i])) == str(tabs[i][2]).replace('TEXT',"<class 'str'>").replace("INT","<class 'int'>"):
                    need = str(tabs[i][2]).replace('TEXT',"'str'").replace("INT","'int'")
                    gived =str(type(elements[i])).replace("<class 'str'>", "'str'").replace("<class 'int'>","'int")
                    raise BaseException(f"Wrong type of element, must be {need} not a {gived} in {i} element")
                i = i + 1
        
        if context == "Exists_in_base":
            table_name = argc
            column = argv
            self._check_table(table_name)
            self._check_column(table_name,column)
        
        if context == "Get_from_base":
            self._check_table(argc)
            self._check_column(argc,argv)
        
        if context == "Get_count":
            self._check_table(argc)

        if context == "Update_base":
            self._check_table(argc)
            self._check_column(argc,argv)
            tabs = (tuple(self.Sql.execute(f'pragma table_info({argc});')))
            for tab in tabs:
                if tab[1] == argv and not str(type(argz)) == str(tab[2]).replace('TEXT',"<class 'str'>").replace("INT","<class 'int'>"):
                    need = str(tab[2]).replace('TEXT',"'str'").replace("INT","'int'")
                    gived =str(type(argz)).replace("<class 'str'>", "'str'").replace("<class 'int'>","'int")
                    raise BaseException(f"Wrong type of argument, must be {need} not a {gived}")


        if context == "Delete_from_base":
            self._check_table(argc)
        

                    
    def _check_table(self,table_name):
        tabs = tuple(self.Sql.execute(f'pragma table_info({table_name});'))
        if not tabs: # Проверка на существование требуемой таблицы
            tmp = ""
            for table in tuple(self.Sql.execute(f"select * from sqlite_master where type = 'table'")):
                tmp = tmp + table[1] + ", "
            raise BaseException(f"This table not exists: '{table_name}'\nYou have only '{tmp[0:-2]}' tables")



    def _check_column(self,table_name,column):
            tabs = tuple(self.Sql.execute(f'pragma table_info({table_name});'))
            exists = None
            tmp = ""
            for item in tabs:
                tmp = tmp + item[1]+ ", "
                if column == item[1] or column == "*":
                    exists = True
            if not exists:
                raise BaseException(f"This column not exists: '{column}'\nYou have only '{tmp[0:-2]}' columns")




if __name__ == "__main__":


    print("Запуск базы")

    string= """
Sql.execute(\"\"\"CREATE TABLE IF NOT EXISTS aneks (
    text TEXT,
    genre TEXT,
    addby TEXT,
    views INT,
    rating INT
)
\"\"\")
Sql.execute(\"\"\"CREATE TABLE IF NOT EXISTS users (
    id INT,
    username TEXT,
    views INT,
    adds INT,
    role TEXT
)
\"\"\")
"""


    a = Data_Base("BASE.db",string)                                     # Имя с путем в первом аргументе и код инициализации таблиц во втором (не обязательно)
    #a.Add_to_base("aneks",["first","second","3",4,5])                  # Добовление в базу
    #print(a.Exists_in_base("aneks","text","first"))                    # Проверка на сущетвования элемета в базе
    #print(a.Get_from_base(table_name="users",column="views",condition="username = 'mashkachan'"))    
    #print(a.Get_count("users"))                                        # Получение количества
    #a.Update_base("users","views","username = 'mashkachan'", 1)        # Обновление
    #a.Delete_from_base("aneks", "ALL")                                 # Удаление
    