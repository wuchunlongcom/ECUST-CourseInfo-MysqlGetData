# mysql
# def getData(sql):
#     import pymysql
#     db = pymysql.Connect(host="127.0.0.1",
#                          user="root",
#                          password="12345678",
#                          port=3306,
#                          db="studb",
#                          charset="utf8")
#     
#     cur = db.cursor()
#     cur.execute(sql)
#     result = cur.fetchall()
#     ret = [[j or '' for j in i] for i in result]
#     cur.close
#     db.close()
#     return ret    