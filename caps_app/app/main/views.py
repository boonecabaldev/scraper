from flask import render_template, session, redirect, url_for, flash, request, make_response
from datetime import datetime
import sys
from urllib.parse import urlparse

sys.path.append('/workspaces/scraper/caps_app/database')  # Add the path to the 'database' package
sys.path.append('/workspaces/scraper/caps_app')  # Add the path to the root directory

from . import main
from .. import db
from ..models import HatComponent, HatLeaf

def extract_text_id(text_id):
    parsed_url = urlparse(text_id)
    path_parts = parsed_url.path.split('/')
    new_text_id = path_parts[-2]  # text_id is the second last part of the path
    return new_text_id

@main.route('/')
def index():
   hat_components = HatComponent.query.all()

   response = make_response(render_template('hatcomponents.html', hat_components=hat_components))
   response.set_etag('some_etag')
   response.headers['Last-Modified'] = datetime.now()


   return response

@main.route('/hat_component/<int:id>')
def hat_component(id):
   hat_component = HatComponent.query.get_or_404(id)
   hat_leaves = HatLeaf.query.filter_by(node_id=id).all()

   response = make_response(render_template('hatleaves.html', hat_component=hat_component, hat_leaves=hat_leaves))
   response.set_etag('some_etag')
   response.headers['Last-Modified'] = datetime.now()

   return response