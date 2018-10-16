from django.contrib.auth.models import AbstractUser

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])  # 得到所有的编程语言
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())  # 得到所有的配色风格


class Snippet(models.Model):
    """创建代码片段类"""
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    title = models.CharField(max_length=100, blank=True, default='',verbose_name='标题')  # 标题
    code = models.TextField(verbose_name='代码')  # 代码
    linenos = models.BooleanField(default=False)  # 行数
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)  # 语言
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)  # 风格
    # 认证和权限
    owner = models.ForeignKey('snippets.User', related_name='snippets', on_delete=models.CASCADE)  # 关联用户字段
    highlighted = models.TextField()  # 代码高亮

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        使用pygments库来生成能使代码高亮的HTML代码
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)


"""  通过扩展AbstractUser的自定义模块来扩展用户模型  """
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tb_user'
