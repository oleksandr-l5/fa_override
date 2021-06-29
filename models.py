from mongoengine import Document, StringField


class Example(Document):
    first = StringField(max_length=40)
    second = StringField()
    third = StringField()
