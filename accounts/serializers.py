from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from accounts.models import Profile


class RegisterSerializer(RegisterSerializer):
    def save(self, request):
        print(1)
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = []

    def update(self, instance, validated_data):
        request = self.context['request']
        instance.avatar = validated_data.pop('avatar')
        instance.user = request.user
        instance.save()
        return instance
