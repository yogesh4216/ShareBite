from django.db.models.signals import post_save
from django.dispatch import receiver
from claims.models import Claim
from .services import TwilioService

@receiver(post_save, sender=Claim)
def send_claim_notifications(sender, instance, created, **kwargs):
    """Send notifications when claim is created or updated"""
    twilio_service = TwilioService()
    
    if created:
        # Send notification to provider when claim is created
        if instance.listing.provider.phone_number:
            twilio_service.send_claim_notification(instance)
    
    elif instance.status == 'confirmed':
        # Send notification to receiver when claim is confirmed
        if instance.receiver.phone_number:
            twilio_service.send_confirmation_notification(instance)
