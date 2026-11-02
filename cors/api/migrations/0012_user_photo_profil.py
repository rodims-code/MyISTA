from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_document_categorie_document_deadline_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="photo_profil",
            field=models.ImageField(blank=True, null=True, upload_to="profiles/"),
        ),
    ]
