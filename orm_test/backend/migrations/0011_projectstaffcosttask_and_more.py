# Generated by Django 4.2.1 on 2023-05-08 13:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_customer_customerplant_derivativegrouplmc_derivativevolumegrouplmc_derivativevolumelmc_lmcderivative'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStaffCostTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='LMCDerivative',
            new_name='DerivativeLMC',
        ),
        migrations.RenameModel(
            old_name='DerivativeVolumeGroupLMC',
            new_name='DerivativeVolumeLMCGroup',
        ),
        migrations.RenameField(
            model_name='derivativelmc',
            old_name='derivative_group_lmc',
            new_name='derivative_lmc_group',
        ),
        migrations.RenameField(
            model_name='derivativevolumelmc',
            old_name='volume_group',
            new_name='derivative_lmc_volume_group',
        ),
        migrations.RenameField(
            model_name='derivativevolumelmc',
            old_name='lmc_revision',
            new_name='revision_lmc',
        ),
        migrations.RenameField(
            model_name='derivativevolumelmcgroup',
            old_name='derivative_group',
            new_name='derivative_lmc_group',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AlterUniqueTogether(
            name='derivativevolumelmcgroup',
            unique_together={('derivative_lmc_group', 'year', 'month')},
        ),
        migrations.RenameModel(
            old_name='DerivativeGroupLMC',
            new_name='DerivativeLMCGroup',
        ),
        migrations.CreateModel(
            name='ScenarioGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('data', models.JSONField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectStaffCostGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.BigIntegerField()),
                ('project_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.projectgroup')),
                ('project_staff_cost_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.projectstaffcosttask')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
            options={
                'unique_together': {('project_group', 'user', 'project_staff_cost_task', 'work_date')},
            },
        ),
        migrations.CreateModel(
            name='ProjectStaffCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('hours', models.FloatField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
                ('project_staff_cost_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.projectstaffcostgroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DerivativeVolumeLMCDerivativeConstelliumConnectionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('derivative_constellium_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.derivativeconstelliumgroup')),
                ('derivative_lmc_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.derivativelmcgroup')),
            ],
            options={
                'unique_together': {('derivative_lmc_group', 'derivative_constellium_group')},
            },
        ),
        migrations.CreateModel(
            name='DerivativeVolumeLMCDerivativeConstelliumConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('take_rate', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
                ('derivative_volume_lmc_derivative_constellium_connection_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.derivativevolumelmcderivativeconstelliumconnectiongroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CacheIntermediate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intermediate_name', models.CharField(max_length=100)),
                ('dependencies', models.JSONField()),
                ('relevant_scenario_dict', models.JSONField()),
                ('data', models.BinaryField()),
            ],
            options={
                'unique_together': {('intermediate_name', 'dependencies', 'relevant_scenario_dict')},
            },
        ),
    ]