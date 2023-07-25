# DB Tables:
## Group Table
Table for topic (e.g. ProjectUser). It contains all unique information to search for the group and unchangeable columns. Unique columns are also unchangeable and need to be labeled as unique. These unique columns are a group definition. This group definition serves as a unique identifier if the group ID is unknown. If there is no unique combination, the group does not contain a unique_together argument.
GroupTables inherit from GroupTable Class and name ends with "Group"
```python
    class ProjectUserGroup(GroupTable):
        user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
        project_group = models.ForeignKey(ProjectGroup, on_delete=models.DO_NOTHING)

        class Meta:
            unique_together = ('user', 'project_group')

        def __str__(self):
            return f"{self.user} - {self.project_group}"
```

## Data Table
Table for data storage of user changeable data. Always contains the following columns: date, creator, active. There is only ONE Data Table for each Topic.
```python
    class DerivativeConstellium(models.Model):
        derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete=models.DO_NOTHING)
        name = models.CharField(max_length=255)
        sop_date = models.DateField()
        eop_date = models.DateField()
        derivative_type = models.ForeignKey(DerivativeType, on_delete=models.DO_NOTHING)
        estimated_price = models.FloatField()
        estimated_weight = models.FloatField()
        prediction_accuracy = models.ForeignKey(PredictionAccuracy, on_delete=models.DO_NOTHING)
        date = models.DateTimeField()
        creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
        active = models.BooleanField()

        def __str__(self):
            return self.name
```

"ManyToMany" fields should always be specified without "s" at the end. "ForeignKey" and "ManyToMany" fields are always named after the referenced object and written in snake_case.
"ForeignKey" and "ManyToMany" fields only reference Reference Table or Group Table.

```python
    class DerivativeConstellium(models.Model):
        ...
        derivative_type = models.ForeignKey(DerivativeType, on_delete=models.DO_NOTHING)
        project_user_role = models.ManyToManyField(ProjectUserRole, blank=True)
        ...
```

## Data Extension Table
Extension Table for many to one data in data table. It will always be incremented when data table is changing and contains additional data that is not manageable within the original data table. In comparison to Reverence Table the data is user changeable.

```python
    class VolumeCustomer(models.Model):
        volume_customer_group = models.ForeignKey(VolumeCustomerGroup)
        description = models.TextField()
        date = models.DateTimeField()
        creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
        active = models.BooleanField()

    class VolumeCustomerExtension(models.Model):
        volume_customer_extension = models.ForeignKey(VolumeCustomer)
        year = models.IntegerField()
        volume = models.IntegerField()
```

## Reverence Table
Table for reverence data (not user changeable data). It's uneditable by user and always contains a active column.
```python
class ProjectUserRole(models.Model):
    role_name = models.CharField(max_length=255)
    active = models.BooleanField()

    def __str__(self):
        return self.role_name
```

# Manager Classes:
## Basics
Manager classes inherit from GeneralManger. There are meant to interact with the database (read, write and update data) and deal with the data directly stored inside there linked tables. Each manager has it's own group and data table. The manager is called with it's group_id and a search_date. It's possible to use an automatic cache option with the kwarg use_cache=True.
Each value in these tables is stored inside attributes of the manager class. If there is a foreign or many-to-many relation to another data or group table the corresponding manager is linked with a @property decorator. The connected manager is not stored inside an attribute because it can change over time.
E.g.:

```python
class ProjectGroup(GroupTable):
    """
    A Django model representing a project group.
    """

    def manager(self, search_date, use_cache):
        return ProjectManager(self.id, search_date, use_cache)

    def __str__(self):
        return f'Project Group with {self.id}'


class Project(DataTable):
    """
    A Django model representing a project, including its name, project number,
    and associated project group.
    """
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False, null=True)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.DO_NOTHING)

    @property
    def group(self):
        return self.project_group

    def __str__(self):
        return self.name



class ProjectManager(GeneralManager):
    """
    A manager class for handling Project-related operations, extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectGroup model.
        data_model (models.Model): The Project model.
    """
    group_model = ProjectGroup
    data_model = Project
    data_extension_model_list = []

    def __init__(self, project_group_id, search_date=None, use_cache=True):
        """
        Initialize a ProjectManager instance.

        Args:
            project_group_id (int): The ID of the ProjectGroup instance.
            search_date (datetime.datetime, optional): The date used for filtering data. Defaults to None.
            use_cache (bool, optional): Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(group_id=project_group_id, search_date=search_date, use_cache=use_cache)


```
## Configuration
Each manager needs the class variables group_model and data_model that link to django orm models (db tables).

## General functionality
```python
all(search_date=None)
    """
    Retrieves all objects of the manager's class, optionally filtering by
    search_date.

    Args:
        search_date (datetime.date, optional): A date to filter the objects by.
            If specified, only objects with a date less than or equal to the
            search_date will be included.

    Returns:
        list: A list of manager objects, filtered by the optional search_date
            if provided.
    """

filter(search_date=None, **kwargs)
    """
    Creates a list of objects based on the given parameters.

    Keyword arguments:
    search_date (datetime.date, optional) -- An optional argument that
        specifies the search date for the objects to be created.
    **kwargs: A variable that contains key-value pairs of filter
        conditions for the database query.

    Returns:
    list -- A list of manager objects that match the filter conditions.

    Example:
    To create a list of all manager objects where the 'name' column is equal
        to 'foo': .filter(name='foo')
    """

update(creator_user_id, **kwargs)
    """
    Update the current instance with new data, uploads to db and refresh the
    cache.

    Args:
        creator_user_id (int): The ID of the user who is making the update.
        **kwargs: Key-value pairs representing the new data to be updated.
    """

deactivate(creator_user_id)
    """
    Deactivate the current instance and set active=False in db.

    Args:
        creator_user_id (int): The ID of the user who is deactivating the
            instance.
    """

create(creator_user_id, **kwargs)
    """
    Create a new instance of the current class and initialize cache.

    Args:
        creator_user_id (int): The ID of the user who is creating the new
            instance.
        **kwargs: Key-value pairs representing the data to be used for creating
            the new instance.

    Returns:
        cls: A new instance of the current manager class.
    """
```

# Intermediate Classes:
## Basics
Intermediate classes inherit from GeneralIntermediate. There are meant to combine data from multiple managers and other intermediates. Each intermediate has its own dependencies und functionality and is called with its own, not standardized arguments. But there must always be three arguments: use_cache, search_date and scenario_dict:
- use_cache=True enables using cached entries.
- search_date is necessary to get the right dependency objects.
- scenario_dict is used to apply scenarios (e.g +5% volume for BMW). It can always contain all scenarios. The relevant_scenarios for this intermediate will be extracted out of the dict.
## Configuration
To extract the relevant_scenarios you need to assign a class variable named relevant_scenario_keys. It's a list of tuples with key chains. E.g.:
```python
relevant_scenario_keys = [('volume', 'project'), ('volume', 'derivative')]
scenario_dict = {
    'other_category': ...
    'volume': {
        'project': {'id': 1, 'value': 1.15}
    }
}
```
results in: 
```python
relevant_scenarios = {
        'volume': {
        'project': {'id': 1, 'value': 1.15}
    }
}
```
All dependencies must be initialized inside the dependencies attribute (list) before calling 
```python
super().__init__()
```
This is because of cache handling. Even if you don't want to use cache, it's necessary. You can only have manager and intermediate dependencies.
