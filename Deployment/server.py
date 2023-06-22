from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <html>
            <head>
                <title>CardiaScan Landing Page</title>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        font-family: sans-serif;
                        background: linear-gradient(to bottom, #d97b93 0%,#6e529d 100%);
                    }

                    .container {
                        width: 100%;
                        max-width: 600px;
                        margin: 0 auto;
                        text-align: center;
                        padding-top: 100px;
                    }

                    h1 {
                        font-size: 36px;
                        margin-bottom: 20px;
                    }

                    button {
                        padding: 12px 24px;
                        font-size: 18px;
                        font-weight: bold;
                        color: #fff;
                        background-color: #008CBA;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        transition: background-color 0.3s;
                    }

                    button:hover {
                        background-color: #005D6E;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>CardiaScan</h1>
                    <p> Welcome to our major project </p>
                    <button onclick="runStreamlit()">Click me to run app</button>
                </div>

                <script>
                    function runStreamlit() {
                        var xhr = new XMLHttpRequest();
                        xhr.open('GET', '/run_streamlit', true);
                        xhr.send();
                    }
                </script>
            </body>
        </html>
    '''

@app.route('/run_streamlit')
def run_streamlit():
    os.system('streamlit run final_app.py')
    return 'Streamlit app has been started'

if __name__ == '__main__':
    app.run(port=5000)


# export FLASK_APP=server.py
# flask run --port=5001

# ......For OS Error................................
# echo 524288 | sudo tee /proc/sys/fs/inotify/max_user_watches
# sudo sysctl -p
