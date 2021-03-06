#To Do List:
from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL

app = Flask(__name__)

#Configuración de la BBDD:
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'todolist'

#Conexión a la BBDD:
mysql = MySQL(app)


#Mis Endpoints:

#Crear Nota:
@app.route('/create-task', methods=['GET','POST'])
def todo_list():
    '''
    Función que permitirá Insertar registros recibiendolos mediante el formulario de HTML a la BBDD
    '''

    if request.method == 'POST':
        task = request.form['task']

        #cursor:
        cursor = mysql.connection.cursor()

        #Consulta:
        cursor.execute('INSERT INTO lista VALUES (NULL, %s)', [task])

        #commit:
        cursor.connection.commit()

        return redirect(url_for('task_list'))

    return render_template('create.html')



#Mostrar mis notas:
@app.route('/task-list')
def task_list():
    '''Función que se encarga de seleccionar todos los registros almacenados en la BBDD, almacenarlos en una variable (en forma de lista) para luego ser mostrados en HTML'''
    
    #cursor:
    cursor = mysql.connection.cursor()

    #Consulta:
    cursor.execute('SELECT * FROM lista')

    tasks = cursor.fetchall()

    cursor.close()

    return render_template('list.html', tasks=tasks)




#Borrar Notas:
@app.route('/delete/<id_task>')
def delete_task(id_task):
    '''
    Función que eliminará los registros de la BBDD recibiendo como parámetro por la URL el id del elemento a borrar. Parámetros:
    -id_task: la PK del elemento para así eliminarse al hacerse la consulta
    '''
    
    #cursor:
    cursor = mysql.connection.cursor()

    #Consulta:
    cursor.execute('DELETE FROM lista WHERE id = %s', [id_task])

    #commit:
    cursor.connection.commit()

    return redirect(url_for('task_list'))



#Editar tarea:
@app.route('/edit-task/<int:id_task>', methods=['GET','POST'])
def edit_task(id_task):
    '''
    Función que actualizará/editar los registros de la BBDD recibiendo como parámetro por la URL el id del elemento. Parámetros:
    -id_task: la PK del elemento para así hacer el UPDATE en la consulta    
    '''

    if request.method == 'POST':
        new_titulo = request.form['task']

        #cursor:
        cursor = mysql.connection.cursor()

        #Consulta:
        cursor.execute('UPDATE lista SET Titulo = %s WHERE id = %s', (new_titulo, id_task))

        #commit:
        cursor.connection.commit()

        return redirect(url_for('task_list'))

    #Los datos que se pasarán mediante la URL para poder elegir la tarea mediante su id seleccionandose 
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM lista')

    tasks = cursor.fetchall()

    cursor.close()

    return render_template('create.html', tasks=tasks[0])


if __name__== '__main__':
    app.run(debug=True)
