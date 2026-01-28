from django.conf import settings
from twilio.rest import Client
from .models import Notification

class TwilioService:
    """Service for sending notifications via Twilio"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        self.client = None
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
    
    def send_sms(self, to_number, message, user, notification_type):
        """Send SMS notification"""
        if not self.client:
            # Log notification without sending (for demo without Twilio credentials)
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                message=message,
                phone_number=to_number,
                sent_successfully=False,
                error_message="Twilio credentials not configured"
            )
            return notification
        
        try:
            twilio_message = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                message=message,
                phone_number=to_number,
                sent_successfully=True
            )
            return notification
            
        except Exception as e:
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                message=message,
                phone_number=to_number,
                sent_successfully=False,
                error_message=str(e)
            )
            return notification
    
    def send_claim_notification(self, claim):
        """Send notification when food is claimed"""
        message = f"ShareBite: Your listing '{claim.listing.title}' has been claimed by {claim.receiver.username}. Pickup location: {claim.listing.pickup_location}"
        return self.send_sms(
            claim.listing.provider.phone_number,
            message,
            claim.listing.provider,
            'claim_created'
        )
    
    def send_confirmation_notification(self, claim):
        """Send notification when claim is confirmed"""
        message = f"ShareBite: Your claim for '{claim.listing.title}' has been confirmed! Pickup at: {claim.listing.pickup_location}"
        return self.send_sms(
            claim.receiver.phone_number,
            message,
            claim.receiver,
            'claim_confirmed'
        )
    
    def send_expiry_alert(self, listing):
        """Send expiry alert for food listing"""
        message = f"ShareBite: Your listing '{listing.title}' is expiring soon! Expiry: {listing.expiry_date.strftime('%Y-%m-%d %H:%M')}"
        return self.send_sms(
            listing.provider.phone_number,
            message,
            listing.provider,
            'expiry_alert'
        )
