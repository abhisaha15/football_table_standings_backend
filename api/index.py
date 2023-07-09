from flask import Flask,jsonify
import psycopg2
import os
import json
from flask_cors import CORS, cross_origin

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

DB_PORT = "5432"


DB_URL="postgres://default:FcVuaDQ1lR2j@ep-spring-meadow-154032-pooler.ap-southeast-1.postgres.vercel-storage.com:5432/verceldb"
POSTGRES_PRISMA_URL="postgres://default:FcVuaDQ1lR2j@ep-spring-meadow-154032-pooler.ap-southeast-1.postgres.vercel-storage.com:5432/verceldb?pgbouncer=true&connect_timeout=15"
POSTGRES_URL_NON_POOLING="postgres://default:FcVuaDQ1lR2j@ep-spring-meadow-154032.ap-southeast-1.postgres.vercel-storage.com:5432/verceldb"
DB_USER="default"
DB_HOST="ep-spring-meadow-154032-pooler.ap-southeast-1.postgres.vercel-storage.com"
DB_PASS="FcVuaDQ1lR2j"
DB_NAME="verceldb"

def get_db_connection():
    connect = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    return connect

@app.route('/')
@app.route('/<string:league>')
@cross_origin()
def home(league='epl'):
    default_error_return ={'league_name':league.upper(),'data':[]}
    league_list = ['epl', 'ligue-1', 'bundesliga', 'serie-a', 'laliga']
    conn = get_db_connection()
    cur = conn.cursor()
    league_standing_list = ''

    if league.lower() not in league_list:
        return default_error_return
    else:
        league = league.lower()

    cur.execute(
        "SELECT * FROM table_standings WHERE LOWER(league_name) = '{}';".format(league)
    )
    d_a_t_a = cur.fetchall()

    cur.close()
    conn.close()
    league_standing_list = ''
    if d_a_t_a :
        for i in d_a_t_a:
            league_standing_list = json.loads(str(i[2]))
        return league_standing_list
    else:
        return default_error_return










if __name__ == "__main__":
    app.run(debug=True)
