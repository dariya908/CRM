from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .services import mailing
from .models import *
from django.db import transaction



class CarSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='id',required=False)

    class Meta:
        model = Car
        fields = ['car_id', 'mark']


class EducationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Education
        fields = ['id', 'school_name']


class WarcraftSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Warcraft
        fields = ['id', 'military_area']


class DosierSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True)
    schools = EducationSerializer(many=True)
    war_crfts = WarcraftSerializer(many=True)

    class Meta:
        model = Dossier
        fields = ['id', 'full_name', 'image', 'cars', 'schools', 'war_crfts', 'date_birth']

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        cars_data = validated_data.pop('cars')
        schools_data = validated_data.pop('schools')
        warcrafts_data = validated_data.pop('war_crfts')
        ids_list = [car.id for car in instance.cars.all()]
        current_ids = [car['id'] for car in cars_data]
        final_list = [car_id for car_id in ids_list if car_id not in current_ids]
        print(final_list)
        for car in cars_data:
            car_id = car['id']
            car_data = Car.objects.get(id=car_id)
            for delete_id in final_list:
                delete_car = Car.objects.get(id=delete_id)
                delete_car.delete()
            car_data.mark = car['mark']
            car_data.save()
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    check_password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=(
        ('common', 'common'),
        ('warrior', 'warrior')
    ), write_only=True)
    dossier = DosierSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'check_password', 'user_type', 'dossier']

    @transaction.atomic
    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        dossier_data = validated_data.pop('dossier')
        password = validated_data.pop('password')
        check_password = validated_data.pop('check_password')
        user = User.objects.create(**validated_data)
        if password != check_password:
            raise ValidationError("Passwords don't match")
        user.set_password(password)

        if user_type == 'warrior':
            user.is_active = False
            group = Group.objects.get(name='sergeant')
            user.groups.add(group)
            mailing(user.username)
        user.save()
        cars_data = dossier_data.pop('cars')
        schools_data = dossier_data.pop('schools')
        war_data = dossier_data.pop('war_crfts')
        dossier = Dossier.objects.create(user=user, **dossier_data)

        for car in cars_data:
            Car.objects.create(dossier=dossier, **car)

        for school in schools_data:
            Education.objects.create(dossier=dossier, **school)

        for war in war_data:
            Warcraft.objects.create(dossier=dossier, **war)
        return user
