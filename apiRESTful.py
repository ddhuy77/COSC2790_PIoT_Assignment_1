from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensehat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class SENSEHAT_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recorded_time = db.Column(db.String)
    temp = db.Column(db.String)
    humidity = db.Column(db.String)

    # def __repr__(self):
    #     return '<Post %s>' % self.title


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "recorded_time", "temp", "humidity")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class PostListResource(Resource):
    def get(self):
        posts = SENSEHAT_data.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = SENSEHAT_data(
            recorded_time=request.json['recorded_time'],
            temp=request.json['temp'],
            humidity=request.json['humidity']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)


class PostResource(Resource):
    def get(self, post_id):
        post = SENSEHAT_data.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = SENSEHAT_data.query.get_or_404(post_id)

        if 'recorded_time' in request.json:
            post.recorded_time = request.json['recorded_time']
        if 'temp' in request.json:
            post.temp = request.json['temp']
        if 'humidity' in request.json:
            post.humidity = request.json['humidity']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = SENSEHAT_data.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/posts/<int:post_id>')


if __name__ == '__main__':
    app.run(debug=True)