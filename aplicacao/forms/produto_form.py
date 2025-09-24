from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import IntegerField
from wtforms.validators import DataRequired, Length, Optional

class ProdutoForm(FlaskForm):
    codproduto = IntegerField('Código', render_kw={"readonly": True}, validators=[Optional()])
    descricao = StringField('Descrição', validators=[DataRequired(), Length(min=3, max=100)])
