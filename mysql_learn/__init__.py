import pymysql.cursors
with pymysql.connect("127.0.0.1","root","123456","my1",3306)  as cursor:

    sql = "select * from t where a=%s"

    line = cursor.execute(sql,args=(20,))

    res = cursor.fetchall()

    print(res)




