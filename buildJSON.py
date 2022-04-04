#build state JSON

import config
import state
import json
from datetime import datetime
from datetime import timezone
import pytz

def getStateJSON():

        now = datetime.now()
        data = {}
        
        data['SkyWeather2Version'] = config.SWVERSION
        data['SampleDateTime'] = now.strftime("%m/%d/%y, %H:%M:%S %Z%z")
        data['UTCTime'] = datetime.utcnow().isoformat()
        data['lastMainReading'] = state.lastMainReading
        data['lastIndoorReading'] = state.lastIndoorReading
        data['mainID'] = state.mainID
        data['insideID'] = state.insideID

        data['OutdoorTemperature'] = state.OutdoorTemperature
        data['OutdoorHumidity'] = state.OutdoorHumidity
        data['IndoorTemperature'] = state.IndoorTemperature
        data['IndoorHumidity'] = state.IndoorHumidity
        data['Rain60Minutes'] = state.Rain60Minutes
        data['SunlightVisible'] = state.SunlightVisible
        data['SunlightUVIndex'] = state.SunlightUVIndex 
        data['WindSpeed'] = state.WindSpeed
        data['WindGust'] = state.WindGust 
        data['WindDirection'] = state.WindDirection 
        data['TotalRain'] = state.TotalRain 
        data['BarometricTemperature'] = state.BarometricTemperature
        data['BarometricPressure'] = state.BarometricPressure
        data['Altitude'] = state.Altitude
        data['BarometricPressureSeaLevel'] = state.BarometricPressureSeaLevel
        data['barometricTrend'] = state.barometricTrend
        data['pastBarometricReading'] = state.pastBarometricReading
        data['AQI'] = state.AQI
        data['Hour24_AQI'] = state.Hour24_AQI

        data['Last_Event'] = state.Last_Event
        data['English_Metric'] = config.English_Metric 
        data['batteryVoltage'] = state.batteryVoltage
        data['batteryCurrent'] = state.batteryCurrent
        data['solarVoltage'] = state.solarVoltage
        data['solarCurrent'] = state.solarCurrent
        data['loadVoltage'] = state.loadVoltage
        data['loadCurrent'] = state.loadCurrent
        data['batteryPower'] = state.batteryPower
        data['solarPower'] = state.solarPower
        data['loadPower'] = state.loadPower
        data['batteryCharge'] = state.batteryCharge
        data['SolarMAXLastReceived'] = state.SolarMAXLastReceived
        data['SolarMaxInsideTemperature'] = state.SolarMaxInsideTemperature
        data['SolarMaxInsideHumidity'] = state.SolarMaxInsideHumidity
        data['fanState'] = state.fanState

        return json.dumps(data)
    
    
def getStateJSON_all():
        """
             Returns a list of json messages based on state variables
        """
        states_list = []
        for single_state in state.MWR2Array:
            #now = datetime.now()
            data = {}
            #Time is converted to UTC time
            get_time = datetime.strptime(single_state['time'], "%Y-%m-%d %H:%M:%S")
            time_utc = get_time.astimezone(pytz.UTC)
            time_utc = time_utc.replace(tzinfo=timezone.utc)
            #data['time'] = time_utc.isoformat()
            data['time'] = time_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")

            data['model'] = single_state['model']
            data['device'] = single_state['device']
            data['id'] = single_state['id']
            data['batterylow'] = single_state['batterylow']
            data['avewindspeed'] = single_state['avewindspeed']
            data['gustwindspeed'] = single_state['gustwindspeed']
            data['winddirection'] = single_state['winddirection']
            data['cumulativerain'] = single_state['cumulativerain']
            #Temp converted to F
            wTemp = (single_state['temperature'] - 400)/10.0
            if (wTemp > 140.0):
                 print("Temp Error")
                 data['temperature'] = -140.0
            else:
                 data['temperature'] = round(((wTemp - 32.0)/(9.0/5.0)),2)
            data['humidity'] = single_state['humidity']
            data['light'] = single_state['light'] 
            data['uv'] = single_state['uv']
            data['mic'] = single_state['mic'] 
            data['mod'] = single_state['mod'] 
            data['freq'] = single_state['freq'] 
            data['rssi'] = single_state['rssi']
            data['snr'] = single_state['snr']
            data['noise'] = single_state['noise']
            data['gateway_id'] = config.Gateway_Id
            states_list.append(json.dumps(data))
        return states_list
