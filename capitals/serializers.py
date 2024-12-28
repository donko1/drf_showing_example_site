# Крч, это сделано для того, что бы переформатировать модель в json и пиши то, что нужно передать.
# Для проверки зайди в shell, напиши Capital.objects.first() и закинь его в сериализатор
# CapitalSerializer(Capital.objects.first()).data
import re
from rest_framework import serializers
from .models import Capital
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]
        read_only_fields = ["date_joined"]


class CapitalSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Capital
        fields = ["capital_city", "capital_population", "country", "author", "pk"]

    def validate_capital_city(self, value):
        allowed_chars = set(" -.'")
        for char in value:
            if not (char.isalpha() or char in allowed_chars):
                raise serializers.ValidationError(
                    f"Название столицы '{value}' содержит недопустимый символ '{char}'"
                )
        return value.strip()

    def create(self, validated_data):  # Такой create - встроенный!!!
        return Capital.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.capital_city = validated_data.get(
            "capital_city", instance.capital_city
        )
        instance.capital_population = validated_data.get(
            "capital_population", instance.capital_population
        )
        instance.author = validated_data.get("author", instance.author)
        instance.save()
        return instance


class CapitalNestedSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Capital
        fields = ["capital_city", "capital_population", "country", "author"]

    def create(self, validated_data):  # Такой create - встроенный!!!
        return Capital.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.capital_city = validated_data.get(
            "capital_city", instance.capital_city
        )
        instance.capital_population = validated_data.get(
            "capital_population", instance.capital_population
        )
        instance.country = validated_data.get("country", instance.country)
        instance.save()
        return instance


class CapitalDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capital
        fields = ["capital_city", "capital_population", "country", "author"]
        depth = 1  # Автоматически сериализует связанные поля на глубину 1


class CapitalDepth2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Capital
        fields = ["capital_city", "capital_population", "country", "author"]
        depth = 2  # Более глубокая сериализация


class CapitalFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capital
        fields = ["capital_city", "capital_population", "country", "author"]
        # Без depth - плоское представление
