from rest_framework import serializers
from .models import Person




class PeopleSerializer(serializers.ModelSerializer):


    class Meta:
        model = Person
        fields = '__all__'


    def validate(self,data):
        speacial_character = "!@#$%^&*()_+-=,<>/"
        if any(c in speacial_character for c in data['name']):
            raise serializers.ValidationError('Name cannot contain special chars')
        if data['age'] < 18:
            raise serializers.ValidationError('age should not be leass than 18')
        
        return data