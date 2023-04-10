from django.db import migrations, models

def move_project_number(apps, schema_editor):
    Project = apps.get_model('backend', 'Project')
    ProjectGroup = apps.get_model('backend', 'ProjectGroup')

    for project_group in ProjectGroup.objects.all():
        project = Project.objects.get(project_group=project_group)
        project.project_number = project_group.project_number
        project.save()

class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_small_changes_on_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_number',
            field=models.CharField(default="TEMP_DEFAULT", max_length=255),
        ),

        migrations.RunPython(move_project_number),

        migrations.AlterField(
            model_name='project',
            name='project_number',
            field=models.CharField(max_length=255, unique=True, null=False),
        ),

        migrations.RemoveField(
            model_name='projectgroup',
            name='project_number',
        ),
    ]