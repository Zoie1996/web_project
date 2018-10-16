from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, User


# from django.contrib.auth.models import User

# class SnippetSerializer(serializers.HyperlinkedModelSerializer):
# # class SnippetSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     # 代码高亮
#     highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
#     class Meta:
#         model = Snippet
#         fields = ('url','id', 'highlight','title', 'code', 'linenos', 'language', 'style','owner')


class UserSerializer(serializers.ModelSerializer):
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    class Meta:
        model = User
        fields = ('url','id', 'username', 'snippets')


class SnippetSerializer(serializers.Serializer):
    id = serializers.ImageField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True)
    # 利用字段标志控制序列化器渲染到HTML页面时的的显示模板
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    style = serializers.ChoiceField(choices=STYLE_CHOICES)

    def create(self, validated_data):
        """
        给定经过验证的数据，创建并返回一个新的 Snippet 实例
        :param validated_data: 所需验证数据
        :return: 一个新的 Snippet 实例
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

    """
    from snippets.serializers import SnippetSerializer
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser
    一、序列化
    1. 创建并保存Snippet模型实例
        snippet = Snippet(code='print "hello, world"\n')
        snippet.save()
    2. 序列化数据
        serializer = Snippetdata: {'code': 'print "hello, world"\n', 'title': '', 'linenos': False, 'style'
        : 'friendly', 'language': 'python'Serializer(snippet)
        serializer., 'id': 2}
    3. 将数据渲染成json格式
        content = JSONRenderer().render(serializer.data)
        content = b'{"id":2,"title":"","code":"print \\"hello, world\\"\\n","linenos":false
,"language":"python","style":"friendly"}'
    二、反序列化
    from django.utils.six import BytesIO
    1. 读取bytes数据
        stream = BytesIO(content)
    2. 将数据渲染成dict格式
        data = JSONParser().parse(stream)
    """

