from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sslify import SSLify
from datetime import datetime

app = Flask(__name__)
sslify = SSLify(app)
app.secret_key = 'secret'
login_manager = LoginManager()
login_manager.init_app(app)


nachtisch = {'sekt': 3, 'zuckerwatte': 2, 'crepes': 2, 'erdbeereis': 5, 'erdbeerkuchen': 4}


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def is_authentificated():
        return True

    def is_active(self):
        return True

    @staticmethod
    def is_anonymus():
        return False

    def get_id(self):
        return str(self.id)


user_data = [
    {'id': 1, 'username': 'sstand', 'password': 'pass1'},
    {'id': 2, 'username': 'root', 'password': 'admin'}
]

# Erstellen von Benutzerobjekten aus den Benutzerdaten
users = [User(data['id'], data['username'], data['password']) for data in user_data]


@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None


new_number = 0
current_number = 0
digit = 0
zucker_clicks = []
crepes_clicks = []
sekt_clicks = []
eis_clicks = []
kuchen_clicks = []
buchungen = []
cz = 0
cc = 0
cs = 0
ce = 0
ck = 0
rg = 0
zwsn = 0  # zwischensumme nachtisch


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user.username == username and user.password == password:
                login_user(user)
                return redirect(url_for('manager'))
        flash('Falscher Benutzername oder Passwort!', 'error')
    return render_template('login.html')


@app.route('/manager')
@login_required
def manager():
    if current_user.username == 'sstand':
        return redirect(url_for('sstand'))
    elif current_user.username == 'root':
        return redirect(url_for('dashboard'))
    else:
        logout_user()
        return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html', selle=len(eis_clicks), sellz=len(zucker_clicks),
                           sells=len(sekt_clicks), sellc=len(crepes_clicks),
                           sellk=len(kuchen_clicks),
                           ue=len(eis_clicks) * nachtisch['erdbeereis'],
                           uz=len(zucker_clicks) * nachtisch['zuckerwatte'],
                           us=len(sekt_clicks) * nachtisch['sekt'],
                           uc=len(crepes_clicks) * nachtisch['crepes'],
                           uk=len(kuchen_clicks) * nachtisch['erdbeerkuchen'],
                           ug=(len(eis_clicks) * nachtisch['erdbeereis']) +
                           (len(zucker_clicks) * nachtisch['zuckerwatte']) +
                           (len(sekt_clicks) * nachtisch['sekt']) +
                           (len(crepes_clicks) * nachtisch['crepes']) +
                           (len(kuchen_clicks) * nachtisch['erdbeerkuchen']),
                           sella=(len(eis_clicks) + len(zucker_clicks) + len(sekt_clicks) +
                                  len(crepes_clicks) + len(kuchen_clicks)),
                           kunden=len(buchungen),
                           username=current_user.username)


# Süßigkeitenstand
@app.route('/sstand')
@login_required
def sstand():
    
    return render_template('sstand.html', rg=rg, new_number=new_number, cz=cz, cc=cc, cs=cs, ce=ce, ck=ck, zwsn=zwsn,
                           username=current_user.username)


@app.route('/sstand/add_digit', methods=['POST'])
def add_digit():
    global digit
    global rg
    global new_number
    global zwsn
    digit = request.form['digit']
    str(new_number)
    new_number = str(new_number) + str(digit)
    rg = float(new_number) - zwsn
    return render_template('sstand.html', new_number=new_number, rg=rg, cz=cz, 
                           cc=cc, cs=cs, ce=ce, ck=ck,
                           zwsn=zwsn, username=current_user.username)
    

@app.route('/sstand/zuckeras', methods=['POST'])
def zuckeras():
    global rg
    global new_number
    global zwsn
    global cz
    cz += 1
    zwsn += nachtisch['zuckerwatte']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/zucker', methods=['POST'])
def zucker():
    global rg
    global new_number
    global zwsn
    global cz
    if cz == 0:
        return redirect(url_for('sstand'))
    cz -= 1
    zwsn -= nachtisch['zuckerwatte']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/crepesteller', methods=['POST'])
