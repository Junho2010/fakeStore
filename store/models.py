# coding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''
    用户表，新增QQ和Mobile字段
    '''
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-id']


    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

class Ad(models.Model):
    '''
    广告表
    '''
    title = models.CharField(max_length=50, verbose_name='标题')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=1, verbose_name='排序顺序')
    class Meta:
        verbose_name = '广告'
        verbose_name_plural = '广告'
        ordering = ['index', 'id']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Category(models.Model):
    '''
    分类表，其中0代表男，1代表女
    '''
    typ = models.CharField(max_length=20, verbose_name='所属大类')
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=1, verbose_name='分类排序')
    sex = models.IntegerField(default=0, verbose_name='性别')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['index', 'id']

    def __str__(self):
        sex_str = '男' if self.sex == 0 else '女'
        return '{}---{}'.format(self.name, sex_str)

    def __unicode__(self):
        return self.__str__


class Brand(models.Model):
    '''
    品牌
    '''
    name = models.CharField(max_length=30, verbose_name='品牌名称')
    index = models.IntegerField(default=1, verbose_name='排序顺序')

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = '品牌'
        ordering = ['index', 'id']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name='尺寸')
    index = models.IntegerField(default=1, verbose_name='排序顺序')

    class Meta:
        verbose_name = '尺寸'
        verbose_name_plural = '尺寸'
        ordering = ['index', 'id']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    '''
    标签
    '''
    name = models.CharField(max_length=30, verbose_name='标签')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Clothing(models.Model):
    '''
    商品
    '''
    category = models.ForeignKey(Category, verbose_name='分类')
    name = models.CharField(max_length=30, verbose_name='名称')
    brand = models.ForeignKey(Brand, verbose_name='品牌')
    size = models.ManyToManyField(Size, verbose_name='尺寸')
    old_price = models.FloatField(default=0.0, verbose_name='原价')
    new_price = models.FloatField(default=0.0, verbose_name='现价')
    discount = models.FloatField(default=1, verbose_name='折扣')
    desc = models.CharField(max_length=100, verbose_name='简介')
    sales = models.IntegerField(default=0, verbose_name='销量')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    num = models.IntegerField(default=0, verbose_name='库存')
    image_url_i = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/default.jpg', verbose_name='展示图片路径')
    image_url_l = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/default.jpg', verbose_name='详情图片路径1')
    image_url_m = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/default.jpg', verbose_name='详情图片路径2')
    image_url_r = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/default.jpg', verbose_name='详情图片路径3')
    image_url_c = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/ce.jpg', verbose_name='购物车展示图片')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['id']
        
    def __str__(self):
        return '{}---{}---{}'.format(self.brand.name, self.catogory.name, self.name)

    def __unicode__(self):
        return self.__str__


class Caritem(models.Model):
    '''
    购物车条目
    '''
    clothing = models.ForeignKey(Clothing, verbose_name='购物车中产品条目')
    quantity = models.IntegerField(default=0, verbose_name='数量')
    sum_price = models.FloatField(default=0.0, verbose_name='小计')

    class Meta:
        verbose_name = '购物车条目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return self.__str__


class Cart(object):
    def __init__(self):
        self.items = []
        self.total_price = 0.0

    def add(self, clothing):
        self.total_price += clothing.new_price
        for item in self.items:
            if item.clothing.id == clothing.id:
                item.quantity += 1
                item.sum_price += clothing.new_price
                return
            else:
                self.items.append(Caritem(clothing=clothing, quantity=1, sum_price=clothing.new_price))