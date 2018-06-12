from django.db import models


# Create your models here.

# 对象模型 --> 关系模型
# 实体类 --> 二维表
# # 属性 --> 列
# # 实体对象 --> 记录

# 创建部门模型
class Dept(models.Model):
    # 设置主键
    # verbose_name 设置中文
    no = models.IntegerField(primary_key=True,verbose_name='部门编号')
    name = models.CharField(max_length=20,verbose_name='部门名称')
    location = models.CharField(max_length=10,verbose_name='部门所在地')
    excellent = models.BooleanField(default=0, verbose_name='是否优秀')

    def __str__(self):
        return self.name

    # 设置一个内部类 给表重命名
    class Meta:
        db_table = 'tb_dept'


class Emp(models.Model):

    no = models.IntegerField(primary_key=True,verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='员工姓名')
    job = models.CharField(max_length=10, verbose_name='职位')
    mgr = models.IntegerField(null=True,blank=True, verbose_name='主管')
    # max_digits 精度 总共多少位  decimal_places 小数点多少位
    sal = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='工资')
    # null=True默认数据库可以放空值  blank=True 默认后台可以填空值
    comm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='奖金')
    # 创建多对一关联关系 on_delete=models.PROTECT 必须指定 不允许删除部门
    # 在实际开发中通常不使用多对多关系 --> 转化成两个一对多关系
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT, verbose_name='所在部门')

    class Meta:
        db_table = 'tb_emp'
