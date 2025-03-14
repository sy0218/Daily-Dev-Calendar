#!/usr/bin/python3
import configparser

class ConfigLoader:
    CONFIG_PATH = "/Data_pj_job/selenium/conf/collector.properties"

    @staticmethod
    def get_conf_values(properties_type):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ConfigLoader.CONFIG_PATH)

        def get(section, key):
            return config.get(section, key)

        return [
            get("url", f"{properties_type}.collector.url"),
            int(get("start_id", f"{properties_type}.collector.start")),
            int(get("end_id", f"{properties_type}.collector.end"))
        ]
