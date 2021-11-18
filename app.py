from datetime import datetime
from collections import Counter

import flask
from data import *
from werkzeug.wrappers.response import Response

app = flask.Flask(__name__)


@app.context_processor
def provide_menu():
    menu = [
        {
            'name': 'Главная',
            'link': '/',
        }, {
            'name': 'Студенты',
            'link': '/students/',
        }, {
            'name': 'Группы',
            'link': '/groups/',
        }, {
            'name': 'Новости',
            'link': '/news/',
        }, {
            'name': 'Создать',
            'link': '/create/'
        },
    ]
    return {'menu': menu}

@app.context_processor
def context_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def view_index():
    context = {
        'header': 'Web-разработка на Python',
        'description': """<p>Наиболее изветсные веб-фреймворки:</p><ul>
        <li>Django</li>
        <li>Flask</li>
        <li>FASTApi</li> 
        <li>Sanic</li> 
        <li>Tornado</li> 
        <li>Pyramid</li> 
        <li>CherryPy</li> </ul>""",
        'sub_menu': 'Состав продукта',
        'items': [
            {
                'header': 'Список студентов',
                'description': 'Описание чего-либо',
                'link': '/students/',
                'link_name': 'Студенты',
            },
            {
                'header': 'Список групп',
                'description': 'Описание чего-либо',
                'link': '/groups/',
                'link_name': 'Группы',
            },
            {
                'header': 'Новости',
                'description': 'Описание чего-либо',
                'link': '/news/',
                'link_name': 'Новости',
            },
            {
                'header': 'Создать',
                'description': 'Создать нового студента',
                'link': '/create/',
                'link_name': 'Создать',
            },
        ],
    }

    return flask.render_template('index.html', **context)


@app.route('/students/', methods=['GET'])
@app.route('/students/<int:id>/', methods=['GET'])
def view_student(id=None):

    search = flask.request.args.get('search')

    for i in range(len(data)):
        data[i]['id'] = i

    if search:
        search_data = []
        for i in range(len(data)):
            if search.lower() in data[i]['name'].lower():
                search_data.append(data[i])

        context = {
            'students': search_data
        }

        return flask.render_template('students.html', **context)


    context = {
        'students': data
    }

    if id is None:
        return flask.render_template('students.html', **context)

    person = {}
    for i in range(len(data)):
        if data[i]['id'] == id:
            person = data[i]

    if person is None:
        return flask.abort(Response('Студент не найден'))

    return flask.render_template('student.html', person=person)


@app.route('/groups/')
def view_groups():
    group = [item['group'] for item in data]

    count = Counter()
    for p in group:
        count[p] += 1

    info_group = dict(count)

    return flask.render_template('groups.html', group=group, info_group=info_group, data=data)


@app.route('/news/')
def view_news():
    context = {
        "news": news
    }
    return flask.render_template('news.html', **context)


# добавление нового студента
@app.route('/create/', methods=['POST', 'GET'])
def view_create():
    if flask.request.method == 'POST':
        new_student = dict()
        new_student['name'] = flask.request.form['name']
        new_student['group'] = flask.request.form['group']
        new_student['email'] = flask.request.form['email']
        data.append(new_student)
        return flask.render_template('student.html', person=new_student)
    else:
        return flask.render_template('create.html')



if __name__ == '__main__':
    app.run(debug=True)
