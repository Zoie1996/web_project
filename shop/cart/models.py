from django.db import models


class Goods(models.Model):
    """商品模型类"""

    id = models.AutoField(primary_key=True, db_column='gid', verbose_name='编号')
    name = models.CharField(max_length=50, db_column='gname', verbose_name='商品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='gprice',verbose_name='价格')
    image = models.CharField(max_length=255, db_column='gimage',verbose_name='图片路径')

    class Meta:
        verbose_name_plural = '商品列表'
        db_table = 'tb_goods'
        ordering = ('id',)
