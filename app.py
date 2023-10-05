from flask import Flask, render_template, request, session, abort, redirect, url_for,jsonify, make_response
from LLMresponse import process_llm_response, modelF
from Text2Voice import intro_voice, predicted_voice
from time import sleep
from threading import Thread
from google.oauth2 import credentials
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests



app = Flask(__name__)



#-----------------------------google function--------------------------------#

app.secret_key = "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" # make sure this matches with that's in client_secret.json

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = "249932032588-17sb0t4cjvsu2gh3d2e24fphrecbhe1h.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)




def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper
#-----------------------------log in --------------------------------------#

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


#----------------------------call back----------------------------#

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/assistview")


#-------------------------logout-----------------------------------#
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#----------------------Flask App----------------------------------#
@app.route('/')
def HomeView():
    return render_template('index.html')


@app.route('/assistview',methods=["POST", "GET"])
@login_is_required
def VirualAssistView():
    if request.method == "POST":
        print('step1')
        qestion = request.form['prompt']
        llm_response = modelF(qestion)
        outAns = process_llm_response(llm_response)
        print('ans', outAns)
        
        text1 = outAns
        thr = Thread(target=predicted_voice, args=[text1])
        thr.start()
        return jsonify({'response': outAns})
    
    thr = Thread(target=intro_voice)
    thr.start()
    return render_template('assist.html')




if __name__ == "__main__":
    app.run(debug=True)