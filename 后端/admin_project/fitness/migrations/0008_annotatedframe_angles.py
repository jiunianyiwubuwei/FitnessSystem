# Generated migration for AnnotatedFrame.angles field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0007_annotatedvideo_annotatedframe'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedframe',
            name='angles',
            field=models.TextField(
                blank=True,
                help_text='本帧各关节角度，包含左右肘/肩/髋/膝/踢腿等10个关节的角度值',
                null=True,
                verbose_name='关节角度JSON {joint_name: angle}'
            ),
        ),
    ]
