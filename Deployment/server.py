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

                    h2 {
                        font-size: 24px;
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

                    .author-container {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-top: 40px;
                    }

                    .author {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }

                    .author img {
                        width: 100px;
                        height: 100px;
                        border-radius: 50%;
                        object-fit: cover;
                    }

                    .author-name {
                        margin-top: 10px;
                        font-size: 16px;
                        color: #fff;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>CardiaScan</h1>
                    <p>Welcome to our major project</p>
                    <button onclick="runStreamlit()">Click me to run app</button>
                    <div class="author-container">
                        <div class="author">
                            <img src="https://avatars.githubusercontent.com/u/65809279?v=4" alt="Author 1">
                            <div class="author-name">Atul Dwivedi</div>
                        </div>
                        <div class="author">
                            <img src="https://media.licdn.com/dms/image/C4E03AQHXmKsDYggAyw/profile-displayphoto-shrink_400_400/0/1609768885569?e=1692835200&v=beta&t=jTpIB6AIR2ZV7Q_tTWN4sbmf1XG7ARNap-gwDcJA6LA" alt="Author 2">
                            <div class="author-name">Anuvart</div>
                        </div>
                        <div class="author">
                            <img src="https://github.com/atultechd/Arrhythmia_detection_using_ecg_image_data/blob/main/Deployment/aman.jpeg?raw=true=" alt="Author 3">
                            <div class="author-name">Aman Parihar</div>
                        </div>
                        <div class="author">
                            <img src="https://media.licdn.com/dms/image/C4E03AQHdMZXsMKgwMA/profile-displayphoto-shrink_400_400/0/1637296311214?e=1692835200&v=beta&t=RFFatqW8zlJdFVNW8UgvuT_CFJBMBIu4nK3H974VAYs" alt="Author 4">
                            <div class="author-name">Abhishek Goyal</div>
                        </div>
                    </div>
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
