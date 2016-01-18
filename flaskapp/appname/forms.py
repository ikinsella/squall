from flask_wtf import Form

from wtforms import (TextField,
                     PasswordField,
                     BooleanField,
                     TextAreaField,
                     SelectField,
                     SelectMultipleField,
                     FileField,
                     IntegerField,
                     FieldList,
                     ValidationError)

from wtforms.validators import (DataRequired,
                                Optional,
                                Length,
                                NumberRange,
                                URL)

from appname.models import (User,
                            Algorithm,
                            Implementation,
                            DataCollection,
                            DataSet,
                            Experiment,
                            Batch,
                            Tag)

import yaml


class UniqueName(object):
    """Validates An Objects Selected Name to Ensure It Has A Unique Name"""
    def __init__(self, cls, message=None):
        self.cls = cls
        if not message:
            message = "{} Name Unavailable".format(self.cls.__name__)
        self.message = message

    def __call__(self, form, field):
        """ Function Used To Validate Form Field """
        if self.cls.query.filter_by(_name=field.data).first() is not None:
            raise ValidationError(self.message)


class ValidParamFile(object):
    """Validates An Uploaded Parameter File To Enforce Proper Formating"""
    def __init__(self, message="Uploaded Parameter File Improperly Formatted"):
        self.message = message

    def __call__(self, form, field):
        try:  # Can be read by yaml.load
            yamldata = yaml.load(field.data)
            assert isinstance(yamldata, dict)
        except IOError:  # Cannot be read by parser
            ValidationError(self.message)
        except AssertionError:  # Is not properly formatted
            ValidationError(self.message)


class AlgorithmForm(Form):
    name = TextField(u'Name', [DataRequired(),
                               UniqueName(Algorithm),
                               Length(max=64)])
    description = TextAreaField(u'Desciption', [Optional(),
                                                Length(max=512)])
    tags = SelectMultipleField(u'Tags', [Optional()],
                               coerce=int)

    def validate(self):
        if super(AlgorithmForm, self).validate():
            return True  # If Our Validators Pass
        return False


class ImplementationForm(Form):
    algorithm = SelectField(u'Algorithm', [DataRequired()], coerce=int)
    name = TextField(u'Name', [DataRequired(),
                               UniqueName(Implementation),
                               Length(max=64)])
    description = TextAreaField(u'Desciption', [Optional(),
                                                Length(max=512)])
    tags = SelectMultipleField(u'Tags', [Optional()],
                               coerce=int)
    urls = FieldList(TextField(u'URLs', [DataRequired(),
                                         URL(),
                                         Length(max=256)]),
                     min_entries=1, max_entries=10)
    setup_scripts = FieldList(TextField(u'Setup Scripts', [DataRequired(),
                                                           Length(max=256)]),
                              min_entries=1, max_entries=10)
    executable = TextField(u'Executable', [DataRequired(),
                                           Length(max=64)])

    def validate(self):
        if super(ImplementationForm, self).validate():
            return True  # If Our Validators Pass
        return False


class ArgumentForm(Form):
    name = TextField(u'Name', [DataRequired(),
                               Length(max=64)])
    data_type = SelectField(u'Data Type', [DataRequired()],
                            choices=[(0, 'Int'),
                                     (1, 'Float'),
                                     (2, 'Array'),
                                     (3, 'String'),
                                     (4, 'Boolean')])
    optional = BooleanField(u'Optional', [DataRequired()])

    def validate(self):
        if super(ArgumentForm, self).validate():
            return True  # If Our Validators Pass
        return False


class DataCollectionForm(Form):
    name = TextField(u'Name', [DataRequired(),
                               UniqueName(DataCollection),
                               Length(max=64)])
    description = TextAreaField(u'Desciption', [Optional(),
                                                Length(max=512)])
    tags = SelectMultipleField(u'Tags', [Optional()],
                               coerce=int)

    def validate(self):
        if super(DataCollectionForm, self).validate():
            return True  # If Our Validators Pass
        return False


class DataSetForm(Form):
    data_collection = SelectField(u'Data Collection', [DataRequired()],
                                  coerce=int)
    name = TextField(u'Name', [DataRequired(),
                               UniqueName(DataSet),
                               Length(max=64)])
    description = TextAreaField(u'Desciption', [Optional(),
                                                Length(max=512)])
    tags = SelectMultipleField(u'Tags', [Optional()],
                               coerce=int)
    urls = FieldList(TextField(u'URLs', [DataRequired(),
                                         URL(),
                                         Length(max=256)]),
                     min_entries=1, max_entries=10)

    def validate(self):
        if super(DataSetForm, self).validate():
            return True  # If Our Validators Pass
        return False


class ExperimentForm(Form):
    name = TextField(u'Name', [DataRequired(),
                               UniqueName(Experiment),
                               Length(max=64)])
    description = TextAreaField(u'Desciption', [Optional(),
                                                Length(max=512)])
    tags = SelectMultipleField(u'Tags', [Optional()],
                               coerce=int)
    algorithms = SelectMultipleField(u'Algorithms', [DataRequired()],
                                     coerce=int)
    collections = SelectMultipleField(u'Collections', [DataRequired()],
                                      coerce=int)

    def validate(self):
        if super(ExperimentForm, self).validate():
            return True  # If Our Validators Pass
        return False


class BatchForm(Form):
    name = TextField(u'Name', [DataRequired(),
                               UniqueName(Batch),
                               Length(max=64)])
    description = TextAreaField(u'Desciption', [Optional(),
                                                Length(max=512)])
    experiment = SelectField(u'Experiment', [DataRequired()],
                             coerce=int)
    data_set = SelectField(u'Data Set', [DataRequired()],
                           coerce=int)
    implementation = SelectField(u'Implementation', [DataRequired()],
                                 coerce=int)
    params = FileField(u'Parameter File', [DataRequired(),
                                           ValidParamFile()])
    memory = IntegerField(u'Memory(MB)', [DataRequired(),
                                          NumberRange()])
    disk = IntegerField(u'Disk Space(KB)', [DataRequired(),
                                            NumberRange()])
    flock = BooleanField(u'Flock', [DataRequired()])
    glide = BooleanField(u'Glide', [DataRequired()])
    tags = SelectMultipleField(u'Tags', [Optional()],
                               coerce=int)

    def validate(self):  # TODO Validate Successful Job Creation
        if super(BatchForm, self).validate():
            return True  # If Our Validators Pass
        return False


class TagForm(Form):
    """ User will create new tags used to add metadata to other entities """
    name = TextField(u'Name', [DataRequired(),
                               UniqueName(Tag),
                               Length(max=64)])

    def validate(self):
        if super(TagForm, self).validate():
            return True  # If Our Validators Pass
        return False


class LoginForm(Form):
    username = TextField(u'Username', [DataRequired(),
                                       Length(max=64)])
    password = PasswordField(u'Password', [Optional(),
                                           Length(max=64)])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False
            self.username.errors.append()
            return False

        # Does the username exist
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
    username = TextField(u'Username', [DataRequired(), Length(max=64)])
    password = PasswordField(u'Password', [DataRequired(), Length(max=64)])

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
