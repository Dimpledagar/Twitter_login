from database import CursorFromConnectionFromPool  # connect
import oauth2
from twitter_utils import consumer


class User:
    def __init__(self, id, screen_name, oauth_token, oauth_token_secret):
        self.id = id
        self.screen_name = screen_name
        self.oauth_token = oauth_token  # oauth_token
        self.oauth_token_secret = oauth_token_secret  # oauth_token_secret

    def save_to_db(self):
        # connection = psycopg2.connect(database="test", user="postgres", password="password", host="localhost")
        with CursorFromConnectionFromPool() as cursor:
            # with connection.cursor() as cursor:
            cursor.execute(
                'insert into users(screen_name,oauth_token,oauth_token_secret) values(%s,%s,%s)',
                (self.screen_name, self.oauth_token, self.oauth_token_secret))
        # connection.commit()
        # connection.close()

    @classmethod
    def load_from_db_by_email(cls, screen_name):  # default return is None in python
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('Select * from users where screen_name= %s', (screen_name,))
            user_data = cursor.fetchone()
            print(user_data)
            if user_data:  # None object is equal to False in boolean comparison
                return cls(user_data[0], user_data[1], user_data[2], user_data[3])

    def twitter_request(self, url, verb='GET'):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # make twitter API call
        response, content = authorized_client.request(url, verb)
        print(response.status)
        if response.status != 200:
            print('An error occurred getting the authorized token from twitter!')
        return content.encode('UTF-8')
