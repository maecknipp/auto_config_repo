import yaml
from jinja2 import Environment, FileSystemLoader
import napalm
import json
from time import sleep

#Gleich wie render aber mit Funktionen/ sollte einfacher sein als render.py
def enforce_config_on_device(device, template):
    router_ip = device["connection_address"]
    rendered_config = template.render(**device)
    print(rendered_config)
    # Connect to switch via napalm
    driver = napalm.get_network_driver('ios')
    device_information = {'hostname': router_ip,
                          'username': 'python',
                          'password': 'cisco'}
    # Config auf Switch mit Template vergleichen
    with driver(**device_information) as device:
        print('Access and check Diffs on Device: ' + router_ip + '\n')
        device.load_replace_candidate(config=rendered_config)
        print('\nDiff:')
        print(device.compare_config())

        # Wenn Config geändert hat, mit Template überschreiben
        diffs = device.compare_config()
        if len(diffs) > 0:
            print('Apply original config to switch' + router_ip)
            device.commit_config()
        else:
            print('No Changes needed ...')
            device.discard_config()


def enforce_config_on_all_devices():
    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('template.j2')
    # Read YAML file
    yaml_file = open('config.yml')
    config = yaml.load(yaml_file)
    # Render config on multiple Devices and print "Diff"
    for device in config:

        enforce_config_on_device(device, template)


#Script wird alle 60s ausgeführt
while True:

    enforce_config_on_all_devices()

    sleep(60)

#Push to github.com
#1. git add config.yml
#2. git add render.py
#3. git add template.j2
#4. git -m commit "Version V1.x"
#5. git push origin master
