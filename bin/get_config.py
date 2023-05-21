"""
Modules to load the configuration files for pytmac from provided data files.
"""
import json
import logging
import os
import sys

import yaml

from bin import input_validator

docs_dir = os.path.join(os.path.dirname(__file__), "../", "docs")


def resources(file):
    """
    Function to return a list of resources to be included in the package
    :return: List of resources
    """
    if file == "demo":
        file = docs_dir + "/resources.yaml"

    try:
        with open(file, "r", encoding="UTF-8") as resources_file:
            try:
                resources_yaml = yaml.safe_load(resources_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError("Failed to load RESOURCE_FILE: %s", error_message)
    except FileNotFoundError:
        raise FileNotFoundError("No resources file found at " + file)

    return resources_yaml


def config(file):
    """
    Function to return a list of config to be included in the package
    :return: List of resources
    """
    if file == "demo":
        file = docs_dir + "/config.yaml"

    try:
        with open(file, "r", encoding="UTF-8") as config_file:
            try:
                config_yaml = yaml.safe_load(config_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError("Failed to load CONFIG_FILE: %s", error_message)
    except FileNotFoundError:
        raise FileNotFoundError("No config file found at " + file)
    return config_yaml


def defaults(file):
    """
    Function to return a list of defaults to be included in the package
    :return: List of resources
    """
    if file == "demo":
        file = docs_dir + "/defaults.yaml"

    try:
        with open(file, "r", encoding="UTF-8") as default_file:
            try:
                default_yaml = yaml.safe_load(default_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError("Failed to load DEFAULTS_FILE: %s", error_message)
    except FileNotFoundError:
        raise FileNotFoundError("No defaults file found at " + file)

    return default_yaml


def security_checks(file):
    """
    Function to return a list of security_checks to be included in the package
    :return: List of resources
    """
    if file == "default":
        file = docs_dir + "/security_checks.yaml"

    try:
        with open(file, "r", encoding="UTF-8") as security_checks_file:
            try:
                security_checks_yaml = yaml.safe_load(security_checks_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError("Failed to load SECURITY_CHECKS_FILE: %s", error_message)

    except FileNotFoundError:
        raise FileNotFoundError("No security_checks file found at " + file)

    return security_checks_yaml


def swagger(file):
    """
    Function to get and return swagger file contents
    :return: List of resources
    """

    if file == "demo":
        file = docs_dir + "/swagger.json"

    try:
        with open(file, "r", encoding="UTF-8") as swagger_file:
            try:
                swagger_json = json.loads(swagger_file.read())
            except Exception as error_message:
                raise Exception("Failed to load SWAGGER_FILE: %s", error_message)
    except FileNotFoundError:
        raise FileNotFoundError("No swagger.json file found at " + file)
    return swagger_json

def settings():
    """
    Function to get and return settings file contents from .pytmac file

    :return: settings file contents
    """
    try:
        with open(".pytmac", "r", encoding="UTF-8") as settings_file:
            try:
                settings_yaml = yaml.safe_load(settings_file)
            except yaml.YAMLError as error_message:
                raise yaml.YAMLError("Failed to load SECURITY_CHECKS_FILE: %s", error_message)
    except FileNotFoundError:
        raise FileNotFoundError("No .pytmac file found in current directory")

    return settings_yaml
