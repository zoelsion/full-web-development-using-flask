from flask import render_template,redirect
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from flask_appbuilder.actions import action
from flask_appbuilder.charts.views import DirectByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count, aggregate_sum, aggregate_avg


from . import appbuilder, db
from .models import ContactGroup, Contact,CountryStats,Person, PersonGroup
class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {'contact_group':'Contacts Group'}
    list_columns = ['name','personal_cellphone','birthday','contact_group']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'address', 'contact_group']}
        ),
        (
            'Personal Info',
            {'fields': ['birthday', 'personal_phone', 'personal_cellphone'], 'expanded': False}
        ),
    ]
class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

class Group(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

"""
chart view
"""
class CountryDirectChartView(DirectByChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = 'Direct Data Example'

    definitions = [
    {
        'label': 'Unemployment',
        'group': 'stat_date',
        'series': ['unemployed_perc',
                   'college_perc']
    },
    {
        'label': 'Poor',
        'group': 'stat_date',
        'series': ['poor_perc',
                   'college_perc']
    }
]

class CountryGroupByChartView(GroupByChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = 'Statistics'

    definitions = [
        {
            'label': 'Country Stat',
            'group': 'country',
            'series': [(aggregate_avg, 'unemployed_perc'),
                       (aggregate_avg, 'population'),
                       (aggregate_avg, 'college_perc')
                      ]
        }
    ]

class PersonModelView(ModelView):
    datamodel = SQLAInterface(Person, db.session)

    list_title = "List Contacts"
    show_title = "Show Contact"
    add_title = "Add Contact"
    edit_title = "Edit Contact"

    # list_widget = ListThumbnail

    label_columns = {
        "person_group_id": "Group",
        "photo_img": "Photo",
        "photo_img_thumbnail": "Photo",
    }
    list_columns = [
        "photo_img_thumbnail",
        "name",
        "personal_celphone",
        "business_celphone",
        "birthday",
        "person_group",
    ]

    show_fieldsets = [
        ("Summary", {"fields": ["photo_img", "name", "address", "person_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "personal_email",
                ],
                "expanded": False,
            },
        ),
        (
            "Professional Info",
            {
                "fields": [
                    "business_function",
                    "business_phone",
                    "business_celphone",
                    "business_email",
                ],
                "expanded": False,
            },
        ),
        ("Extra", {"fields": ["notes"], "expanded": False}),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name", "photo", "address", "person_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "personal_email",
                ],
                "expanded": False,
            },
        ),
        (
            "Professional Info",
            {
                "fields": [
                    "business_function",
                    "business_phone",
                    "business_celphone",
                    "business_email",
                ],
                "expanded": False,
            },
        ),
        ("Extra", {"fields": ["notes"], "expanded": False}),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name", "photo", "address", "person_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "personal_email",
                ],
                "expanded": False,
            },
        ),
        (
            "Professional Info",
            {
                "fields": [
                    "business_function",
                    "business_phone",
                    "business_celphone",
                    "business_email",
                ],
                "expanded": False,
            },
        ),
        ("Extra", {"fields": ["notes"], "expanded": False}),
    ]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(PersonGroup, db.session)
    related_views = [PersonModelView]

    label_columns = {"phone1": "Phone (1)", "phone2": "Phone (2)", "taxid": "Tax ID"}
    list_columns = ["name", "notes"]


class PersonChartView(GroupByChartView):
    datamodel = SQLAInterface(Person)
    chart_title = "Grouped Persons"
    label_columns = PersonModelView.label_columns
    chart_type = "PieChart"

    definitions = [
        {"group": "person_group", "series": [(aggregate_count, "person_group")]}
    ]


"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)




    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""

db.create_all()
appbuilder.add_view(
    GroupModelView,
    "List Groups",
    icon = "fa-folder-open-o",
    category = "Contacts",
    category_icon = "fa-envelope"
)
appbuilder.add_view(
    ContactModelView,
    "List Contacts",
    icon = "fa-envelope",
    category = "Contacts"
)
appbuilder.add_view(
    Group,
    "List group Contacts",
    icon = "fa-envelope",
    category = "Contacts"
)
appbuilder.add_view(CountryDirectChartView, "Show Country Chart", icon="fa-dashboard", category="Statistics")
appbuilder.add_view(CountryGroupByChartView, "population", icon="fa-dashboard", category="Statistics")
appbuilder.add_view(
    GroupModelView(), "Group list", icon="fa-folder-open-o", category="Contacts"
)
appbuilder.add_view(
    PersonModelView(), "List Contacts", icon="fa-envelope", category="Contacts"
)
appbuilder.add_view(
    PersonChartView(), "Contacts Chart", icon="fa-dashboard", category="Contacts"
)


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
