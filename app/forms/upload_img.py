from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from flask_uploads import UploadSet, IMAGES
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

images = UploadSet('images', IMAGES)


class UploadImage(FlaskForm):
    img = FileField('Add Image',
                    validators=[FileRequired(), FileAllowed(images,
                                                            'Images only!')])

