from flask_wtf import Form

from wtforms import (TextField,
                     PasswordField,
                     BooleanField,
                     TextAreaField,
                     SelectField,
                     SelectMultipleField,
                     FileField)

from wtforms import validators

from appname.models import User


class AlgorithmForm(Form):
    name = TextField(u'Name')
    description = TextAreaField(u'Desciption')
    tags = SelectMultipleField(u'Tags', coerce=int)


class ImplementationForm(Form):
    algorithm = SelectField(u'Algorithm', coerce=int)
    name = TextField(u'Name')
    address = TextField(u'Address')
    executable = TextField(u'Executable')
    description = TextAreaField(u'Desciption')
    tags = SelectMultipleField(u'Tags', coerce=int)


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
    description = TextAreaField(u'Desciption')
    tags = SelectMultipleField(u'Tags', coerce=int)


class ExperimentForm(Form):
    name = TextField(u'Name')
    algorithms = SelectMultipleField(u'Algorithms', coerce=int)
    collections = SelectMultipleField(u'Collections', coerce=int)
    description = TextAreaField(u'Desciption')
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
