from adventure.models import Item

items = Item.objects.all().delete()

items = {
    "Empty": "Nothing",
    "Gold": "Gold greases palms, builds empires, and instigates murder.",
    "Sword": "The razor-sharp point makes this weapon ideal to pierce your "
             "enemies and turn them into a sieve.",
    "Shield": "A lightweight shield that is easy to maneuver but strong " \
              "enough to defend off most attacks.",
    "Key": "A gleaming key with a unique design. What could it be used for?",
    "Door": "A solid oak door. You see sunlight filtering through the cracks. Unfortunately, it is locked..."
}

count = 1
for item in items.items():
    i = Item(name=item[0], description = item[1])
    i.id = count
    count += 1
    i.save()
