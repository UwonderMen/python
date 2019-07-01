import pymysql

with pymysql.connect("127.0.0.1","root","123456","my1",3306)  as cursor:

    sql = "insert into t(a,b) values(10,8)"

    res = cursor.execute(sql)

    print()




