import pymysql.cursors
import sqlite3

class usuari(object):

    def carregaUsuaris():
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='reserves',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT * from usuaris"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery


    def eliminaUsuari(id_usuari):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='reserves',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="DELETE from usuaris WHERE id_usuari="+str(id_usuari)
        cursor.execute(sql)
        db.close()

    def guardaUsuari(nom, llinatges, telefon):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='reserves',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="INSERT INTO usuaris(nom,llinatges,telefon) VALUES ('"+nom+"','"+llinatges+"','"+telefon+"');"
        cursor.execute(sql)
        db.close()

    def editarUsuari(id_usuari):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='reserves',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()        
        sql="SELECT * from usuaris WHERE id_usuari='"+id_usuari+"'"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery    

    def actualitzarUsuari(id_usuari, nom, llinatges, telefon):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='reserves',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        
       
        cursor.execute("UPDATE usuaris SET nom = %s, llinatges = %s, telefon = %s WHERE id_usuari = %s", 
               (nom, llinatges, telefon, id_usuari))
        db.close()

class reserva(object):  
    def guardaReserva(data, nom, instalacio, setmana,):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='reserves',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        cursor.execute('insert into reserves(data, id_usuari, tipus, setmana) values(%s, %s, %s, %s)', (data, nom, instalacio, setmana))
        db.close()  

    def carregaReserves():
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='reserves',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT * from reserves"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery    

    def carregaReservesPerSetmana(setmana):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='reserves',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()        
        cursor.execute("SELECT * from reserves WHERE setmana=%s ORDER BY data ASC",(setmana))       
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery          