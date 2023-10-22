# Generated by Django 4.2.1 on 2023-10-20 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "backend",
            "0005_alter_absence_description_alter_absence_is_accepted_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PatentGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("patent_number", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PatentStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=150, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Patent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField()),
                ("active", models.BooleanField(default=True)),
                ("remark", models.TextField(null=True)),
                ("abstract", models.TextField(null=True)),
                ("priority_date", models.DateTimeField(null=True)),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="backend.user",
                    ),
                ),
                ("drawing", models.ManyToManyField(blank=True, to="backend.filegroup")),
                (
                    "inventor",
                    models.ManyToManyField(
                        blank=True, related_name="inventor", to="backend.user"
                    ),
                ),
                (
                    "part_group",
                    models.ManyToManyField(blank=True, to="backend.partgroup"),
                ),
                (
                    "patent_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="backend.patentgroup",
                    ),
                ),
                (
                    "patent_tag",
                    models.ManyToManyField(blank=True, to="backend.patenttag"),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="backend.patentstatus",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PatentClaim",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("claim_number", models.IntegerField()),
                (
                    "patent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="backend.patent",
                    ),
                ),
            ],
            options={
                "unique_together": {("patent", "claim_number")},
            },
        ),
    ]
