import uuid
from EtikTakApp.models.clients import *

def create_client():
    client = Client(uid = uuid.uuid4())
    client.save()

