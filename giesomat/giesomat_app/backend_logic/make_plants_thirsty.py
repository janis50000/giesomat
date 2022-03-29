from ..models import Plant

def make_plants_thirsty():
    #ToDo: Only active Plants!
    plants_to_water_cyclically = Plant.objects.exclude(current_status=Plant.PLANT_STATE_THIRSTY, is_active=False).filter(water_mode=Plant.WATER_MODE_CYCLICAL)
    for plant in plants_to_water_cyclically:
        if plant.current_status == Plant.PLANT_STATE_HAPPY:
            plant.is_thirsty()
            plant.save()
        else:
            plant.is_still_thirsty()
            plant.save()
    return
