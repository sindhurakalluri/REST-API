from flask import (Flask, request)
from flask_restful import (Resource, Api)
import bit, git

app = Flask(__name__)
api = Api(app)

class GitBit(Resource):
    def get(self, **kwargs):
        gituser = request.args['git']
        bituser = request.args['bit']
        data_git = git.GitHubAPI(gituser).get_data()
        data_bit = bit.BitbucketAPI(bituser).get_data()

        for (k,v) in data_bit.items():
            data_git[k] = data_git[k] + data_bit[k]

        return data_git

api.add_resource(GitBit, '/username')

if __name__=='__main__':
    app.run()