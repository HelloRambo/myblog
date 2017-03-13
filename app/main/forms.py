from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from flask_pagedown.fields import PageDownField



class PostForm(Form):
    title = StringField("TITLE")
    body = PageDownField("BODY")
    summury = PageDownField('SUMMURY')
    category=StringField('CATEGORY')
    submit = SubmitField('SUBMIT')

