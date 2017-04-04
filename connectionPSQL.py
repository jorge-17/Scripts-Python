import psycopg2

def insertar_registro(path, folder, tamaño, down_path):
	sql="INSERT INTO rutas (path, folder, tamaño, download_path) VALUES (%s, %s, %s, %s);"

	conn=None
	data=(path, folder, tamaño, down_path)

	try:
		conn=psycopg2.connect(host="ine-postgresql.ciatec.int", database="dev-inegi", user="dev-inegi", password="76DB*ine")
		cur=conn.cursor()
		cur.execute(sql,data)
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

if __name__ == '__main__':
	insertar_registro("http://ine-web-dev/pruebas/Aguascalientes_bin/AGS1/F13B77/F13B77a3/cloud.js","f13b77a3",5.5,
	"http://ine-web-dev/pruebas/Aguascalientes_rar/AGS1/F13B77/F13B77a3.rar")