from flask import Flask, render_template, abort

app = Flask(__name__)

name = "Владимир"

@app.get("/")
def home():
    return render_template("index.html")

'''
@app.route("/names")
def names():
    return render_template('names.html', name = name)
'''

@app.get("/names")
def names():
    entities = list()
    with open("files/names.txt", encoding="utf-8") as f:
        for raw_line in f:
            entities.append(raw_line.strip())
    return render_template('names.html', entities = entities)


@app.get("/table")
def humans():
    entities = list()
    with open("files/humans.txt", encoding="utf-8") as f:
        for raw_line in f:
            data = raw_line.strip().split(';')
            keys = ['last_name', 'name', 'surname']
            item = dict()
            for i in range(len(data)):
                item[keys[i]] = data[i]
            entities.append(item)
    return render_template('table.html', entities = entities)
'''
Или можно так создать таблицу
data = raw_line.strip().split(';')
entities.append({'last_name': data[0], 
                               'name': data[1], 'surname': data[2]})
'''

@app.route('/users')
def users_list():
    entities = list()
    with open("files/users.txt", encoding="utf-8") as f:
        for raw_line in f:
            data = raw_line.strip().split(';')
            keys = ['username', 'last_name', 'name', 
                    'surname', 'birth_date', 'phone_number']
            item = dict()
            for i in range(len(data)):
                item[keys[i]] = data[i]
            entities.append(item)
    return render_template('users_list.html', entities = entities)

'''и можно еще сделать вот так **{'entities': entities}'''

'''Можно еще создать вот так            
entities.append(dict(zip(('login', 'last_name', 'name',
                     'surname', 'birth_date', 'phone'), data))'''


@app.route("/users/<login>")
def user_item(login):
    item = None
    with open('files/users.txt', encoding="utf-8") as f:
        for raw_line in f:
            data = raw_line.strip().split(';')
            if data[0] == login:
                item = {
                    'login': data[0],
                    'last_name': data[1],
                    'name': data[2],
                    'surname': data[3],
                    'birth_date': data[4],
                    'phone': data[5]
                }
                break
    if item is None:
        abort(404, f'User with login: {login} not found')
    return render_template('user_info.html', item=item)

'''
@app.route('/users/<login>')
def user_item(login):
    entities = list()
    user = list()
    with open("files/users.txt", encoding="utf-8") as f:
        for raw_line in f:
            data = raw_line.strip().split(';')
            keys = ['username', 'last_name', 'name', 
                    'surname', 'birth_date', 'phone_number']
            item = dict()
            for i in range(len(data)):
                item[keys[i]] = data[i]
            entities.append(item)
    for e in entities:
        if e['username'] == login:
            user.append(e)
    if len(user) == 0:
        abort(404, f'User with login: {login} not found')    
    return render_template('user_item.html', user = user)
'''


'''
@app.route('/posts/<int:post_id>')
def show_post(post_id):
    # показывает статью по её id (int)
    return f'Post {post_id}'
'''


@app.route("/about")
def about():
    return "О нас"

if __name__ == "__main__":
    app.run(debug=True)
