client_id = 'c895de4e2dde4f32886ec383d6f39bd8'
redirect_uri = 'http://localhost:8642/'
config = {'client_id': client_id, 'redirect_uri': redirect_uri}
oauth_url = 'https://instagram.com/oauth/authorize/?client_id=%(client_id)s&redirect_uri=%(redirect_uri)s&response_type=token' % config
token_file = '/Users/max/.instagram_token'
port = 8642
width = 250
