from flask import Flask, render_template
from spotify_for_flask_app import createSpotify
from SMS_setup_alert import simp_setupCompleteSMS
#from get_user_mood_from_top import getUserMood

app = Flask(__name__)
# geo = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)



# Start here
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Home page links to this about page, where the spotify Auth is triggered

@app.route('/about')
def about():
    return render_template('about.html')

# Immediately redirects to spotify permissions form/sign in
@app.route('/auth')
def auth():
    print("Hello World!")
    createSpotify()
    return render_template('auth.html')

# Once the permissions have been granted, the user will be redirected to this page
# At this point the user clicks on the button to analyse their music tastes
@app.route('/authorised')
def authorised():
    #This is where the user is redirected to after authorising spotify access
    return render_template('authorised.html')

# This page displays a summary of the user's music (mean_valence as a percentage)
# click through to add mobile numbers
@app.route('/summary')
def summary():
    return render_template('summary.html')

# Page to add both mobile numbers
# Click through leads to finish page and starts the background script
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Set up is finished at this point and script is running inthe background
@app.route('/finish')
def finish():
    to = '+447952165272'
    to2 = '+447758637203'
    simp_setupCompleteSMS(to, to2)
    return render_template('finish.html')




# Spare Template
@app.route('/button')
def button():
    return render_template('button.html')

'''
@app.route("/forward", methods=["GET", "POST"])
def move_forward():
    ah = weather()
    prediction = predictPlay(ah)
    print(type(prediction))
    cloud = ah[0]
    wind = ah[1]
    temp = round((ah[2]-32)*5/9)
    humidity = ah[3]
    sum = ah[4]
    return render_template('index.html', cloud=cloud, wind=wind, temp=temp, humidity=humidity, sum=sum ,  prediction=prediction)

@app.route("/test/", methods = ["POST"])
def get_javascript_data():
    ah = weather()
    cloud = ah[0]
    wind = ah[1]
    temp = round((ah[2]-32)*5/9)
    humidity = ah[3]
    sum = ah[4]
    return render_template('index.html', cloud=cloud, wind=wind, temp=temp, humidity=humidity, sum=sum )

if __name__ == "__main__":
    app.run()
'''
