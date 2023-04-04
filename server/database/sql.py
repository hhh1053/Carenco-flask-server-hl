import pymysql


class Sql():

    def save(self, id, img_url, weight):
        conn = pymysql.connect(host='database-1.c5pmtrhecz2d.ap-northeast-1.rds.amazonaws.com', user='admin',
                               db='carenco', password='zpdjdpszh', charset='utf8')
        cursor = conn.cursor()
        sql = "UPDATE carenco.foot_print SET image = %s,weight = %s WHERE id = %s"
        cursor.execute(sql, (img_url, weight, id))
        conn.commit()

        # sql = "SELECT * FROM carenco.foot_print WHERE id=%s"
        # cursor.execute(sql,(id))
        # result=cursor.fetchall()
        # print(result)

        conn.close()

    def create_health_info(self, data):
        print('- sql -----------------')
        print(data)
        conn = pymysql.connect(host='database-1.c5pmtrhecz2d.ap-northeast-1.rds.amazonaws.com', user='admin',
                               db='carenco',
                               password='zpdjdpszh', charset='utf8')
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO foot_print_ocr (weight, muscle, fat) VALUES (%s, %s, %s)"
                cursor.execute(sql, (data['weight'], data['skeletal_muscle_mas'], data['body_fat_mass']))

            conn.commit()

        finally:
            conn.close()
