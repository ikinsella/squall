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
                     SubmitField,
                     StringField,
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
       1. Ensuring the filename is correct
       2. TODO: Enforcing Proper Formating
       3. TODO: Ensuring it is properly formatted
       4. TODO: Ensuring the arguments are correct for the batch
    """
    def __init__(self, message='Valid file extensions: ".yaml" or ".yml"'):
        self.message = message

    def __call__(self, form, field):  # TODO: 2,3,& 4
        try:
            # yamldata = yaml.load(field.data)
            # assert isinstance(yamldata, dict)
            filename = field.data.filename
            assert '.' in filename
            assert filename.rsplit('.', 1)[1] in set(['yaml', 'yml'])
            assert field.has_file()
        except AssertionError:  # Is not properly formatted
            raise ValidationError(self.message)


class ValidResultsBatch(object):
    """ Validates A Batch To Add Results To By:
        1. Ensuring the batch doesn't already have an associated results file
    """
    def __init__(self, message='Selected Batch Is Already Completed'):
        self.message = message

    def __call__(self, form, field):
        try:
            # batch = Batch.query.filter_by(id=field.data).first()
            # assert not batch.completed
            pass
        except AssertionError:
            raise ValidationError(self.message)


class ValidResultsFile(object):
    """Validates An Uploaded Results Parameter File By:
        1. Ensuring the filename is correct
        2. TODO: Ensuring it belongs to a batch without results
        3. TODO: Ensuring it is properly formatted
    """
    def __init__(self, message='Valid file extensions: ".json"'):
        self.message = message

    def __call__(self, form, field):  # TODO: 2 & 3
        try:
            filename = field.data.filename
            assert '.' in filename
            assert filename.rsplit('.', 1)[1] in set(['json'])
            assert field.has_file()
        except AssertionError:  # Is not properly formatted
            raise ValidationError(self.message)


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
    optional = BooleanField(u'Optional')

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


class URLForm(Form):
    url = TextField('URL', validators=[DataRequired()])

    def validate(self):
        if super(DataSetForm, self).validate():
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
    # urls = FieldList(TextField(u'URLs', [DataRequired(), # Ian's old code
    #                                      URL(),
    #                                      Length(max=256)]),
    #                  min_entries=1, max_entries=10)
    urls = FieldList(FormField(URLForm), min_entries=1, max_entries=1)
    # urls = FieldList(TextField(), min_entries=1, max_entries=10)

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
    # batch = SelectField(u'Batch', [DataRequired()], coerce=int)
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
