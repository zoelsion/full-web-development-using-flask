from datetime import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey,Date,Float,DateTime
from sqlalchemy.orm import relationship
from flask import Markup, url_for
from flask_appbuilder import Model
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address =  Column(String(564), default='Street ')
    birthday = Column(Date)
    personal_phone = Column(String(20))
    personal_cellphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'))
    contact_group = relationship("ContactGroup")

    def __repr__(self):
        return self.name

class Country(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class CountryStats(Model):
    id = Column(Integer, primary_key=True)
    stat_date = Column(Date, nullable=True)
    population = Column(Float)
    unemployed_perc = Column(Float)
    poor_perc = Column(Float)
    college = Column(Float)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    country = relationship("Country")

    def college_perc(self):
        if self.population != 0:
            return (self.college * 100) / self.population
        else:
            return 0.0

    def college_perc(self):
        if self.population != 0:
            return (self.college * 100) / self.population
        else:
            return 0.0

    def month_year(self):
        return datetime.datetime(self.stat_date.year, self.stat_date.month, 1)


class PersonGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    address = Column(String(264))
    phone1 = Column(String(20))
    phone2 = Column(String(20))
    taxid = Column(Integer)
    notes = Column(Text())

    def __repr__(self):
        return self.name


class Person(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date)
    photo = Column(ImageColumn(thumbnail_size=(30, 30, True), size=(300, 300, True)))
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    personal_email = Column(String(64))
    notes = Column(Text())
    business_function = Column(String(64))
    business_phone = Column(String(20))
    business_celphone = Column(String(20))
    business_email = Column(String(64))
    person_group_id = Column(Integer, ForeignKey("person_group.id"))
    person_group = relationship("PersonGroup")

    def photo_img(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="' +
                url_for("PersonModelView.show", pk=str(self.id)) +
                '" class="thumbnail"><img src="' +
                im.get_url(self.photo) +
                '" alt="Photo" class="img-rounded img-responsive"></a>'
            )
        else:
            return Markup(
                '<a href="' +
                url_for("PersonModelView.show", pk=str(self.id)) +
                '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive">'
                '</a>'
            )

    def photo_img_thumbnail(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="' +
                url_for("PersonModelView.show", pk=str(self.id)) +
                '" class="thumbnail"><img src="' +
                im.get_url_thumbnail(self.photo) +
                '" alt="Photo" class="img-rounded img-responsive"></a>'
            )
        else:
            return Markup(
                '<a href="' +
                url_for("PersonModelView.show", pk=str(self.id)) +
                '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive">'
                '</a>'
            )