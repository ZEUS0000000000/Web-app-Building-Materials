from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy as sa
import pyodbc
# python -m http.server 5000
# http://localhost:5000/


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://Andrey:Andrey@SQL2017/BuildingMaterials?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cache = Cache(app)
cache.clear()

class Плотность_и_цена(db.Model):
    __tablename__ = "Плотность_и_цена"
    id_Цена = Column(Integer, primary_key=True)
    Материал = Column(String(50), nullable=True)
    Плотность = Column(Integer, nullable=True)
    Цена = Column(String(50), nullable=True)


class Обработка_и_растяжение(db.Model):
    __tablename__ = "Обработка_и_растяжение"
    id = Column(Integer, primary_key=True)
    Материал = Column(String(50))
    Прочность_растяжения = Column(Integer, nullable=True)
    Способ_обработки = Column(String(50), nullable=True)
    id_Цена = Column(Integer, ForeignKey('Плотность_и_цена'))
    id_Сложность = Column(Integer, ForeignKey('Сложность_и_популярность'))
    СвязьПлотность = relationship('Плотность_и_цена', backref='Обработка_и_растяжение')
    СвязьСложность = relationship('Сложность_и_популярность', backref='Обработка_и_растяжение')


class Сложность_и_популярность(db.Model):
    __tablename__ = "Сложность_и_популярность"
    id_Сложность = Column(Integer, primary_key=True)
    Материал = Column(String(50), nullable=True)
    Сложность_изготовления = Column(String(50), nullable=True)
    Популярность = Column(Integer, nullable=True)


# Подключение к БД   
def connect_db(db_name):
    #engine = create_engine(f'mssql+pyodbc://user:password@host/db?driver=SQL+Server')
    #                        'mssql+pyodbc://sa:sa@TS2018/MyDataBase?driver=SQL+Server'
    connect_str = "mssql+pyodbc://SQL2017/" + db_name + "?driver=SQL+Server"
    engine = sa.create_engine(connect_str, echo=False)
    Session = sessionmaker(bind=engine)
    return Session()


# Роут для отображения информации о всех материалах
@app.route('/')
def index():
    Табл1 = db.session.query(Плотность_и_цена).all()
    Табл2 = db.session.query(Обработка_и_растяжение).all()
    Табл3 = db.session.query(Сложность_и_популярность).all()
    return render_template('index.html', Табл1=Табл1, Табл2=Табл2, Табл3=Табл3)

# Роут для отображения информации о всех материалах
@app.route('/index1.html')
def index1():
    Табл1 = db.session.query(Плотность_и_цена).all()
    Табл2 = db.session.query(Обработка_и_растяжение).all()
    Табл3 = db.session.query(Сложность_и_популярность).all()
    return render_template('index1.html', Табл1=Табл1, Табл2=Табл2, Табл3=Табл3)

# Роут для отображения информации о всех материалах
@app.route('/index2.html')
def index2():
    Табл1 = db.session.query(Плотность_и_цена).all()
    Табл2 = db.session.query(Обработка_и_растяжение).all()
    Табл3 = db.session.query(Сложность_и_популярность).all()
    return render_template('index2.html', Табл1=Табл1, Табл2=Табл2, Табл3=Табл3)

# Роут для отображения информации о всех материалах
@app.route('/index3.html')
def index3():
    Табл1 = db.session.query(Плотность_и_цена).all()
    Табл2 = db.session.query(Обработка_и_растяжение).all()
    Табл3 = db.session.query(Сложность_и_популярность).all()
    return render_template('index3.html', Табл1=Табл1, Табл2=Табл2, Табл3=Табл3)

@app.route('/index_аналитика.html')
def index_аналитика():
    return render_template('index_аналитика.html')





# Роут для добавления материала
@app.route('/add1', methods = ['GET', 'POST'])
def add1():
    if request.method == 'POST':
        Объект1_Материал = request.form['Материал']
        Объект1_Плотность = request.form['Плотность']
        Объект1_Цена = request.form['Цена']


        Объект1 = Плотность_и_цена(Материал=Объект1_Материал,
                                   Плотность=Объект1_Плотность,
                                   Цена=Объект1_Цена)
        db.session.add(Объект1)
        db.session.commit()

    return redirect(url_for('index1'))

# Роут для добавления материала
@app.route('/add2', methods = ['GET', 'POST'])
def add2():
    if request.method == 'POST':
        Объект2_Материал = request.form['Материал']
        id_Цена = request.form['id_Цена']
        id_Сложность = request.form['id_Сложность']
        Объект2_Прочность_растяжения = request.form['Прочность_растяжения']
        Объект2_Способ_обработки= request.form['Способ_обработки']

        Объект2 = Обработка_и_растяжение(Материал=Объект2_Материал,
                                        id_Цена=id_Цена,
                                        id_Сложность=id_Сложность,
                                        Прочность_растяжения=Объект2_Прочность_растяжения,
                                        Способ_обработки=Объект2_Способ_обработки)
        db.session.add(Объект2)
        db.session.commit()

    return redirect(url_for('index2'))

# Роут для добавления материала
@app.route('/add3', methods = ['GET', 'POST'])
def add3():
    if request.method == 'POST':
        Объект3_Материал = request.form['Материал']
        Объект3_Сложность_изготовления = request.form['Сложность_изготовления']
        Объект3_Популярность= request.form['Популярность']

        Объект3 = Сложность_и_популярность(Материал=Объект3_Материал,
                                           Сложность_изготовления=Объект3_Сложность_изготовления,
                                           Популярность=Объект3_Популярность)
        db.session.add(Объект3)
        db.session.commit()

    return redirect(url_for('index3'))




