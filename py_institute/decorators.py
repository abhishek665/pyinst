from functools import wraps
from device_detector import DeviceDetector
from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup
from .models import UserDeviceInfo, IP
from django.contrib.auth.models import User


# location of incoming request
def get_location(myfunc):
    @wraps(myfunc)
    def wrap(request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        print(ip)

        if str(ip) == '127.0.0.1':
            return myfunc(request)

        user_agent = request.headers.get('User-Agent')
        device_type = DeviceDetector(user_agent).parse().device_type()
        print(device_type)

        url = f'https://tools.keycdn.com/geo?host={ip}'
        req = requests.get(url)

        soup = BeautifulSoup(req.content, 'lxml')

        a = soup.find('div', {'id': 'geoResult requirements'})
        a = a.find('dl')
        a = a.find_all('dd')
        data = {'user_agent': user_agent, 'device_type': device_type, 'ip': ip}
        data_list = ['city', 'state', 'postal_code', 'country', 'region', 'lat_long', 'date']
        for i in range(0, len(a)):
            data[data_list[i]] = a[i].text

        print(data)

        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            data['user'] = user
            device = UserDeviceInfo(**data)
            device.save()
            return myfunc(request)
        else:
            try:
                my_ip_list = IP.objects.get(ip=ip)
                data['ip_ref'] = my_ip_list
                UserDeviceInfo(**data).save()
                return myfunc(request)
            except Exception as e:
                save_ip = IP(ip=ip)
                save_ip.save()
                data['ip_ref'] = save_ip
                UserDeviceInfo(**data).save()
                return myfunc(request)

    return wrap
