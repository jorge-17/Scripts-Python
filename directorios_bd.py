import os, sys
import psycopg2


#Funcion que registra la clave en un archivo de texto
def registro_clave(clave):
    file=open("claves.txt", "a")
    file.write(clave)
    file.close()

#Funcion que registra la ruta en un archivo de texto
def registro_path(path):
    file=open("registros.txt","a")
    file.write(path)
    file.close()

#Funcion que registra en la base de datos la ruta, la clave(folder), el tamaño, y la ruta de descarga
def insertar_registro(path, folder, tamaño, down_path):
    #sentencia INSERT INTO
	sql="INSERT INTO rutas (path, folder, tamaño, download_path) VALUES (%s, %s, %s, %s);"


	conn=None    
	data=(path, folder, tamaño, down_path)

	try:
        #Conexion al servidor ine-postgresql.ciatec.int y a la base de datos dev-inegi usarndo usuarios
		conn=psycopg2.connect(host="ine-postgresql.ciatec.int", database="dev-inegi", user="dev-inegi", password="76DB*ine")
		cur=conn.cursor()
        #Se ejecuta la sentencia en la base de datos especificados
		cur.execute(sql,data)

        #Se actualiza la base de datos para mostrar los registros ingresados
		conn.commit()

        #Se cierra la conexion al realizar el registro de forma correcta
		cur.close()        
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


#Funcion para realizar la actualizacion en la base de datos dentro de la tabla rutas
def actualizar_registro_rutas(folder, path_down, path):

    #Se definen las consultas UPDATE a ejecutar en la base de datos
    sql="UPDATE rutas SET path=%s, download_path=%s WHERE folder=%s;"
    

    conn=None
    data=(path, path_down, folder)
    

    try:
        #Conexion al servidor ine-postgresql.ciatec.int y a la base de datos dev-inegi usarndo usuarios
        conn=psycopg2.connect(host="ine-postgresql.ciatec.int", database="dev-inegi", user="dev-inegi", password="76DB*ine")
        cur=conn.cursor()
        #Se ejecuta la sentencia en la base de datos especificados
        cur.execute(sql, data)

        #Se actualiza la base de datos para mostrar los registros ingresados
        conn.commit()

        #Se cierra la conexion al realizar el registro de forma correcta
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


#Funcion para realizar la actualizacion en la base de datos dentro de la tabla metadatos
def actualizar_registro_metadatos(clvlidar, path):
    #Se definen las consultas UPDATE a ejecutar en la base de datos
    sql="UPDATE metadatos SET path=%s WHERE clvlidar=%s;"

    conn=None
    data=(path, clvlidar)

    try:
        #Conexion al servidor ine-postgresql.ciatec.int y a la base de datos dev-inegi usarndo usuarios
        conn=psycopg2.connect(host="ine-postgresql.ciatec.int", database="dev-inegi", user="dev-inegi", password="76DB*ine")
        cur=conn.cursor()
        #Se ejecuta la sentencia en la base de datos especificados
        cur.execute(sql, data)
        #Se actualiza la base de datos para mostrar los registros ingresados
        conn.commit()
        #Se cierra la conexion al realizar el registro de forma correcta
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#Ruta de la carpeta de la cual se haran las converciones
#Siempre se comenzara con /MDE_Nuber_Lidar_INEGI y se ira modificando las demas
#carpetas conforme sea necesario---------------------------------------------------------
root="/Guanajuato"
#-----------------------------------------------------------------------------------------
path_origin="E:\MDE_Nuber_Lidar_INEGI"+root
#path_destiny="F:/MDE_Nuber_Lidar_INEGI_bin"+root
#Raices de las rutas que seran registradas en la base de datos
path_root_bd="http://187.174.175.168:8089/pruebas/LiDAR/MDE_Nuber_Lidar_INEGI_bin"+root
path_root_bd_down="http://187.174.175.168:8089/pruebas/LiDAR/MDE_Nuber_Lidar_INEGI_rar"+root
path_root_xml="http://187.174.175.168:8089/pruebas/LiDAR/MDE_Nuber_Lidar_INEGI_bin"+root

#Se obtiene un arreglo de todos los directorios dentro del dierectorio original
dirs_origin=os.listdir(path_origin)
#dirs_dest=os.listdir(path_destiny)

#Se inicializan contadores para la visualizacion de los progresos
i=1
x=1
y=1

#Se recorre el primer arreglo y cada elemento es llamado como cosa
for cosa in dirs_origin:
    print("-----------------------------"+cosa+"--------------------------------------")
    #total=len(dirs_origin)
    #string=str(i)+"/"+str(total)
    #print(cosa+" "+string)
    #Se concatena el primer directorio accesado a la direccion de origen
    path_origin2=path_origin+"/"+cosa
    path_root="/"+cosa
    print(path_root)
    #path_destiny2=path_destiny+"/"+cosa
    #Se genera un segundo arreglo con los elementos que contiene el directorio al que se ingreso
    dirs_origin2=os.listdir(path_origin2)
    #Se recorre el segundo arreglo y cada elemento dentro de este es llamado cosa2
    for cosa2 in dirs_origin2:
        print("-----------------------------"+cosa2+"--------------------------------------")
        #total2=len(dirs_origin2)
        #print("-------"+cosa2+" "+str(x)+"/"+str(total2))
        #Se concatena el directorio creado anteriormente y el elemento actual
        path_origin3=path_origin2+"/"+cosa2
        path_root2=path_root+"/"+cosa2
        print(path_root2)
        #path_destiny3=path_destiny2+"/"+cosa2
        #Se genera un ultimo arreglo en el cual se almacenaran todos los elementos del directorio
        dirs_origin3=os.listdir(path_origin3)
        for cosa3 in dirs_origin3:
            #total3=len(dirs_origin3)
            #porcentaje3=y/total3
            #print("--------->"+cosa3+" "+str(porcentaje3*100))
            #comando="PotreeConverter.exe "+path_origin3+"/"+cosa3+" -o "+path_destiny3+"/"+cosa3
            #resultado=os.popen(comando).read()
            #Se crean las rutas de la nube de puntos, archivos comprimidos y metadatos 
            #que seran registradas en la base de datos
            path_root_final=path_root2+"/"+cosa3+"/cloud.js"
            path_down_final=path_root2+"/"+cosa3+".zip"
            path_xml=path_root2+"/"+cosa3+"/Nube_Puntos_LiDAR_"+cosa3+".xml"
            #Se concatenan las cadenas creadas anteriormente a las rutas que corresponden a cada
            #tipo de rutas
            path=path_root_bd+path_root_final
            path_down=path_root_bd_down+path_down_final            
            path_xml_final=path_root_xml+path_xml            
            #print(path)
            #print(path_down)
            #print(path_xml_final)
            folder=cosa3.lower()
            #folder_xml=folder+"\n"
            #registro_clave(folder_xml)
            #registro_path(path_xml_final)  

            #Se envian los datos a las funciones para realizar el regristro en la BD
            insertar_registro(path,folder,0,path_down)
            actualizar_registro_rutas(folder, path_down, path)
            actualizar_registro_metadatos(folder, path_xml_final)
            y+=1
        x+=1
        y=1
    i+=1
    x=1
print(root)
