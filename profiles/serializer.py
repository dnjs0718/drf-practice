import re
from enum import StrEnum

from rest_framework import serializers
from profiles.models import Profile, Label, Company


class ProfileListOrderingEnum(StrEnum):
    NAME_ASC = "name"
    NAME_DESC = "-name"
    EMAIL_ASC = "email"
    EMAIL_DESC = "-email"
    TEL_ASC = "tel"
    TEL_DESC = "-tel"


class ProfileOrderingSerializer(serializers.Serializer):
    ordering = serializers.ChoiceField(choices=[e.value for e in ProfileListOrderingEnum], required=False)


class ProfileListSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    company_id = serializers.IntegerField(source='company.id', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'img_url',
            'name',
            'email',
            'tel',
            'rank',
            'company_id',
            'company_name',
            'labels'
        ]

    def get_labels(self, obj):
        return obj.labels.values_list('name', flat=True)
    

class ProfileDetailSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    company_id = serializers.IntegerField(source='company.id', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'img_url',
            'name',
            'email',
            'tel',
            'rank',
            'company_id',
            'company_name',
            'labels',
            'memo',
            'address',
            'birthday',
            'web_site'
        ]

    def get_labels(self, obj):
        return obj.labels.values_list('name', flat=True)
    

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']


class ProfileCreateSerializer(serializers.ModelSerializer):
    labels = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Profile
        fields = [
            'img_url',
            'name',
            'email',
            'tel',
            'rank',
            'address',
            'birthday',
            'web_site',
            'memo',
            'company_id',
            'labels'
        ]
        
    def validate_birthday(self, value):
        pattern = r'^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'
        if not re.match(pattern, str(value)):
            raise serializers.ValidationError("Invalid Birthday format")
        return value
    
    def validate_company_id(self, value):
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError("Company does not exist")
        return value

    def create(self, validated_data):
        labels = validated_data.pop('labels', [])
        
        profile = Profile.objects.create(**validated_data)
        
        if labels:
            label_objects = [Label(name=label, profile=profile) for label in labels]
            Label.objects.bulk_create(label_objects)

        return ProfileDetailSerializer(profile).data