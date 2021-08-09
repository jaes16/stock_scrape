from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectMultipleField, SelectField, widgets
from wtforms.validators import ValidationError, DataRequired, NumberRange, Length


class GoogleSearchForm(FlaskForm):
	term1 = StringField('Search Term', validators=[Length(min=1,max=20), DataRequired()])
	term2 = StringField('Search Term', validators=[Length(min=0,max=20)])
	term3 = StringField('Search Term', validators=[Length(min=0,max=20)])
	term4 = StringField('Search Term', validators=[Length(min=0,max=20)])
	term5 = StringField('Search Term', validators=[Length(min=0,max=20)])
	submit = SubmitField()


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

def validate_subreddit(form, field):
	subreddits = ['stocks', 'StockMarket', 'wallstreetbets', 'investing', 'business', 'finance']
	if field.data:
		if field.data not in subreddits:
			raise ValidationError('Not a valid subreddit.')

class RedditSubForm(FlaskForm):
	days = IntegerField('# of Days', validators=[NumberRange(min=1,max=10)])
	subr1 = StringField('Subreddit', validators=[Length(min=1,max=20), validate_subreddit, DataRequired()])
	subr2 = StringField('Subreddit', validators=[Length(min=0,max=20), validate_subreddit])
	subr3 = StringField('Subreddit', validators=[Length(min=0,max=20), validate_subreddit])
	subr4 = StringField('Subreddit', validators=[Length(min=0,max=20), validate_subreddit])
	subr5 = StringField('Subreddit', validators=[Length(min=0,max=20), validate_subreddit])
	submit = SubmitField()

class TwitterSearchForm(FlaskForm):
	user1 = StringField('User', validators=[Length(min=1,max=20), DataRequired()])
	user2 = StringField('User', validators=[Length(min=0,max=20)])
	user3 = StringField('User', validators=[Length(min=0,max=20)])
	user4 = StringField('User', validators=[Length(min=0,max=20)])
	user5 = StringField('User', validators=[Length(min=0,max=20)])
	submit = SubmitField()
