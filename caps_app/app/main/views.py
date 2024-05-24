from flask import make_response, render_template
from datetime import datetime
import sys
sys.path.append('/workspaces/scraper/caps_app/database')  # Add the path to the 'database' package
sys.path.append('/workspaces/scraper/caps_app')  # Add the path to the root directory

from . import main
from ..models import HatComponent, HatLeaf

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
   hat_leaves = HatLeaf.query.filter_by(hat_component_id=id).all()

   response = make_response(render_template('hat_component.html', hat_component=hat_component, hat_leaves=hat_leaves))
   response.set_etag('some_etag')
   response.headers['Last-Modified'] = datetime.now()

   return response