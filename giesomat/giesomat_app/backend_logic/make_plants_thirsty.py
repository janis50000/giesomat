from ..models import Plant

'''
WATER_MODE_CYCLICAL = 0
    WATER_MODE_HUMIDITY = 1
    WATER_MODES = (
        (WATER_MODE_CYCLICAL,'Water plant based on a fixed schedule.'),
        (WATER_MODE_HUMIDITY,'Water plant based on the measured humidity.')
    )

    PLANT_STATE_HAPPY = 0
    PLANT_STATE_THIRSTY = 1
    PLANT_STATE_WATERED = 2
    PLANT_STATES = (
        (PLANT_STATE_HAPPY,'Plant is happy.'),
        (PLANT_STATE_THIRSTY,'Plant is thirsty.'),
        (PLANT_STATE_WATERED,'Plant has been watered.')
    )

    plant_name = models.CharField(max_length=200, help_text='Name of the plant.')
    water_need = models.DecimalField(max_digits=9, decimal_places=2, default=100, help_text='How much water does the plant need each time it is watered?')
    is_active = models.BooleanField(default=True, help_text='Is this plant active?')
    current_status = FSMIntegerField(choices=PLANT_STATES, default=PLANT_STATE_HAPPY, protected=True, help_text='The current status of the plant - this field is set automatically')
    water_mode = models.SmallIntegerField(choices=WATER_MODES, default= WATER_MODE_HUMIDITY)


question = Question.objects.get(pk=question_id)
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
'''

def make_plants_thirsty():
    plants_to_water_cyclically = Plant.objects.exclude(current_status=Plant.PLANT_STATE_THIRSTY).filter(water_mode=Plant.WATER_MODE_CYCLICAL)
    for plant in plants_to_water_cyclically:
        if plant.current_status == Plant.PLANT_STATE_HAPPY:
            plant.is_thirsty()
            plant.save()
        else:
            plant.is_still_thirsty()
            plant.save()
    return
