"""
Payment system with Stripe integration for AI Assistant subscriptions.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import stripe
from datetime import datetime, timedelta

from .database import get_db
from .models import User, PaymentTransaction, SubscriptionStatus
from .auth import get_current_user
from .config import settings

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter()


class CreatePaymentIntentRequest(BaseModel):
    """Request to create payment intent."""
    product_type: str  # "monthly", "yearly", "per_application"
    currency: str = "eur"


class PaymentIntentResponse(BaseModel):
    """Payment intent response."""
    client_secret: str
    amount: int
    currency: str
    product_type: str


class SubscriptionResponse(BaseModel):
    """Subscription information response."""
    status: SubscriptionStatus
    expires_at: Optional[datetime]
    credits: int
    usage_count: int


@router.get("/pricing")
async def get_pricing():
    """Get pricing information for AI Assistant."""
    return {
        "monthly": {
            "price": settings.AI_ASSISTANT_PRICE_MONTHLY,
            "currency": "eur",
            "description": "Monthly AI Assistant subscription",
            "features": [
                "Unlimited grant analysis",
                "AI-powered form pre-filling",
                "Application guidance and tips",
                "Priority support"
            ]
        },
        "yearly": {
            "price": settings.AI_ASSISTANT_PRICE_YEARLY,
            "currency": "eur", 
            "description": "Yearly AI Assistant subscription (2 months free)",
            "features": [
                "Unlimited grant analysis",
                "AI-powered form pre-filling", 
                "Application guidance and tips",
                "Priority support",
                "2 months free (€98 value)"
            ]
        },
        "per_application": {
            "price": settings.AI_ASSISTANT_PRICE_PER_APPLICATION,
            "currency": "eur",
            "description": "Pay per grant application",
            "features": [
                "Complete AI assistance for one application",
                "Form pre-filling and guidance",
                "Document generation",
                "Application review"
            ]
        }
    }


@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(
    request: CreatePaymentIntentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe payment intent for AI Assistant subscription."""
    
    # Determine amount based on product type
    if request.product_type == "monthly":
        amount = settings.AI_ASSISTANT_PRICE_MONTHLY
        description = "AI Assistant Monthly Subscription"
    elif request.product_type == "yearly":
        amount = settings.AI_ASSISTANT_PRICE_YEARLY
        description = "AI Assistant Yearly Subscription"
    elif request.product_type == "per_application":
        amount = settings.AI_ASSISTANT_PRICE_PER_APPLICATION
        description = "AI Assistant Per Application"
    else:
        raise HTTPException(status_code=400, detail="Invalid product type")
    
    try:
        # Create or get Stripe customer
        if not current_user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=current_user.email,
                name=current_user.full_name,
                metadata={"user_id": current_user.id}
            )
            current_user.stripe_customer_id = customer.id
            db.commit()
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=request.currency,
            customer=current_user.stripe_customer_id,
            description=description,
            metadata={
                "user_id": current_user.id,
                "product_type": request.product_type
            }
        )
        
        # Store payment transaction
        transaction = PaymentTransaction(
            user_id=current_user.id,
            stripe_payment_intent_id=intent.id,
            amount=amount,
            currency=request.currency.upper(),
            description=description,
            product_type=request.product_type,
            status="pending"
        )
        db.add(transaction)
        db.commit()
        
        return PaymentIntentResponse(
            client_secret=intent.client_secret,
            amount=amount,
            currency=request.currency,
            product_type=request.product_type
        )
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Payment error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhooks."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle payment intent succeeded
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        await handle_payment_success(payment_intent, db)
    
    # Handle payment intent failed
    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        await handle_payment_failure(payment_intent, db)
    
    return {"status": "success"}


async def handle_payment_success(payment_intent: Dict[str, Any], db: Session):
    """Handle successful payment."""
    user_id = int(payment_intent["metadata"]["user_id"])
    product_type = payment_intent["metadata"]["product_type"]
    
    # Update payment transaction
    transaction = db.query(PaymentTransaction).filter(
        PaymentTransaction.stripe_payment_intent_id == payment_intent["id"]
    ).first()
    
    if transaction:
        transaction.status = "succeeded"
        
        # Update user subscription
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            now = datetime.utcnow()
            
            if product_type == "monthly":
                user.subscription_status = SubscriptionStatus.MONTHLY
                user.subscription_start_date = now
                user.subscription_end_date = now + timedelta(days=30)
                
            elif product_type == "yearly":
                user.subscription_status = SubscriptionStatus.YEARLY
                user.subscription_start_date = now
                user.subscription_end_date = now + timedelta(days=365)
                
            elif product_type == "per_application":
                user.subscription_status = SubscriptionStatus.PAY_PER_USE
                user.ai_assistant_credits += 1
                transaction.credits_added = 1
        
        db.commit()


async def handle_payment_failure(payment_intent: Dict[str, Any], db: Session):
    """Handle failed payment."""
    transaction = db.query(PaymentTransaction).filter(
        PaymentTransaction.stripe_payment_intent_id == payment_intent["id"]
    ).first()
    
    if transaction:
        transaction.status = "failed"
        db.commit()


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user: User = Depends(get_current_user)
):
    """Get current user's subscription status."""
    expires_at = None
    if current_user.subscription_end_date:
        expires_at = current_user.subscription_end_date
        
        # Check if subscription has expired
        if expires_at < datetime.utcnow() and current_user.subscription_status != SubscriptionStatus.FREE:
            # Update subscription status
            from .database import SessionLocal
            db = SessionLocal()
            user = db.query(User).filter(User.id == current_user.id).first()
            user.subscription_status = SubscriptionStatus.FREE
            db.commit()
            db.close()
            current_user.subscription_status = SubscriptionStatus.FREE
    
    return SubscriptionResponse(
        status=current_user.subscription_status,
        expires_at=expires_at,
        credits=current_user.ai_assistant_credits,
        usage_count=current_user.ai_assistant_usage_count
    )


@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel current subscription."""
    if current_user.subscription_status in [SubscriptionStatus.MONTHLY, SubscriptionStatus.YEARLY]:
        current_user.subscription_status = SubscriptionStatus.CANCELLED
        db.commit()
        
        return {"message": "Subscription cancelled successfully"}
    else:
        raise HTTPException(status_code=400, detail="No active subscription to cancel")
