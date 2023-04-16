from rest_framework import fields, serializers

from admin_panel.models import HomePageLayout

class HomePageLayoutSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = HomePageLayout
        fields = ( 'title', 'id', 'body_text', 'image', 'created_at' )

    def get_image_url(self, obj):
        return obj.image.url

class HomePageLayoutRequestSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    body_text = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)