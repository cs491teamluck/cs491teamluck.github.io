from flask import Flask , render_template , url_for , request , flash , redirect , send_from_directory
from masterController import controller

app = Flask(__name__ , static_folder='static')
app.config['SECRET_KEY'] = 'secretkey'

@app.route('/')
def home():
    if controller.getCurrentUserID() == -1:
        return redirect(url_for('userpage'))
    return render_template('home.html')

@app.route('/usermanual')
def usermanual():
    if controller.getCurrentUserID() != -1:
        return render_template('nonusermanual.html')
    else:
        return render_template('usermanual.html')

@app.route('/userpage/download/<path:filename>')
def downloadFile(filename):
    downloadPath = str(app.static_folder) + '/usersongs'
    return send_from_directory(downloadPath , filename)

@app.route('/userpage' , methods=['GET' , 'POST'])
def userpage():
    if controller.getCurrentUserID() == -1:
        return redirect(url_for('login'))
    
    userSongs = controller.getUserSongs(controller.getCurrentUserID())
    
    if userSongs:
        chosenSong = userSongs[0]
    else:
        chosenSong = None

    if request.method == 'POST':
        chosenSong = request.form.get('usersong')
        if request.form['action'] == 'Download':
            return downloadFile(chosenSong)

    return render_template('userpage.html' , userSongs=userSongs , chosenSong=chosenSong)

@app.route('/createsong' , methods=['GET' , 'POST'])
def createsong():
    if controller.getCurrentUserID() == -1:
        return redirect(url_for('login'))
    
    creationSongs = controller.getCreationSongs()

    if request.method == 'POST':
        chosenSong = request.form.get('creationsong')
        songLength = int(request.form.get('generateLength'))
        generateSongName = request.form.get('generateSongName')
        if ('/' or '\\') not in generateSongName:
            controller.createSong(chosenSong , songLength , generateSongName , controller.getCurrentUserID())
            return redirect(url_for('userpage')) 

    return render_template('createsong.html' , creationSongs=creationSongs)

@app.route('/listensample' , methods=['GET' , 'POST'])
def listensample():
    if controller.getCurrentUserID() == -1:
        return redirect(url_for('login'))
    
    sampleSongs = controller.getCreationSongs()

    if sampleSongs:
        chosenSong = sampleSongs[0]
    else:
        chosenSong = None

    if request.method == 'POST':
        chosenSong = request.form.get('samplesong')

    return render_template('listensample.html' , sampleSongs=sampleSongs , chosenSong=chosenSong)

@app.route('/logout')
def logout():
    controller.setCurrentUserID(-1)
    return redirect(url_for('home'))

@app.route('/login' , methods=['GET' , 'POST'])
def login():
    if controller.getCurrentUserID() != -1:
        return redirect(url_for('userpage'))
    
    isAlert = False

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        isSuccessful = controller.login(email , password)

        if controller.getCurrentUserID() != -1 and isSuccessful:
            return redirect(url_for('userpage'))

    return render_template('login.html' , isAlert=isAlert)

@app.route('/signup' , methods=['GET' , 'POST'])
def signup():
    if controller.getCurrentUserID() != -1:
        return redirect(url_for('userpage'))

    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        isSuccessful = controller.signup(email , password1 , password2)

        if isSuccessful:
            return redirect(url_for('login'))
        
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)