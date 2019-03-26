import yaml
from jinja2 import Environment, FileSystemLoader
import napalm
import json
from time import sleep



while True:

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('template.j2')

    # Read YAML file
    yaml_file = open('config.yml')
    config = yaml.load(yaml_file)

    # Render configs and print
    for device in config:

        rendered_config = template.render(**device)
        print(rendered_config)


    driver = napalm.get_network_driver('ios')

    device_information = {'hostname': '10.3.255.101',
                          'username': 'python',
                          'password': 'cisco'}

    print('Accessing 10.3.255.101 ...')

    # device.load_merge_candidat  - Napalm
    with driver(**device_information) as device:
        device.load_replace_candidate(config=rendered_config)
        print('\nDiff:')
        print(device.compare_config())

        diffs = device.compare_config()
        if len(diffs) > 0:
            print('Changes need to be applied ...')
            device.commit_config()
        else:
            print('No Changes needed ...')
            device.discard_config()
sleep(60)