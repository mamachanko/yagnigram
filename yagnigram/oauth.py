import multiprocessing
import os
import time
import webbrowser

from wsgiref.simple_server import make_server
import falcon


CLIENT_ID = 'c895de4e2dde4f32886ec383d6f39bd8' 
PORT = 8642
REDIRECT_URI = 'http://localhost:%s/' % PORT
OAUTH_URL = 'https://instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=token' % (CLIENT_ID, REDIRECT_URI)


def handle_oauth(output_file):
    app = build_oauth_app(output_file)
    with Server(app, PORT):
        browse_url(OAUTH_URL)
        wait_for_file(output_file)
        time.sleep(1)


def build_oauth_app(output_file):
    app = falcon.API()
    app.add_route('/', OauthResource())
    app.add_route('/{token}/', TokenResource(output_file))
    return app


def browse_url(url):
    browser = webbrowser.get()
    browser.open_new_tab(url)


def wait_for_file(filename):
    while True:
        if os.path.exists(filename):
            break


class Server:

    def __init__(self, app, port=8000):
        server = make_server('', port, app)
        self.server_process = multiprocessing.Process(
            target=server.serve_forever
        )

    def __enter__(self):
        self.server_process.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server_process.terminate()


class OauthResource:

    def on_get(self, req, resp):
        resp.body = """
            <script type="text/javascript">
                var token = window.location.href.split("access_token=")[1];
                window.location = "/" + token + "/";
            </script>
        """
        resp.content_type = 'text/html'


class TokenResource:

    def __init__(self, output_file):
        self.output_file = output_file

    def on_get(self, req, resp, token):
        if token == 'favicon.ico':
            return
        with open(self.output_file, 'w') as f:
            f.write(token)
        resp.body = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>yagnigram</title>
                </head>
                <body>
                    <h3>yagnigram</h3>
                    <p>Your Instagram access token has been written to %s.</p>
                    <p>You may return to the shell.</p>
                    <p></p>
                    <p><em>Thank you.</em></p>
                </body>
            </html>
        """ % os.path.abspath(self.output_file)
        resp.content_type = 'text/html'
