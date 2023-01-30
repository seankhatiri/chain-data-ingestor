from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList, validators, SelectMultipleField, TextAreaField


class RetryForm(FlaskForm):
    limit = IntegerField('limit', id='retry-limit')


class UploadForm(FlaskForm):
    limit = IntegerField('limit', id='upload-limit')
    history_time_delta = IntegerField('history_time_delta', id='upload-history-time-delta')


class FailurePipelineForm(FlaskForm):
    limit = StringField('limit', id='FailurePipeline-limit')
    run_env = StringField('run_env', id='FailurePipeline-run_env')


class MainPipelineForm(FlaskForm):
    class_ = StringField('class', id='FailurePipeline-class')
    run_env = StringField('run_env', id='FailurePipeline-run_env')

class ProcessorsForm(FlaskForm):
    processors = SelectMultipleField('processors', id='Processor-processors',
                                     choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    listings = TextAreaField('listings', id='Processor-listings')
    run_env = StringField('run_env', id='Processor-run_env')




