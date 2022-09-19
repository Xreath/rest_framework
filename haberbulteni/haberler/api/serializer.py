from dataclasses import field
from pprint import pprint
from rest_framework import serializers
from haberler.models import Makale

from datetime import datetime
from datetime import date
from django.utils.timesince import timesince


class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()

    class Meta:
        model = Makale
        fields = '__all__'
        # fields = ['yazar', 'baslik', 'metin']
        # exclude = ['yazar', 'baslik', 'metin']
        read_only_fields = ['id', 'yaratilma_tarihi', 'güncelleneme_tarihi']

    def get_time_since_pub(self, object):
        now = datetime.now()
        pub_date = object.yayımlanma_tarihi

        if object.aktif == True:
            return timesince(pub_date, now)
        else:
            return 'Aktif Değil'

    def validate_yayımlanma_tarihi(self, tarihdegeri):

        today = date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError(
                'Yayımlanma tarihi ileri bir tarih olamaz!')
        return tarihdegeri

    def validate(self, attrs):
        if attrs['baslik'] == attrs['aciklama']:
            raise serializers.ValidationError("Başlık ve Açıklama Aynı Olamaz")
        else:
            return attrs


class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayımlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    güncelleneme_tarihi = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayımlanma_tarihi = validated_data.get(
            'yayımlanma_tarihi', instance.yayımlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance
