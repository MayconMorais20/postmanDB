import pymysql, jwt, base64
from pymysql.cursors import DictCursor 

class Db():
    def __init__(self, post_body, local):
        self.local = local
        self.cur = None
        self.error = None
        self.conn = self.connect(post_body)
        
    def log(self, message: str):
        self.count = +1
        print(f"LOG - {self.count} :", message)

    def execute(self, query):
        """this method execute query in format string  """

        #execute query on database selected
        """tratamento para definir a base de dados"""
        database = ""
        if '$' in query:
            database_split = query.split("$")
            database = database_split[1]
            query = query.replace("$","")
        table = ""

        if '@' in query:
            table_split = query.split("@")
            table = table_split[1]
            query = query.replace("@","")
        print(">>",database, table)   
        
        query_columns = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{database}' AND TABLE_NAME = '{table}';"
        try:
            #get query result
            result_query = []
            self.cur.execute(query)
        
            for r in self.cur:
                result_query.append(r)  

            #get colums from database.table
            self.cur.execute(query_columns)
            columns = self.cur.fetchall()
            
            result = []

            #join columns and data
            for i in range(len(result_query)):
                row = {}
                for j in range(len(columns)):
                    cl = str(columns[j])
                    cl = cl.replace("('","")
                    cl = cl.replace("',)","")
                    row.update({cl : result_query[i][j]})
                result.append(row)

            self.cur.close()

            
        except Exception as e:
            print(e)
            return {"data": {"type":"Invalid query","query_status":"FAIL"}}
        return {"data": {"response":result, "query_status":"SUCESS"} if result != [] else {"response":"no result from this query command", "query_status":"SUCESS"}}

    def connect(self, post_body):
        try:
            if self.local:
                self.conn = pymysql.connect(host="localhost", user="root", password="root", db="ra_dse", port=3306)
            else:
                try:
                    #validate secret
                    token = jwt.decode(post_body.token, base64.b64decode(post_body.secretdecode) , algorithms=["HS256"])
                    print(token)
                except Exception as e:
                    self.error = {"message":"Incorrect secret word"}

                    raise Exception(self.error)

                #validate fields 
                required = {"host":False,"user":False,"password":False,"database":False}
                for i in token.keys():
                    if i in required:
                        required[i] = True

                required_key = []
                for j in required.keys():
                    if not required[j]:
                        required_key.append(j)

                if any(required_key):
                    self.error = {"message":"token not contains required field(s): " + str(required_key)}
                    raise Exception(self.error)
                
                self.conn = pymysql.connect(host=token["host"], user=token["user"], password=token["password"], db=token["database"], port=3306)

            self.cur = self.conn.cursor()
            self.log("connected to database")

        except Exception as e:
            self.log("has a problem to connect database: " + str(e))

    