import pymysql
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from key import *

class Sql():

    def __init__(self):
            self.conn = None
    def connect(self):
            self.conn = pymysql.connect(host=DB_HOST, user=DB_USER,
                               db=DB_NAME, password=DB_KEY, charset='utf8')

    def save(self,id,img_url,weight,standard_num):
        self.connect()
        cursor = self.conn.cursor() 
        sql = "INSERT INTO carenco.foot_info(url,weight,rdata_id,stand_num) VALUES (%s,%s,%s,%s)"
        #sql = "UPDATE carenco.foot_print_image SET image = %s,weight = %s WHERE id = %s" 
        cursor.execute(sql,(img_url,weight,id,standard_num)) 
        self.conn.commit()

        # sql = "SELECT * FROM carenco.foot_print WHERE id=%s"
        # cursor.execute(sql,(id))
        # result=cursor.fetchall()
        # print(result)

        self.conn.close()  

    def find_description(self,standard_num):
        self.connect()
        cursor = self.conn.cursor() 
      
        sql = "SELECT description FROM carenco.standard WHERE id=%s"
        cursor.execute(sql,(standard_num))
        result=cursor.fetchall()
        #print(result)

        self.conn.close()  

        return result

    def create_health_info(self, data):
        print('- sql -----------------')
        print(data)
        conn = pymysql.connect(host=DB_HOST, user=DB_USER,
                               db=DB_NAME,
                               password=DB_KEY, charset='utf8')
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO foot_print_ocr (weight, muscle, fat) VALUES (%s, %s, %s)"
                cursor.execute(sql, (data['weight'], data['skeletal_muscle_mas'], data['body_fat_mass']))

            conn.commit()

        finally:
            conn.close()
