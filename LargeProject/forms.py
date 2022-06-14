from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField, RadioField, SelectMultipleField, SelectField, validators, EmailField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed

class AddForm(FlaskForm):
    name = StringField("Name of Shoe: ", [validators.DataRequired(), validators.length(min = 1, max = 20, message="Too Long/Short")])
    shoetype = SelectField('Shoe Type: ', choices = [('Lifestyle', 'Lifestyle'), ('Sports', 'Sports'), ('Dress', 'Dress')], validators=[DataRequired()])
    condition = SelectField('Condition: ', choices = [('New', 'New'), ('Used-Like New', 'Used-Like New'), ('Used-Good', 'Used-Good'), ('Used-Acceptable', 'Used-Acceptable')], validators = [DataRequired()])
    description = StringField("Description: " , [validators.DataRequired(), validators.length(min = 1, max = 30, message="Too Long/Short")])
    gender = RadioField("Sex: ", choices = [('Mens', 'Mens'), ('Womens', 'Womens')], validators = [DataRequired()])
    size = IntegerField('Size: ', [validators.DataRequired(), validators.NumberRange(min = 1, max = 16, message="Too Large/Small!")])
    price = StringField('Price', validators = [DataRequired()] )
    quantity = IntegerField('Quantity: ', [validators.DataRequired(), validators.NumberRange(min = 1, max = 50, message="Too Much/Little!")])
    file = FileField("Image(Jpg or Png Only): ", validators = [DataRequired()])
    contact = EmailField("Contact Email(This is not secure btw!)" , validators = [DataRequired()])
    accesscode = StringField("Your own code to delete your entry later!", [validators.DataRequired(), validators.length(min = 4, max = 20, message="Not Secure, range 4-20")])
    submit = SubmitField("Post Shoes")

class DelForm(FlaskForm):
    accesscode = StringField("Input Your Access Code If You Want to Delete Your Product with this Code", validators = [DataRequired()])
    submit = SubmitField("Delete-If it exists")

class EditForm(FlaskForm):
    accesscode = StringField("Input Your Access Code If You Want to Edit Your Product with this Code", validators = [DataRequired()])
    name = StringField("Name of Shoe: ", [validators.DataRequired(), validators.length(min = 1, max = 20, message="Too Long/Short")])
    shoetype = SelectField('Shoe Type: ', choices = [('Lifestyle', 'Lifestyle'), ('Sports', 'Sports'), ('Dress', 'Dress')], validators=[DataRequired()])
    condition = SelectField('Condition: ', choices = [('New', 'New'), ('Used-Like New', 'Used-Like New'), ('Used-Good', 'Used-Good'), ('Used-Acceptable', 'Used-Acceptable')], validators = [DataRequired()])
    description = StringField("Description: " , [validators.DataRequired(), validators.length(min = 1, max = 30, message="Too Long/Short")])
    gender = RadioField("Sex: ", choices = [('Mens', 'Mens'), ('Womens', 'Womens')], validators = [DataRequired()])
    size = IntegerField('Size: ', [validators.DataRequired(), validators.NumberRange(min = 1, max = 16, message="Too Large/Small!")])
    price = StringField('Price', validators = [DataRequired()] )
    quantity = IntegerField('Quantity: ', [validators.DataRequired(), validators.NumberRange(min = 1, max = 50, message="Too Much/Little!")])
    file = FileField("Image(Jpg or Png Only): ", validators = [DataRequired()])
    contact = EmailField("Contact Email(This is not secure btw!)" , validators = [DataRequired()])
    submit = SubmitField("Edit-If it exists")
