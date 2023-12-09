from django.db import models

# Create your models here.
class Topic(models.Model):

    topic = models.TextField('题目')
    type = models.CharField('类型', max_length=10, default='s')
    # 类型：s选择题，c填空题

    photo = models.ImageField('附图', upload_to='image', null=True, blank=True)

    def __str__(self):
        return f'题目{self.id}'

class Selections(models.Model):

    select = models.TextField('选项')
    select2 = models.ImageField('图片选项', upload_to='image', null=True, blank=True)
    explain = models.TextField('选项讲解', default='无')
    judge = models.BooleanField('选择正误', default=False, null=True, blank=True)
    fill = models.TextField('填空正确答案',  null=True, blank=True)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.select

class KnowledgePoints(models.Model):

    point = models.TextField('知识点')
    type = models.CharField('知识点分类', max_length=20, null=True, blank=True)
    science_education_edition = models.CharField('教科版小节', max_length=20, null=True, blank=True)

    video = models.FileField('视频', upload_to='video', null=True, blank=True)
    url = models.URLField('链接', null=True, blank=True)
    text = models.TextField('文字讲解', null=True, blank=True)
    photo = models.ImageField('图形解释', upload_to='image', null=True, blank=True)

    select = models.ManyToManyField(Selections)

    def __str__(self):
        return self.point