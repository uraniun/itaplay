from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Player(models.Model):
    player_name = models.CharField(max_length=50)
    player_description = models.CharField(max_length=500)
    player_mac_address = models.CharField(max_length=17)
    player_status = models.BooleanField(default=False)

    def set_player(self, arg):
        self = Player(**arg)
        self.save()

    def delete_player(self, player_id):
        self = Player.objects.get(id = player_id)
        self.delete()
    @classmethod
    def get_player(cls, player_id=None):
        if player_id==None:
            return cls.objects.all()
        return cls.objects.get(id=player_id)
