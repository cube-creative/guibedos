import json
from Qt import QtWidgets
from guibedos import css
from guibedos import declarative_form as df


def _is_mail_valid(text):
    return '@' in text and ' ' not in text


root_property = df.Group('personal_info', caption="Personnal Information", properties=(
    df.Text('name', caption='Name', default='Jean'),
    df.Text('surname', caption='Surname', default='Bauchefort'),
    df.Text('password', caption='Password'),
    df.Label('info', caption='This is a bit of text\nthat can help your user understand what is going'),
    df.Group('address', caption="Address", layout=df.HORIZONTAL, properties=(
        df.Text('street', caption='Street', default='123 Fake Street'),
        df.Enum('country', caption='Country', items=[
            df.Enum.Item('France', data='FR'),
            df.Enum.Item('Etats-Unis', data='US', current=True),
            df.Enum.Item('Chine ', data='CH'),
        ])
    )),
    None,
    df.Integer('age', caption='Age', default=27, range_=[18, 109]),
    df.Text('email', caption='E-mail', default='jean.bauchefort@gmail.com', validator=_is_mail_valid),
    df.Bool('single', caption='Celibataire', default=True),
    df.Filepath('profile_picture', caption='Profile picture', default='C:/test.jpg'),
    df.Group('interests', caption='Centres d interet', layout=df.FLOW, properties=(
        df.Bool('music', caption="Musique", default=False),
        df.Bool('movies', caption="Cinema", default=True),
        df.Bool('sports', caption="Sport", default=False),
        df.Bool('alcohol', caption="Alcool", default=False),
        df.Bool('cooking', caption="Cuisine", default=False),
        df.Bool('travel', caption="Voyages", default=False),
        df.Bool('theater', caption="Theatre", default=False),
        df.Bool('murder', caption="Meurtre", default=False),
        df.Bool('capitalism', caption="Capitalisme", default=False),
        df.Bool('communism', caption="Communisme", default=False),
        df.Bool('web_dev', caption="Developpement Web", default=False)
    )),
    df.List('tags', caption='Tags', default=['Personne', 'Humain'])
))


app = QtWidgets.QApplication([])
css.set_theme(app, 'light-blue')

widget = df.DeclarativeForm(df.Label('info', caption='this wont be shown'))

widget.reload(root_property)

widget.show()
app.exec_()

print(json.dumps(widget.data(), indent=2))
