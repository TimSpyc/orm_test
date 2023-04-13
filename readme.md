# DB Tables:
## Group Table
Table for topic (e.g. ProjectUser). It contains all unique information to search for the group and unchangeable columns. Unique columns are also unchangeable and need to be labeled as unique. These unique columns are a group definition. This group definition serves as a unique identifier if the group ID is unknown. If there is no unique combination, the group does not contain a unique_together argument.
GroupTables inherit from GroupTable Class and name ends with "Group"
```python
    class ProjectUserGroup(GroupTable):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

        class Meta:
            unique_together = ('user', 'project_group')

        def __str__(self):
            return f"{self.user} - {self.project_group}"
```

## Data Table
Table for data storage of user changeable data. Allways contains the following columns: date, creator, active. There is only ONE Data Table for each Topic.
```python
    class DerivativeConstellium(models.Model):
        derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete=models.CASCADE)
        name = models.CharField(max_length=255)
        sop_date = models.DateField()
        eop_date = models.DateField()
        derivative_type = models.ForeignKey(DerivativeType, on_delete=models.CASCADE)
        estimated_price = models.FloatField()
        estimated_weight = models.FloatField()
        prediction_accuracy = models.ForeignKey(PredictionAccuracy, on_delete=models.CASCADE)
        date = models.DateTimeField()
        creator = models.ForeignKey(User, on_delete=models.CASCADE)
        active = models.BooleanField()

        def __str__(self):
            return self.name
```

"ManyToMany" fields should always be specified without "s" at the end. "ForeignKey" and "ManyToMany" fields are always named after the referenced object and written in snake_case."

```python
    class DerivativeConstellium(models.Model):
        ...
        derivative_type = models.ForeignKey(DerivativeType, on_delete=models.CASCADE)
        project_user_role = models.ManyToManyField(ProjectUserRole, blank=True)
        ...
```

## Reverence Table
Table for reverence data (not user changeable data). It uneditable by user and allways contains a active column.
```python
class ProjectUserRole(models.Model):
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name
```