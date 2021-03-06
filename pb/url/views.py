# -*- coding: utf-8 -*-
"""
    url.model
    ~~~~~~~~~

    url url routes and views.

    :copyright: Copyright (C) 2014 by the respective authors; see AUTHORS.
    :license: GPLv3, see LICENSE for details.
"""

from flask import Blueprint

from pb.db import cursor
from pb.util import redirect, request_content, id_url
from pb.url import model

url = Blueprint('url', __name__)

@url.route('/<id(length=3):b66>')
@cursor
def get(b66):
    id, name = b66
    content = model.get_content(id)
    if not content:
        return 'Not found.\n', 404

    content = content.decode('utf-8')

    return redirect(content, '{}\n'.format(content))

@url.route('/u', methods=['POST'])
@cursor
def post():
    content, _ = request_content()
    if not content:
        return "Nope.\n", 400

    content = content.decode('utf-8').split('\n')[0].encode('utf-8')

    id = model.get_digest(content)
    if not id:
        id = model.insert(content)

    url = id_url(b66=id)
    return redirect(url, "{}\n".format(url), 200)
