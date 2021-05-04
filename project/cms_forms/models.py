from django.db import models


# Create your models here.
class Topic(models.Model):
    TOPICS = [
        ('Op', 'Opera'),
        ('Mu', 'Musical'),
        ('Te', 'Teatro'),
        ('Mo', 'Moderno'),
        ('Cl', 'Clasico'),
    ]
    topic = models.CharField(max_length=2, choices=TOPICS)

    def __str__(self):
        for tuple in self.TOPICS:
            if tuple[0] == self.topic:
                return tuple[1]


class Content(models.Model):
    key = models.CharField(max_length=64)
    value = models.TextField()

    # tiene mas sentido por el formualrio de content, la ponemos la sgunda (donde tiene + sentido el form)
    topic = models.ManyToManyField(Topic)

    def __str__(self):
        return self.key + ": " + self.value


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(blank=False)
    date = models.DateTimeField('published')

    def __str__(self):
        return self.content + ": " + self.title
