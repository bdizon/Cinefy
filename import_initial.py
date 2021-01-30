from django.core import serializers

with open('fixtures\initialdata.json', 'r') as fopen:
    for obj in serializers.deserialize("json", fopen.read()):
        obj.save()