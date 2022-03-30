from django.db import models
from django_fsm import transition, FSMIntegerField
from django.contrib import admin


'''
Next steps:
UI to display current values in a gauge (Gießcounter per day oder letzter Sensor Wert)
UI to display values over time (Sensor Wert über den Tag, Flüssigkeit über die Zeit)
Nice style sheets

2 Cron Jobs. 
- 1 Job alle 10 Minuten zum Sensor Auslesen
- 1 Job alle Stunde von Abends um 19 Uhr bis morgens um 9 Uhr zum gießen.

Plant States:
- HAPPY
- THIRSTY
- WATERED

HAPPY => THIRSTY: Sensor below Threshold
THIRSTY => WATERED: Plant has been watered
WATERED => HAPPY: Sensor above Threshold
WATERED => THIRSTY: SENSOR (still) below Threshold

'''

#Giesomat data model


#MasterData

class Plant(models.Model):
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

    @transition(field=current_status, source=PLANT_STATE_THIRSTY, target=PLANT_STATE_THIRSTY)
    @transition(field=current_status, source=PLANT_STATE_HAPPY, target=PLANT_STATE_THIRSTY)
    def is_thirsty(self):
        #self.save()
        return

    #@transition(field=current_status, source=PLANT_STATE_WATERED, target=PLANT_STATE_WATERED)
    @transition(field=current_status, source=PLANT_STATE_THIRSTY, target=PLANT_STATE_WATERED)
    def is_watered(self):
        #self.save()
        return

    @transition(field=current_status, source=PLANT_STATE_HAPPY, target=PLANT_STATE_HAPPY)
    @transition(field=current_status, source=PLANT_STATE_WATERED, target=PLANT_STATE_HAPPY)
    def is_happy(self):
        #self.save()
        return

    @transition(field=current_status, source=PLANT_STATE_THIRSTY, target=PLANT_STATE_THIRSTY)
    @transition(field=current_status, source=PLANT_STATE_WATERED, target=PLANT_STATE_THIRSTY)
    def is_still_thirsty(self):
        #self.save()
        return
    
    @admin.display(
        boolean=True,
        ordering='current_status',
        description='Ordered by current status.',
    )
    def __str__(self):
        return self.plant_name

class Sensor(models.Model):
    gpio_pin = models.IntegerField(help_text='Raspberry Pi GPIO Pin of the sensor.')
    max_sensor_value = models.IntegerField(help_text='Calibration parameter: Maximum value that the sensor returns when it is in water.')
    min_sensor_value = models.IntegerField(default = 0, help_text='Calibration parameter: Minimum value that the sensor returns when it is completely dry.')
    sensor_threshold = models.IntegerField(help_text='Threshold of watering the plant. In percentage of minimum / maximum sensor value')
    def __str__(self):
        return 'Sensor ' + str(self.id)

class Pump(models.Model):
    gpio_pin = models.IntegerField(help_text='Raspberry Pi GPIO Pin of the pump.')
    water_flow_per_minute = models.IntegerField(default = 5000, help_text='Calibration parameter: The water flow through the pump per minute in milli liter')
    def __str__(self):
        return 'Pump ' + str(self.id)

class Valve(models.Model):
    gpio_pin = models.IntegerField(help_text='Raspberry Pi GPIO Pin of the valve.')
    time_offset = models.IntegerField(default = 0, help_text='Optional calibration parameter: The time it takes from starting the pump until the water reaches the plant.')
    def __str__(self):
        return 'Valve ' + str(self.id)

class PlantTechnical(models.Model):
    plant = models.ForeignKey(Plant, on_delete =models.CASCADE, null=True, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete = models.CASCADE,null=True, blank=True)
    pump = models.ForeignKey(Pump, on_delete = models.CASCADE,null=True, blank=True)
    valve = models.ForeignKey(Valve, on_delete = models.CASCADE,null=True, blank=True)
    def __str__(self):
        return 'Technical information for ' + str(self.plant)

class PlantHistoryWater(models.Model):
    plant = models.ForeignKey(Plant, on_delete =models.CASCADE, null=True, blank=True)
    water_volume = models.DecimalField(max_digits=9, decimal_places=2, default=0, help_text='How much water was given to the plant in ml?')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return 'Water information for ' + str(self.plant) + ' at ' + str(self.timestamp)

    

#Plant
    #ID
    #Name
    #WaterNeed
    #Sensor
    #Pump
    #Valve

#Sensor
    #ID
    #GpioPin
    #Max
    #Min
    #Threshold
#Pump
    #ID
    #GpioPin
    #WaterFlow
#Valve
    #ID
    #GpioPin
    #TimeOffset (?)

#Plant
    #ID
    #Name
    #WaterNeed
    #Sensor
    #Pump
    #Valve

#Transaction Data

#PlantCurrentState
    #ID
    #PlantID
    #State
    #StateChanged
    #Active

#PlantHistoryWater
    #ID
    #Plant
    #Timestamp
    #Water_Volume
    #TTL


#PlantHistorySensor
    #ID
    #PlantID
    #SensorID
    #Timestamp
    #SensorValue
    #TTL