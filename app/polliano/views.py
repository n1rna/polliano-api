from . import polliano_blueprint

from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify
from app.models import User
from app.polliano.models import Poll, Vote
from datetime import datetime

class PollView(MethodView):
    """This class-based view registers a new user."""

    def post(self):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # user authed
                poll_id = int(request.data.get('poll_id', 0))
                date_modified = datetime.utcnow()
                question = str(request.data.get('question', ''))
                poll_image = str(request.data.get('image', ''))
                options = str(request.data.get('options', ''))
                features = str(request.data.get('features', ''))
                stats = str(request.data.get('stats', ''))
                created_by = user_id
                date_created = datetime.utcnow()

                if poll_id:
                    poll = Poll.query.get(poll_id)
                    poll.date_modified = date_modified
                    poll.question = question
                    poll.poll_image = poll_image
                    poll.options = options
                    poll.features = features
                    poll.save()

                    response = jsonify({
                        'message': "poll already existed and updated",
                    })

                    return make_response(response), 201

                else:
                    poll = Poll(question=question, options=options, created_by=user_id)
                    poll.date_modified = date_modified
                    poll.date_created = date_created
                    poll.poll_image = poll_image
                    poll.features = features
                    poll.save()

                    response = jsonify({
                        'message': "poll created successssfully"
                    })

                    return make_response(response), 201

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


    def get(self, poll_id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                #user authed
                poll = Poll.query.get(poll_id)
                if poll:

                    response = jsonify({
                        'id': poll.id,
                        'question': poll.question,
                        'date_created': poll.date_created,
                        'date_modified': poll.date_modified,
                        'created_by': poll.created_by
                    })

                    return make_response(response), 200

                else:

                    response = jsonify({
                        'message': "no poll existed with the requested id",
                        'requested_id': poll_id
                    })

                    return make_response(response), 401

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


def polls_list():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]

    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            #user authed
            polls = Poll.query

            if polls.count() > 0:

                res_obj = {
                    'num' : polls.count()
                }

                for p in polls:
                    res_obj[str(p.id)]={
                        'question' : p.question,
                        'poll_image' : p.poll_image,
                        'options' : p.options,
                        'features' : p.features,
                        'date_modified' : p.date_modified,
                    }

                return make_response(jsonify(res_obj)), 200

            else:

                response = jsonify({
                    'message': "no polls exist YET!",
                    'requester_user_id': user_id
                })

                return make_response(response), 401

        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

# Define the API resource
polls_view = PollView.as_view('polls_view')

polliano_blueprint.add_url_rule(
    '/polliano/poll',
    view_func=polls_view,
    methods=['POST'])

polliano_blueprint.add_url_rule(
    '/polliano/poll/<int:poll_id>',
    view_func=polls_view,
    methods=['GET'])

polliano_blueprint.add_url_rule(
    '/polliano/poll/all',
    view_func=polls_list,
    methods=['GET'])
