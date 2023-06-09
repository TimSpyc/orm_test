# Generated by Django 4.2.1 on 2023-06-13 07:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('company_name', models.CharField(max_length=255)),
                ('group_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerPlant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('city', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DerivativeConstelliumGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DerivativeLMCGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lmc_full_code', models.CharField(max_length=255, unique=True)),
                ('lmc_model_code', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('lmc_full_code', 'lmc_model_code')},
            },
        ),
        migrations.CreateModel(
            name='DerivativeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PredictionAccuracy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
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
        migrations.CreateModel(
            name='ProjectUserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('role_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RevisionLMC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('revision_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('microsoft_id', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('last_login', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
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
            name='ProjectUserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.projectgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
            options={
                'unique_together': {('user', 'project_group')},
            },
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
                ('project_user_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.projectusergroup')),
                ('project_user_role', models.ManyToManyField(to='backend.projectuserrole')),
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
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('project_number', models.CharField(max_length=255, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
                ('project_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.projectgroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DerivativeVolumeLMCGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)])),
                ('month', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('derivative_lmc_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.derivativelmcgroup')),
            ],
            options={
                'unique_together': {('derivative_lmc_group', 'year', 'month')},
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
            name='DerivativeVolumeLMC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('volume', models.PositiveIntegerField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
                ('derivative_lmc_volume_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.derivativevolumelmcgroup')),
                ('revision_lmc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.revisionlmc')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DerivativeLMC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('region', models.CharField(max_length=255)),
                ('trade_region', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('local_model_line', models.CharField(max_length=255)),
                ('local_program_code', models.CharField(max_length=255)),
                ('local_production_model', models.CharField(max_length=255)),
                ('global_production_model', models.CharField(max_length=255)),
                ('gvw', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=255)),
                ('production_type', models.CharField(max_length=255)),
                ('vehicle_type', models.CharField(db_column='type', max_length=255)),
                ('regional_size', models.CharField(max_length=255)),
                ('regional_body_type', models.CharField(max_length=255)),
                ('regional_status', models.CharField(max_length=255)),
                ('global_size', models.CharField(max_length=255)),
                ('global_body_type', models.CharField(max_length=255)),
                ('global_status', models.CharField(max_length=255)),
                ('sop_date', models.DateField()),
                ('eop_date', models.DateField()),
                ('next_facelift', models.DateField()),
                ('last_actual', models.DateField()),
                ('design_lead_location', models.CharField(max_length=255)),
                ('design_lead_country', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
                ('derivative_lmc_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.derivativelmcgroup')),
                ('design_lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='design_leads', to='backend.customer')),
                ('global_make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='global_makes', to='backend.customer')),
                ('local_make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_makes', to='backend.customer')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturers', to='backend.customer')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.customerplant')),
                ('revision_lmc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.revisionlmc')),
                ('sales_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_groups', to='backend.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='derivativeconstelliumgroup',
            name='project_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.projectgroup'),
        ),
        migrations.CreateModel(
            name='DerivativeConstellium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('sop_date', models.DateField()),
                ('eop_date', models.DateField()),
                ('estimated_price', models.FloatField()),
                ('estimated_weight', models.FloatField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
                ('derivative_constellium_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.derivativeconstelliumgroup')),
                ('derivative_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.derivativetype')),
                ('prediction_accuracy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.predictionaccuracy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CacheManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_name', models.CharField(max_length=100)),
                ('group_id', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('data', models.BinaryField()),
            ],
            options={
                'unique_together': {('manager_name', 'group_id', 'date')},
            },
        ),
        migrations.CreateModel(
            name='CacheIntermediate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intermediate_name', models.CharField(max_length=100)),
                ('identification', models.JSONField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('data', models.BinaryField()),
            ],
            options={
                'unique_together': {('intermediate_name', 'identification', 'start_date', 'end_date')},
            },
        ),
    ]
