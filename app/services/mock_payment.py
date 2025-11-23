from datetime import datetime
import uuid
from flask import current_app

class MockPaymentService:
    def __init__(self):
        self.transactions = {}
        
    def create_order(self, amount, currency='INR', receipt=None, notes=None):
        """Create a mock payment order"""
        order_id = f"mock_order_{uuid.uuid4().hex[:8]}"
        
        order_data = {
            'id': order_id,
            'amount': int(amount * 100),  # Keep same format as real payment gateways
            'currency': currency,
            'receipt': receipt or f"order_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'status': 'created',
            'created_at': datetime.utcnow().isoformat(),
            'notes': notes or {}
        }
        
        # Store the order for verification
        self.transactions[order_id] = {
            'order': order_data,
            'status': 'created',
            'amount': amount,
            'verified': False
        }
        
        return order_data

    def verify_payment(self, order_id):
        """Simulate payment verification"""
        if order_id in self.transactions:
            self.transactions[order_id].update({
                'status': 'verified',
                'verified': True,
                'verified_at': datetime.utcnow().isoformat()
            })
            return True
        return False

# Create a singleton instance
mock_payment_service = MockPaymentService()
