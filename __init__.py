import os
from datetime import datetime
from peewee import DoesNotExist
from flask import Flask, request, redirect, url_for, abort
from inf5190.models import init_app, Product, Choice
from inf5190.services import PollServices
from inf5190 import views


def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)

    @app.route('/')
    def index():
        products = Product.select()
        if products:
            return views.index(products)
        else:
            return views.index_empty()

    @app.route('/polls/new', methods=['GET'])
    def polls_new():
        poll = Poll(None, '', None)
        return views.new_poll(poll)

    @app.route('/polls/new', methods=['POST'])
    def polls_create():
        poll = PollServices.create_new_poll_from_post_data(request.form, datetime.now())

        return redirect(url_for('inf5190', poll_id=poll.id))

    @app.route('/polls/<int:poll_id>', methods=['GET'])
    def poll(poll_id):
        poll = Poll.get_or_none(Poll.id == poll_id)
        if not poll:
            return abort(404)

        return views.view_poll(poll)

    @app.route('/polls/<int:poll_id>/choices/new', methods=['POST'])
    def choice_create(poll_id):
        poll = Poll.get_or_none(Poll.id == poll_id)
        if not poll:
            return abort(404)

        choice = PollServices.create_new_choice_for_poll_from_post_data(poll, request.form)
        return redirect(url_for('inf5190', poll_id=poll.id))

    @app.route('/polls/<int:poll_id>/vote', methods=['POST'])
    def poll_vote(poll_id):
        try:
            vote = PollServices.cast_vote_from_post_data(poll_id, request.form)
        except DoesNotExist:
            return abort(404)

        return redirect(url_for('inf5190', poll_id=vote.poll.id))

    return app
