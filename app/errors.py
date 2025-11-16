"""
Error handlers for the SHOP_SERV application.
"""
from flask import render_template, request, jsonify
from werkzeug.exceptions import HTTPException
from app import db

def page_not_found(error):
    """Handle 404 errors."""
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found.'
        }), 404
    return render_template('errors/404.html'), 404

def forbidden(error):
    """Handle 403 errors."""
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource.'
        }), 403
    return render_template('errors/403.html'), 403

def internal_server_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred on the server.'
        }), 500
    return render_template('errors/500.html'), 500

def bad_request(error):
    """Handle 400 errors."""
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400
    return render_template('errors/400.html', error=str(error)), 400

def handle_http_exception(error):
    """Handle all HTTP exceptions."""
    if request.path.startswith('/api/'):
        response = {
            'error': error.name,
            'message': error.description
        }
        if hasattr(error, 'code'):
            response['code'] = error.code
        return jsonify(response), error.code
    return render_template('errors/generic.html', error=error), error.code

def handle_exception(error):
    """Handle all uncaught exceptions."""
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.'
        }), 500
    return render_template('errors/500.html', error=error), 500

def init_app(app):
    """Register error handlers with the Flask application."""
    app.register_error_handler(400, bad_request)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(HTTPException, handle_http_exception)
    
    # Register a generic exception handler
    if not app.config['DEBUG']:
        app.register_error_handler(Exception, handle_exception)
