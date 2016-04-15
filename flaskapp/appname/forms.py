from flask_wtf import Form

from wtforms import (TextField,
                     PasswordField,
                     BooleanField,
                     TextAreaField,
                     SelectField,
                     SelectMultipleField,
                     IntegerField,
                     FieldList,
                     ValidationError,
                     FormField)

from wtforms.validators import (DataRequired,
                                Optional,
                                Length,
                                NumberRange,
                                URL)

from flask_wtf.file import (FileField,
                            FileRequired)

from appname.models import (User,
                            Algorithm,
                            Implementation,
                            DataCollection,
                            DataSet,
                            Experiment,
                            Batch,
                            Tag)
import wtforms
import yaml
import json
import copy
import numpy as np


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
    """Validates An Uploaded Parameter File By:
       1. TODO: Ensuring it is properly formatted
       2. TODO: Ensuring the arguments are correct for the batch
    """
    def __init__(self, message='Uploaded File Improperly Formatted'):
        self.message = message

    def __call__(self, form, field):  # TODO: Param Validation
        """Upload and parse yaml file to ensure proper formatting"""
        try:
            # Validate Presence of Yaml File
            filename = field.data.filename
            assert '.' in filename
            assert filename.rsplit('.', 1)[1] in set(['yaml', 'yml'])
            assert field.has_file()
            # Validate & Parse Contents of Yaml File
            field.data = self.parse(yaml.load(field.data))
        except AssertionError:
            raise ValidationError('Valid file extensions: ".yaml" or ".yml"')
        except:  # TODO: Identify possible Error Types
            raise ValidationError(self.message)

    def parse(self, params):
        """ Expands Yaml Fields List Of Param Files For Each Job"""

        try:  # If Expand Fields Doesn't Exist, Nothing To Be Done
            expand_fields = params['ExpandFields']
            del params['ExpandFields']
        except KeyError:
            return params

        # Copy Only Static Fields
        static_data = copy.copy(params)
        for field in expand_fields:
            if isinstance(field, list):  # TODO: Make More Robust/Elegant
                for subfield in field:
                    del static_data[subfield]
            else:
                del static_data[field]

        # Count Number Of Values Per Expand Field
        field_lengths = np.zeros(len(expand_fields))
        for idx, field in enumerate(expand_fields):
            if isinstance(field, list) or isinstance(field, tuple):
                subfields = [len(params[key]) for key in field]
                if not all(map(lambda x: x is subfields[0], subfields)):
                    raise RuntimeError('Incompatible Length: ExpandFields')
                field_lengths[idx] = subfields[0]
            else:
                field_lengths[idx] = len(params[field])

        enum_params = [static_data for _ in xrange(int(field_lengths.prod()))]

        # Enumerate Expand Fields
        for cdx, enum_param in enumerate(enum_params):
            for idx, field in zip(
                    np.unravel_index(cdx, field_lengths), expand_fields):
                if isinstance(field, list) or isinstance(field, tuple):
                    for k in field:
                        enum_param[k] = params[k][idx]
                else:
                    enum_param[field] = params[field][idx]
        return enum_params


class ValidResultsFile(object):
    """Validates An Uploaded Results Parameter File By:
        1. Ensuring the filename/extension is correct
        2. TODO: Ensuring it is properly formatted
    """
    def __init__(self, message='Uploaded File Improperly Formatted'):
        self.message = message

    def __call__(self, form, field):
        try:
            # Validate Presence of JSON File
            filename = field.data.filename
            assert '.' in filename
            assert filename.rsplit('.', 1)[1] in set(['json'])
            assert field.has_file()
            field.data = self.parse(field.data)  # Parse & Format Results JSON
        except AssertionError:
            raise ValidationError('Valid file extensions: ".json"')
        except:
            raise ValidationError(self.message)

    def parse(self, json_file):
        """Sift through results, validate contents, & format"""
        return [dict(id=jid, **results)
                for jid, results in json.load(json_file).iteritems()]


