from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Product


@receiver(post_save, sender=Product)
def notify_user_on_status_change(sender, instance, created, **kwargs):
    """
     Product holati o'zgarganda foydalanuvchiga avtomatik email yuboradi.
    """
    if created:
        # Yangi product yaratildi — hali tasdiqlanmagan
        subject = "E'lon yuborildi — tasdiqlash kutilmoqda"
        message = (
            f"Salom, {instance.user.full_name or instance.user.email}!\n\n"
            f"Sizning '{instance.title}' nomli e'loningiz yuborildi.\n"
            f"Admin tasdiqlaganidan so‘ng saytda chiqadi.\n\n"
            "Rahmat!"
        )
    else:
        # Holat o‘zgarganda
        if instance.status == "approved":
            subject = "E'lon tasdiqlandi ✅"
            message = (
                f"Tabriklaymiz!\n\n"
                f"Sizning '{instance.title}' nomli e'loningiz tasdiqlandi va endi saytda ko‘rinadi.\n\n"
                "OLX jamoasi bilan birga bo‘ling! 🚀"
            )
        elif instance.status == "rejected":
            subject = "E'lon rad etildi ❌"
            message = (
                f"Kechirasiz,\n\n"
                f"Sizning '{instance.title}' nomli e'loningiz rad etildi.\n"
                f"Iltimos, e'lon qoidalarini tekshirib qayta yuboring.\n\n"
                "OLX jamoasi"
            )
        else:
            return  # boshqa holatlar uchun email yuborilmaydi

    # Email yuborish
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [instance.user.email],
        fail_silently=True,
    )
