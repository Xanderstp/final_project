from flask import Flask, request, render_template, make_response, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect
import flask

import datetime
from data import db_session
from data.users import User
from data.login_form import LoginForm
from data.register import RegisterForm

baykal_url = 'https://ru.wikipedia.org/wiki/%D0%91%D0%B0%D0%B9%D0%BA%D0%B0%D0%BB'
baykal_info = "Байка́л (бур. Байгал далай) — озеро тектонического происхождения в южной части Восточной Сибири, самое глубокое озеро на планете, крупнейший природный резервуар пресной воды и самое большое по площади пресноводное озеро на континенте. Озеро и прибрежные территории отличаются уникальным разнообразием флоры и фауны, бо́льшая часть видов животных эндемична."
baykal_photos = ['main/baykal-1.jpg', 'main/baykal-2.jpg', 'main/baykal-3.jpg', 'main/baykal-4.jpg', 'main/baykal-5.jpg']


titikaka_url = 'https://ru.wikipedia.org/wiki/%D0%A2%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%D0%BA%D0%B0'
titikaka_info = "Титика́ка (исп. Titicaca, кечуа и айм. Titiqaqa) — озеро в Южной Америке, самое большое по запасам пресной воды озеро Южной Америки и второе по площади поверхности (после озера Маракайбо, которое к тому же иногда считают морским заливом). Часто называют высочайшим в мире судоходным озером. Находится в Андах на плоскогорье Альтиплано, на границе Перу и Боливии. Крупнейший город — Пуно на западном берегу; в 19 км расположен город Тиуанако. Вокруг озера и на островах находится множество поселений народов аймара и кечуа. Часть населения живёт на плавучих тростниковых островах Урос (Uros)."
titikaka_photos = ['titikaka/0.jpg', 'titikaka/1.jpg', 'titikaka/2.jpg', 'titikaka/3.jpg', 'titikaka/4.jpg']

seliger_url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%B5%D0%BB%D0%B8%D0%B3%D0%B5%D1%80'
seliger_info = "Селиге́р — система озёр ледникового происхождения в Тверской и Новгородской областях России. Другое название — Осташковское, по названию стоящего на озёрном берегу города Осташкова. Селигер принимает 110 притоков, а из него вытекает лишь одна река Селижаровка. Озеро лежит на высоте 205 метров над уровнем моря и имеет ледниковое происхождение. Этим объясняется его своеобразная форма — это не озеро в привычном понятии, а скорее цепочка озёр, протянувшихся с севера на юг на 100 км и связанных между собой короткими узкими протоками. Береговая линия протяжённостью более 500 км отличается изрезанностью — поросшие лесом мысы, глубокие вдавшиеся в сушу живописные заливы, разнообразные по форме острова."
seliger_photos = ['seliger/0.jpg', 'seliger/1.jpg', 'seliger/2.jpg', 'seliger/3.jpg', 'seliger/4.jpg']

loh_url = 'https://ru.wikipedia.org/wiki/%D0%9B%D0%BE%D1%85-%D0%9D%D0%B5%D1%81%D1%81'
loh_info = "Лох-Не́сс (англ. Loch Ness, гэльск. Loch Nis) — большое глубокое пресноводное озеро в Шотландии, растянувшееся на 36 км к юго-западу от Инвернесса.Озеро широко известно в мире благодаря легенде о Лох-Несском чудовище. Существуют многочисленные коммерческие маршруты по озеру для туристов, желающих насладиться живописной природой и, возможно, увидеть мифического монстра.Лох-Несс — это самый большой водоём на протяжении геологического разлома Грейт-Глен, проходящего с севера на юг от Инвернесса до Форт-Уильяма. Озеро является частью Каледонского канала, соединяющего западное и восточное морские побережья Шотландии."
loh_photos = ['loh_nes/0.jpg', 'loh_nes/1.jpg', 'loh_nes/2.jpg', 'loh_nes/3.jpg', 'loh_nes/4.jpg']

kaspey_url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%81%D0%BF%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B5_%D0%BC%D0%BE%D1%80%D0%B5'
kaspey_info = "Каспи́йское мо́ре (Ка́спий, от лат. Caspium mare или др.-греч. Κασπία θάλασσα, Kaspía thálassa) — крупнейший на Земле замкнутый водоём, который может классифицироваться как самое большое бессточное озеро либо как море — из-за своих размеров, а также из-за того, что его ложе образовано земной корой океанического типа.Расположено на стыке Европы и Азии. Вода в Каспии солоноватая, — от 0,05 ‰ близ устья Волги до 11—13 ‰ на юго-востоке. Уровень воды подвержен колебаниям, согласно данным 2009 года составлял 27,16 м ниже уровня Мирового океана.Площадь Каспийского моря в настоящее время — примерно 390 000 км², максимальная глубина — 1025 м."
kaspey_photos = ['kaspie/0.jpg', 'kaspie/1.jpg', 'kaspie/2.jpg', 'kaspie/3.jpg', 'kaspie/4.jpg']

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def main():
    global photos
    return render_template('main.html', photos=baykal_photos, title="Geagraphy", text=baykal_info, url=baykal_url)


def name(session, idd):
    for i in session.query(User).filter(User.id == idd):
        return i.name


def surname(session, idd):
    for i in session.query(User).filter(User.id == idd):
        return i.surname


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if request.method == "POST":
        print('post')
        if form.password.data != form.password_again.data:
            return render_template('reg.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('reg.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('reg.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def lin():
    form = LoginForm()
    if request.method == "POST":  # form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/states', methods=['GET', 'POST'])
def albums():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    global photos
    return render_template('albums_list.html', title="STATE")


@app.route('/titikaka', methods=['GET', 'POST'])
def z3():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=titikaka_photos, title="TITIKAKA", text=titikaka_info, url=titikaka_url)


@app.route('/seliger', methods=['GET', 'POST'])
def z4():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=seliger_photos, title="SELIGER", text=seliger_info, url=seliger_url)


@app.route('/loh_nes', methods=['GET', 'POST'])
def z5():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=loh_photos, title="LOH_NES", text=loh_info, url=loh_url)


@app.route('/kaspey', methods=['GET', 'POST'])
def z6():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=kaspey_photos, title="KASPEY", text=kaspey_info, url=kaspey_url)


@app.route('/need_login', methods=['GET', 'POST'])
def need_log():
    return render_template('need_login.html', title='Авторизуйтесь')


def main():
    db_session.global_init("db/blogs.db")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()


if __name__ == '__main__':
    main()
