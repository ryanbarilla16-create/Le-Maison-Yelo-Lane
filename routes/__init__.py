from flask import Blueprint

# Initialize the Blueprint exactly once here, so it can be shared across all route modules
main_bp = Blueprint('main', __name__)

# Import the routes from the decoupled files to register them with the blueprint
# These must be imported AFTER main_bp is instantiated to avoid circular imports.
from . import views, auth, reservations, orders