def crepesteller():
    global rg
    global new_number
    global zwsn
    global cc
    cc += 1
    zwsn += nachtisch['crepes']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/crepes', methods=['POST'])
def crepes():
    global rg
    global new_number
    global zwsn
    global cc
    if cc == 0:
        return redirect(url_for('sstand'))
    cc -= 1
    zwsn -= nachtisch['crepes']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/sektglas', methods=['POST'])
def sektglas():
    global rg
    global new_number
    global zwsn
    global cs
    cs += 1
    zwsn += nachtisch['sekt']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/sekt', methods=['POST'])
def sekt():
    global rg
    global new_number
    global zwsn
    global cs
    if cs == 0:
        return redirect(url_for('sstand'))
    cs -= 1
    zwsn -= nachtisch['sekt']
    rg = float(new_number) + zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/eis', methods=['POST'])
def eis():
    global rg
    global new_number
    global zwsn
    global ce
    ce += 1
    zwsn += nachtisch['erdbeereis']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/eeis', methods=['POST'])
def eeis():
    global rg
    global new_number
    global zwsn
    global ce
    if ce == 0:
        return redirect(url_for('sstand'))
    ce -= 1
    zwsn -= nachtisch['erdbeereis']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/kuchen', methods=['POST'])
def kuchen():
    global rg
    global new_number
    global zwsn
    global ck
    ck += 1
    zwsn += nachtisch['erdbeerkuchen']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/ekuchen', methods=['POST'])
def ekuchen():
    global rg
    global new_number
    global zwsn
    global ck
    if ck == 0:
        return redirect(url_for('sstand'))
    ck -= 1
    zwsn -= nachtisch['erdbeerkuchen']
    rg = float(new_number) - zwsn
    return redirect(url_for('sstand'))


@app.route('/sstand/reset', methods=['POST'])
@login_required
def reset():
    global rg
    global digit
    global current_number
    global zwsn
    global new_number
    rg = 0
    new_number = 0
    current_number = 0
    digit = 0
    rg = float(new_number) - zwsn
    return render_template('sstand.html', new_number=new_number, rg=rg, cz=cz, cc=cc,
                           cs=cs, ce=ce,
                           ck=ck, zwsn=zwsn,
                           username=current_user.username)


@app.route('/sstand/book', methods=['POST'])
@login_required
def book():
    global zwsn
    global digit
    global current_number
    global rg
    global new_number
    global cz
    global cc
    global cs
    global ce
    global ck
    if not cz == 0:
        for count in range(cz):
            zucker_clicks.append(datetime.now().strftime('%H:%M'))

    if not cc == 0:
        for count in range(cc):
            crepes_clicks.append(datetime.now().strftime('%H:%M'))

    if not cs == 0:
        for count in range(cs):
            sekt_clicks.append(datetime.now().strftime('%H:%M'))

    if not ce == 0:
        for count in range(ce):
            eis_clicks.append(datetime.now().strftime('%H:%M'))

    if not ck == 0:
        for count in range(ck):
            kuchen_clicks.append(datetime.now().strftime('%H:%M'))

    cz = 0
    cc = 0
    cs = 0
    ce = 0
    ck = 0
    if not zwsn == 0:
        buchungen.append(datetime.now().strftime('%H:%M'))
    zwsn = 0
    new_number = 0
    rg = 0
    digit = 0
    current_number = 0
    return render_template('sstand.html', new_number=new_number, rg=rg, cz=cz, cc=cc, cs=cs, ce=ce, ck=ck, zwsn=zwsn,
                           username=current_user.username)
  

@app.route('/dashboard/logout', methods=['POST'])
def logouts():
    logout_user()
    flash('Du wurdest Abgemeldet!')
    return redirect(url_for('index'))


@app.route('/sstand/logout', methods=['POST'])
def logoutd():
    logout_user()
    flash('Du wurdest Abgemeldet!')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
