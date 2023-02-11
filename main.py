import json
from datetime import date
from copy import deepcopy
import logging

date_today = str(date.today())

# Configure logging
logging.basicConfig(level="INFO")
logging.info("Creating handler")
logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)

# Load resources
with open("docs/resources.json", "r") as resources_file:
    resources_json = json.loads(resources_file.read())

# Load config
with open("docs/config.json", "r") as config_file:
    config_json = json.loads(config_file.read())

# Load defaults
with open("docs/defaults.json", "r") as defaults_file:
    defaults_json = json.loads(defaults_file.read())

resources = resources_json["resources"]

output_file_dir = "reports"
output_file_name = "report-" + str(date_today)

with open(
    output_file_dir + "/" + output_file_name + ".md", "w", encoding="UTF-8"
) as output_file:

    # Build out json report
    with open(
        output_file_dir + "/" + output_file_name + ".json", "w", encoding="UTF-8"
    ) as output_json:

        # Start empty json for output report
        output_json_report = {}
        # Write intro into markdown
        output_file.write("# " + config_json["title"] + "\n")
        for description_line in config_json["description"]:
            output_file.write(description_line + "\n\n")

        # Write wrapper for DFD
        output_file.write("# Data Flow Diagram\n")
        output_file.write("```mermaid")
        output_file.write("\n")
        output_file.write("C4Context")
        output_file.write("\n")

        # Write networks wrapper
        output_json_report["networks"] = {}
        output_json_report["databases"] = {}
        output_json_report["users"] = {}
        output_json_report["systems"] = {}
        output_json_report["containers"] = {}
        # Process network resources as top wrapper
        for network in resources["networks"]:

            # Build out network config in output
            output_json_report["networks"][network["name"]] = deepcopy(
                defaults_json["networks"]
            )

            # Look for override config for network
            try:
                override_network_config = network["config"]
                logging.info("Overrides set for " + network["name"])
                for config_setting in network["config"]:
                    logging.info("Setting " + config_setting + " on " + network["name"])
                    output_json_report["networks"][network["name"]][
                        config_setting
                    ] = network["config"][config_setting]
            except KeyError:
                # No overrides set, nothing to do
                pass

            # Write network to mermaid
            output_file.write(
                "\t"
                + "Boundary(b"
                + network["name"]
                + ', "'
                + network["name"]
                + '") {'
                + "\n"
            )

            # Look for users in network
            for user in resources["users"]:
                if user["network"] == network["name"]:

                    output_json_report["users"][user["name"]] = deepcopy(
                        defaults_json["users"]
                    )
                    # Look for override config
                    try:
                        override_user_config = user["config"]
                        logging.info("Overrides set for " + user["name"])
                        for config_setting in user["config"]:
                            logging.info(
                                "Setting " + config_setting + " on " + user["name"]
                            )
                            output_json_report["databases"][user["name"]][
                                config_setting
                            ] = user["config"][config_setting]
                    except KeyError:
                        # No overrides set, nothing to do
                        logging.info("No overrides for " + user["name"])
                        pass

                    output_file.write(
                        "\t\t"
                        + "Person("
                        + user["name"]
                        + ', "'
                        + user["name"]
                        + '", "'
                        + user["description"]
                        + '")'
                        + "\n"
                    )

            # Look for databases in network
            for database in resources["databases"]:
                if database["network"] == network["name"]:

                    output_json_report["databases"][database["name"]] = deepcopy(
                        defaults_json["databases"]
                    )
                    # Look for override config for database
                    try:
                        override_database_config = database["config"]
                        logging.info("Overrides set for " + database["name"])
                        for config_setting in database["config"]:
                            logging.info(
                                "Setting " + config_setting + " on " + database["name"]
                            )
                            output_json_report["databases"][database["name"]][
                                config_setting
                            ] = database["config"][config_setting]
                    except KeyError:
                        # No overrides set, nothing to do
                        logging.info("No overrides for " + database["name"])
                        pass

                    output_file.write(
                        "\t\t"
                        + "SystemDb("
                        + database["name"]
                        + ","
                        + '"'
                        + database["name"]
                        + ' ", "'
                        + database["description"]
                        + '")'
                        + "\n"
                    )

            # Look for systems in network
            for system in resources["systems"]:
                if system["network"] == network["name"]:
                    output_file.write(
                        "\t\t"
                        + "System("
                        + system["name"]
                        + ","
                        + '"'
                        + system["name"]
                        + ' ", "'
                        + system["description"]
                        + '")'
                        + "\n"
                    )

            # Look for containers in network
            for container in resources["containers"]:
                if container["network"] == network["name"]:
                    output_file.write(
                        "\t\t"
                        + "Container("
                        + container["name"]
                        + ","
                        + '"'
                        + container["name"]
                        + ' ", "'
                        + container["description"]
                        + '")'
                        + "\n"
                    )
            output_file.write("\t" + "}" + "\n")

        # Process links between resources
        for res_links in resources["res_links"]:
            output_file.write(
                "\t"
                + "BiRel("
                + res_links["source"]
                + ","
                + res_links["destination"]
                + ', "'
                + res_links["description"]
                + '")'
                + "\n"
            )
            output_file.write("\n")
        output_file.write(
            'UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="3")' + "\n"
        )
        output_file.write("```")

        # Print final json
        final_report = json.dumps(output_json_report)
        output_json.write(final_report)
