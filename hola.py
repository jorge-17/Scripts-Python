import psycopg2
import wxPython.wx

def insert_registro(clave, path,x):
    sql="INSERT INTO metadatos (ClvLiDAR, Path) VALUES (%s, %s);"

    con=None
    data=(clave, path)

    try:
        con=psycopg2.connect(host="ine-postgresql.ciatec.int", database="dev-inegi", user="dev-inegi", password="76DB*ine")
        cursor=con.cursor()
        cursor.execute(sql, data)
        con.commit()
        cursor.close()
        print(x)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()


if __name__=="__main__":
    #archi_claves=open("claves.txt","r")
    #archi_path=open("registros.txt","r")
    #rows_claves=archi_claves.readlines()
    #rows_path=archi_path.readlines()
    #x=0
    #for i in rows_claves:
    #    insert_registro(rows_claves[x][:-1],rows_path[x][:-1],x)
    #    #print(rows_claves[x]+"-"+rows_path[x])        
    #    x=x+1
    hola="hola"
    hola_path="hola/path"
    insert_registro(hola, hola_path, 2)