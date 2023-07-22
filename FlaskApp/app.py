# from flask import Flask,render_template,request,json
# from flaskext.mysql import MySQL
# #from werkzeug import generate_password_hash



# mysql = MySQL()

# app = Flask(__name__)
# # MySQL configurations 
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'Jyo4704@my_sql'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)



# @app.route("/")
# def main():
#     return render_template('index.html')
# @app.route('/signup')
# def signup():
#     return render_template('signup.html')


# @app.route('/api/signup', methods=['POST']) #/api/signup is the name of the api
# def signUp():
#     try:
#         name = request.form['inputName']
#         email = request.form['inputEmail']
#         password = request.form['inputPassword']

#         # validate the received values
#         if name and email and password:

#             # All Good, let's call MySQL

#             conn = mysql.connect()
#             cursor = conn.cursor()
#             #hashed_password = generate_password_hash(password) #hashing the password for security
#             cursor.callproc('sp_createUser', (name, email, password))
#             data = cursor.fetchall()

#             if len(data) is 0:
#                 conn.commit()
#                 return json.dumps({'message': 'User created successfully !'})
#                 # json.dumps: python obj to json string
#                 # when ever there is a network call, it has to be converted to json
#             else:
#                 return json.dumps({'error': str(data[0])})
#         else:
#             return json.dumps({'html': '<span>Enter the required fields</span>'})

#     except Exception as e:
#         return json.dumps({'error': str(e)})
#     finally:
#         cursor.close()
#         conn.close()
#         # database connections are costly and has limited no. of conn and traffic is heavy
#         # therefore when the connection is not required, it's better to close the conn for someone else to access
    

# if __name__ == "__main__":
#     app.run()

from flask import Flask, render_template, json, request, session, redirect
from flaskext.mysql import MySQL
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'abcd'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Jyo4704@my_sql'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signup')
def showSignUp():
    return render_template('signup.html')


@app.route('/api/signup', methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        conn = mysql.connect()
        cursor = conn.cursor()

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            
            # _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    finally:
        cursor.close()
        conn.close()

    # except Exception as e:
    #     return json.dumps({'error': str(e)})
    
@app.route('/signin')
def showSignin():
    return render_template('signin.html')

@app.route('/api/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        # connect to mysql 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        if len(data) > 0:
            print(data,'data is: ')
            print(_password,'password: ')
            if (str(data[0][3]) ==  _password):
                session['user'] = data[0][0]
                return redirect('/userhome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/userhome')
def userHome():
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')

@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish',(_title,_description,_user))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect('/userhome')
            else:
                return render_template('error.html',error = 'An error occurred!')
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))      

if __name__ == "__main__":
    app.run()
