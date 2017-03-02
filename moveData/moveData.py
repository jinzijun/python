# coding: utf-8
import MySQLdb
import sys
import ConfigParser
#############################################################
'''
                    配置区
'''
'''
    源数据库配置信息
'''
Source_MySQL_Host = "127.0.0.1"
Source_MySQL_Port = 3306
Source_MySQL_User = "user"
Source_MySQL_Password = "*****"
Source_MySQL_Connect_TimeOut = 2
Source_MySQL_Charset = "utf8"
Source_Database_Name = "user"
'''
    目标数据库配置信息
'''
Target_MySQL_Host = "127.0.0.1"
Target_MySQL_Port = 3306
Target_MySQL_User = "user"
Target_MySQL_Password = "******"
Target_MySQL_Connect_TimeOut = 2
Target_MySQL_Charset = "utf8"
Target_Database_Name = "user"

'''
    Table_Name 表名
'''
Table_Name = "t_user_info"
'''
    Fileds_Name 字段名称，务必拼写正确，且用英文逗号作为间隔    
'''
Fileds_Name = "user_id,user_name,create_time"
'''
    Condition 应以where作为开头。
    如果不添加条件，则应设置 Condition = ""
'''
Condition = "where user_id =123456"
###############################################################

def get_mysql_connection(database):
    """
    根据默认配置返回数据库连接
    :return: 数据库连接
    """
    if database == 'source':
        conn = MySQLdb.connect(
                host=Source_MySQL_Host,
                port=Source_MySQL_Port,
                user=Source_MySQL_User,
                passwd=Source_MySQL_Password,
                connect_timeout=Source_MySQL_Connect_TimeOut,
                charset=Source_MySQL_Charset,
                db=Source_Database_Name
        )
        return conn
    elif database == 'target':
        conn = MySQLdb.connect(
                host=Target_MySQL_Host,
                port=Target_MySQL_Port,
                user=Target_MySQL_User,
                passwd=Target_MySQL_Password,
                connect_timeout=Target_MySQL_Connect_TimeOut,
                charset=Target_MySQL_Charset,
                db=Target_Database_Name
        )
        return conn
    else:
        return None
    
def mysql_exec(database,sql_script):
    """
    执行传入的脚本，返回影响行数
    :param sql_script:
    :param connection:
    :return: 脚本最后一条语句执行影响行数
    """
    try:
        connection = get_mysql_connection(database)
        cursor = connection.cursor()
        cursor.execute(sql_script)
        affect_rows = cursor.rowcount
        connection.commit()
        cursor.close()
        connection.close()
        return affect_rows
    except Exception as ex:
        cursor.close()
        connection.rollback()
        print "Exception={}".format(str(ex))

def mysql_query(database,sql_script):
    """
    执行传入的SQL脚本，并返回查询结果
    :param sql_script:
    :param sql_param:
    :return: 返回SQL查询结果
    """
    try:
        connection = get_mysql_connection(database)
        cursor = connection.cursor()
        cursor.execute(sql_script)
        exec_result = cursor.fetchall()
        cursor.close()
        connection.close()
        return exec_result
    except Exception as ex:
        cursor.close()
        connection.close()
        print "Exception={}".format(str(ex))

def main():
    """
    主函数
    1、清除目标表的旧数据。
    2、到源表中查询数据。
    3、将数据插入至目标表。
    """

    # 1、清除目标表的旧数据。
    delete_sql = "delete from "+ Table_Name +" "+Condition
    deleted_row_count = mysql_exec(database='target',sql_script=delete_sql)
    print "清理了目标表中的%d行旧数据"%(deleted_row_count)
    # 2、到源表中查询数据。
    query_sql = "select "+ Fileds_Name +" from "+ Table_Name + " " + Condition
    query_result = mysql_query(database='source',sql_script=query_sql)
    func_escape_str = MySQLdb.escape_string
    for row in query_result:
        column_value_lst = list()
        column_value_lst_append = column_value_lst.append
        for column in row:
            if type(column) == long or type(column) == int:
                column_value_lst_append(str(column))
            elif type(column) == unicode or type(column) == str:
                column_value_lst_append("\""+func_escape_str(str(column))+"\"")
            elif type(column) == datetime.datetime:
                column_value_lst_append("\""+column.strftime("%Y-%m-%d %H:%M:%S")+"\"")
            else:
                print "find new type in %s:%s"%(Table_Name,str(type(column)))
                column_value_lst_append(str(column))
        # 3、将数据插入至目标表。
        insert_sql = "insert into " + Table_Name + " (" + Fileds_Name + ") values (" + ",".join(column_value_lst) + ")"
        mysql_exec(database='target',sql_script=insert_sql)
    print "数据插入完毕，程序退出。"

if __name__ == '__main__':
    reload(sys)  
    sys.setdefaultencoding('utf8')
    main()
    sys.exit()

def test_delete():
    '''
        测试删除功能
    '''
    delete_sql = "delete from "+ Table_Name +" "+Condition
    deleted_row_count = mysql_exec(database='target',sql_script=delete_sql)
    print "清理了目标表中的%d行旧数据"%(deleted_row_count)

def test_query_insert():
    '''
        测试查询和插入
    '''
    # 2、到源表中查询数据。
    query_sql = "select "+ Fileds_Name +" from "+ Table_Name + " " + Condition
    query_result = mysql_query(database='source',sql_script=query_sql)
    func_escape_str = MySQLdb.escape_string
    for row in query_result:
        column_value_lst = list()
        column_value_lst_append = column_value_lst.append
        for column in row:
            if type(column) == long or type(column) == int:
                column_value_lst_append(str(column))
            elif type(column) == unicode or type(column) == str:
                column_value_lst_append("\""+func_escape_str(str(column))+"\"")
            elif type(column) == datetime.datetime:
                column_value_lst_append("\""+column.strftime("%Y-%m-%d %H:%M:%S")+"\"")
            else:
                print "find new type in %s:%s"%(Table_Name,str(type(column)))
                column_value_lst_append(str(column))
        # 3、将数据插入至目标表。
        insert_sql = "insert into " + Table_Name + " (" + Fileds_Name + ") values (" + ",".join(column_value_lst) + ")"
        mysql_exec(database='target',sql_script=insert_sql)
    print "数据插入完毕，程序退出。"
