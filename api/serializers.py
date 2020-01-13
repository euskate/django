# 직렬화
# Model의 Object를 View로 가져올 때...

from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('no', 'name', 'price', 'regdate')
    
    # Calss Member .....
