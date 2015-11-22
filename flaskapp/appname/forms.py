from flask_wtf import Form

from flask import flash

from wtforms import (TextField,
                     PasswordField,
                     BooleanField,
                     TextAreaField,
                     SelectField,
                     SelectMultipleField,
                     FileField)

from wtforms import validators

from appname.models import User, Algorithm, Implementation


class AlgorithmForm(Form):
    name = TextField(u'Name',validators=[validators.required()])
    description = TextAreaField(u'Desciption',validators=[validators.optional()])
    tags = SelectMultipleField(u'Tags', coerce=int,validators=[validators.optional()])

    def validate(self):
        check_validate = super(AlgorithmForm, self).validate()
        # if our validators do not pass
        if not check_validate:
            return False
        # Does our the exist
        algorithm = Algorithm.query.filter_by(name=self.name.data).first()
        if not algorithm:
            return True

        self.name.errors.append('Algorithm name unavailable') # not functional yet
        flash('Algorithm name unavailable', 'danger')
        return False


class ImplementationForm(Form):
    algorithm = SelectField(u'Algorithm', coerce=int,validators=[validators.required()])
    name = TextField(u'Name',validators=[validators.required()])
    address = TextField(u'Address',validators=[validators.required()])
    executable = TextField(u'Executable',validators=[validators.required()])
    description = TextAreaField(u'Desciption',validators=[validators.optional()])
    tags = SelectMultipleField(u'Tags', coerce=int,validators=[validators.optional()])

    def validate(self):
        check_validate = super(ImplementationForm, self).validate()
        # if our validators do not pass
        if not check_validate:
            return False
        # Does our the exist
        implementation = Implementation.query.filter_by(name=self.name.data).first()
        if not implementation:
            return True

        self.name.errors.append('Implementation name unavailable') # not funcitonal yet
        flash('Implementation name unavailable', 'danger')
        return False


class ArgumentForm(Form):
    name = TextField(u'Name')
    data_type = SelectField(u'Data Type', choices=[(0, 'Int'),
                                                   (1, 'Float'),
                                                   (2, 'Array'),
                                                   (3, 'String'),
                                                   (4, 'Boolean')])
    optional = BooleanField(u'Optional')


class DataCollectionForm(Form):
    name = TextField(u'Name')
    description = TextAreaField(u'Desciption')
    tags = SelectMultipleField(u'Tags', coerce=int)


class DataSetForm(Form):
    name = TextField(u'Name')
    address = TextField(u'Address')
    data_collection = SelectField(u'Data Collection', coerce=int)
    description = TextAreaField(u'Desciption')
    tags = SelectMultipleField(u'Tags', coerce=int)


class ExperimentForm(Form):
    name = TextField(u'Name')
    #description = TextAreaField(u'Desciption')
    algorithms = SelectMultipleField(u'Algorithms', coerce=int)
    collections = SelectMultipleField(u'Collections', coerce=int)
    description = TextAreaField(u'Description')
    tags = SelectMultipleField(u'Tags', coerce=int)


class BatchForm(Form):
    name = TextField(u'Name')
    experiment = SelectField(u'Experiment', coerce=int)
    data_set = SelectField(u'Data Set', coerce=int)
    implementation = SelectField(u'Implementation', coerce=int)
    description = TextAreaField(u'Desciption')
    params = FileField(u'Parameter File')
    tags = SelectMultipleField(u'Tags', coerce=int)


class TagForm(Form):
    """ User will create new tags used to add metadata to other entities """
    name = TextField(u'Name')


class LoginForm(Form):
    username = TextField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.optional()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our the exist
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True


class CreateUserForm(Form):
    username = TextField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.required()])

    def validate(self):
        check_validate = super(CreateUserForm, self).validate()
        # if our validators do not pass
        if not check_validate:
            return False
        # Does our the exist
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            return True

        self.username.errors.append('Username Unavailable')
        return False
