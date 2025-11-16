# This file makes the routes directory a Python package
# Import all route modules here to avoid circular imports
from . import auth, customer, shop_owner, admin, main, api

# Export all blueprints for easy access
__all__ = ['auth', 'customer', 'shop_owner', 'admin', 'main', 'api']
