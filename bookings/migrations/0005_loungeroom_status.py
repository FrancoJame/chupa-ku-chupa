from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_alter_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='loungeroom',
            name='status',
            field=models.CharField(
                choices=[
                    ('AVAILABLE', 'Available'),
                    ('BUSY', 'Busy'),
                    ('FREE_SOON', 'Free soon'),
                    ('UNAVAILABLE', 'Not available'),
                    ('MAINTENANCE', 'Under maintenance'),
                ],
                default='AVAILABLE',
                max_length=20,
            ),
        ),
    ]