class ValidResultsBatch(object):
    """ Validates A Batch To Add Results To By:
        1. Ensuring the batch doesn't already have an associated results file
    """
    def __init__(self, message='Selected Batch Is Already Completed'):
        self.message = message

    def __call__(self, form, field):
        try:
            batch = Batch.query.filter_by(id=field.data).first()
            assert not batch.completed
            pass
        except AssertionError:
            raise ValidationError(self.message)


class URLForm(wtforms.Form):
    url = TextField('URL', validators=[DataRequired(), URL()])

    def validate(self):
        if super(URLForm, self).validate():
            return True  # If Our Validators Pass
        return False


class ScriptForm(wtforms.Form):
    path = TextField('Path', validators=[DataRequired()])

    def validate(self):
        if super(ScriptForm, self).validate():
            return True  # If Our Validators Pass
        return False


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
    url_forms = FieldList(FormField(URLForm), min_entries=1, max_entries=10)

    setup_scripts = FieldList(FormField(ScriptForm),
                              min_entries=1,
                              max_entries=10)
    executable = TextField(u'Executable', [DataRequired(),
                                           Length(max=64)])

    def validate(self):
        if super(ImplementationForm, self).validate():
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
    description = TextAreaField(u'Description', [Optional(),
                                                 Length(max=512)])
    tags = SelectMultipleField(u'Tags', [Optional()],
                               coerce=int)

    url_forms = FieldList(FormField(URLForm), min_entries=1, max_entries=10)

    def validate(self):
        if super(DataSetForm, self).validate():
            return True  # If Our Validators Pass
        return False


class ExperimentForm(Form):
    name = TextField(u'Name', [DataRequired(),
                               UniqueName(Experiment),
                               Length(max=64)])
    description = TextAreaField(u'Description', [Optional(),
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
    params = FileField(u'Parameter File', [FileRequired(),
                                           ValidParamFile()])
    memory = IntegerField(u'Memory (MB)', [DataRequired(),
                                           NumberRange()])
    disk = IntegerField(u'Disk Space (KB)', [DataRequired(),
                                             NumberRange()])
    flock = BooleanField(u'Flock')
    glide = BooleanField(u'Glide')
    tags = SelectMultipleField(u'Tags', [Optional()],
                               coerce=int)

    def validate(self):  # TODO Validate Param File
        if super(BatchForm, self).validate():
            return True  # If Our Validators Pass
        return False


class DownloadBatchForm(Form):
    batch = SelectField(u'Batch', [DataRequired()], coerce=int)

    def validate(self):
        if super(DownloadBatchForm, self).validate():
            return True
        return False


class UploadResultsForm(Form):
    batch = SelectField(u'Batch', [DataRequired(),
                                   ValidResultsBatch()], coerce=int)
    results = FileField(u'Results.json', [FileRequired(),
                                          ValidResultsFile()])

    def validate(self):
        if super(UploadResultsForm, self).validate():
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

        # if our validators do not pass
        if not super(LoginForm, self).validate():
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
    launch_directory = TextField(u'HTCondor Submit Node Launch Directory',
                                 [DataRequired(), Length(max=128)])
    password = PasswordField(u'Password', [DataRequired(), Length(max=64)])

    def validate(self):

        # if our validators do not pass
        if not super(CreateUserForm, self).validate():
            return False

        # Does the user exist
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            return True

        self.username.errors.append('Username Unavailable')
        return False

""" TODO: For Parameter Validation
class ArgumentForm(Form):
    name = TextField(u'Name', [DataRequired(),
                               Length(max=64)])
    data_type = SelectField(u'Data Type', [DataRequired()],
                            choices=[(0, 'Int'),
                                     (1, 'Float'),
                                     (2, 'Array'),
                                     (3, 'String'),
                                     (4, 'Boolean')])
    optional = BooleanField(u'Optional')

    def validate(self):
        if super(ArgumentForm, self).validate():
            return True  # If Our Validators Pass
        return False
"""

class DisplayAllForm(Form):

    algorithms = SelectField(u'Algorithms', [Optional()],
                               coerce=int)
    implementations = SelectField(u'Implementations', [Optional()],
                                    coerce=int)
        
    def validate(self):
        if super(AlgorithmForm, self).validate():
            return True  # If Our Validators Pass
        return False