# Роут для изменения материалов
@app.route('/alter1', methods = ['GET', 'POST'])
def alter1():
    if request.method == 'POST':
        id_Цена = int(request.values.get('id_Цена'))
        Объект1_Материал = request.values.get('Материал')
        Объект1_Плотность = int(request.values.get('Плотность'))
        Объект1_Цена = request.values.get('Цена')


        Объект1 = db.session.query(Плотность_и_цена).get(id_Цена)

        if Объект1.id_Цена != id_Цена:
            Объект1.id_Цена = id_Цена
        if Объект1.Материал != Объект1_Материал:
            Объект1.Материал = Объект1_Материал
        if Объект1.Плотность != Объект1_Плотность:
            Объект1.Плотность = Объект1_Плотность
        if Объект1.Цена != Объект1_Цена:
            Объект1.Цена = Объект1_Цена

        db.session.commit()

    return redirect(url_for('index1'))

# Роут для изменения материалов
@app.route('/alter2', methods = ['GET', 'POST'])
def alter2():
    if request.method == 'POST':
        id = int(request.values.get('id'))
        Объект2_Материал = request.values.get('Материал')
        id_Цена = request.values.get('id_Цена')
        id_Сложность = request.values.get('id_Сложность')
        Объект2_Прочность_растяжения = int(request.values.get('Прочность_растяжения'))
        Объект2_Способ_обработки = request.values.get('Способ_обработки')

        Объект2 = db.session.query(Обработка_и_растяжение).get(id)

        if Объект2.id != id:
            Объект2.id = id
        if Объект2.Материал != Объект2_Материал:
            Объект2.Материал = Объект2_Материал
        if Объект2.id_Цена != id_Цена:
            Объект2.id_Цена = id_Цена
        if Объект2.id_Сложность != id_Сложность:
            Объект2.id_Сложность = id_Сложность
        if Объект2.Прочность_растяжения != Объект2_Прочность_растяжения:
            Объект2.Прочность_растяжения = Объект2_Прочность_растяжения
        if Объект2.Способ_обработки != Объект2_Способ_обработки:
            Объект2.Способ_обработки = Объект2_Способ_обработки

        db.session.commit()

    return redirect(url_for('index2'))



# Роут для изменения материалов
@app.route('/alter3', methods = ['GET', 'POST'])
def alter3():
    if request.method == 'POST':
        id_Сложность = int(request.values.get('id_Сложность'))
        Объект3_Материал = request.values.get('Материал')
        Объект3_Сложность_изготовления = request.values.get('Сложность_изготовления')
        Объект3_Популярность = int(request.values.get('Популярность'))

        Объект3 = db.session.query(Сложность_и_популярность).get(id_Сложность)

        if Объект3.id_Сложность != id_Сложность:
            Объект3.id_Сложность = id_Сложность
        if Объект3.Материал != Объект3_Материал:
            Объект3.Материал = Объект3_Материал
        if Объект3.Сложность_изготовления != Объект3_Сложность_изготовления:
            Объект3.Сложность_изготовления = Объект3_Сложность_изготовления
        if Объект3.Популярность != Объект3_Популярность:
            Объект3.Популярность = Объект3_Популярность

        db.session.commit()

    return redirect(url_for('index3'))





# Роут для удаления материалов
@app.route('/remove1', methods = ['GET', 'POST'])
def remove1():
    if request.method == 'POST':
        Объект1_Материал = request.values.get('Материал')
        Объект1_Плотность = int(request.values.get('Плотность'))
        Объект1_Цена = request.values.get('Цена')

        db.session.query(Плотность_и_цена).filter(
                 Плотность_и_цена.Материал == Объект1_Материал,
                          Плотность_и_цена.Плотность == Объект1_Плотность,
                          Плотность_и_цена.Цена == Объект1_Цена).delete()
        db.session.commit()

    return redirect(url_for('index1'))

# Роут для удаления материалов
@app.route('/remove2', methods = ['GET', 'POST'])
def remove2():
    if request.method == 'POST':
        Объект2_Материал = request.values.get('Материал')
        id_Цена = int(request.values.get('id_Цена'))
        id_Сложность = int(request.values.get('id_Сложность'))
        Объект2_Прочность_растяжения = int(request.values.get('Прочность_растяжения'))
        Объект2_Способ_обработки = request.values.get('Способ_обработки')

        db.session.query(Обработка_и_растяжение).filter(
            Обработка_и_растяжение.Материал == Объект2_Материал,
            Обработка_и_растяжение.id_Цена == id_Цена,
            Обработка_и_растяжение.id_Сложность == id_Сложность,
            Обработка_и_растяжение.Прочность_растяжения == Объект2_Прочность_растяжения,
            Обработка_и_растяжение.Способ_обработки == Объект2_Способ_обработки).delete()
        db.session.commit()

    return redirect(url_for('index2'))

# Роут для удаления материалов
@app.route('/remove3', methods = ['GET', 'POST'])
def remove3():
    if request.method == 'POST':
        Объект3_Материал = request.values.get('Материал')
        Объект3_Сложность_изготовления = request.values.get('Сложность_изготовления')
        Объект3_Популярность = int(request.values.get('Популярность'))

        db.session.query(Сложность_и_популярность).filter(
            Сложность_и_популярность.Материал == Объект3_Материал,
                     Сложность_и_популярность.Сложность_изготовления == Объект3_Сложность_изготовления,
                     Сложность_и_популярность.Популярность == Объект3_Популярность).delete()
        db.session.commit()

    return redirect(url_for('index3'))




if __name__ == '__main__':
    app.run(host="127.0.0.1", port = 6160, debug = True)
