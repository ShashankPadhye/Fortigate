FortiGate Config Parser v2.0A CLI Python tool for auditing FortiGate full-configuration files.
Features
Stream-based parsing (low memory footprint)
Regex or preset-based pattern matching
Configurable context lines
Exact-match mode for scripting
Meaningful exit codes for automation
PrerequisitesPython 3.6+
(Optional) Git for cloning the repository
Installation# Clone the repository
git clone https://github.com/your-org/fgt_cfg_parser.git
cd fgt_cfg_parser

# (Optional) Make the script executable
chmod +x fgt_cfg_parser.pyUsagepython3 fgt_cfg_parser.py [--list-presets] -f <config_file> -p <pattern> [options]OptionDescription--list-presetsList all built-in preset patterns and exit (no other flags required).-f, --fileRequired. Path to the FortiGate full-configuration file.-p, --patternRequired. Regex pattern or preset name to search for.-c, --contextContext lines before/after each match (default: 10).--ignore-casePerform case-insensitive matching.--exactPrint only the matching text (omit context lines).Running ExamplesList presets (no file needed):
python3 fgt_cfg_parser.py --list-presetsSearch a preset with default context:
python3 fgt_cfg_parser.py -f fortigate.conf -p admin-timeoutExact-match for ssh lines:
python3 fgt_cfg_parser.py -f fortigate.conf -p ssh --exactCustom regex, short context, ignore case:
python3 fgt_cfg_parser.py \
  -f fortigate.conf \
  -p "^config firewall policy" \
  -c 5 --ignore-casePresetsUse --list-presets to display the full list. Common examples include:
PresetDescriptionadmin-timeoutAdmin session timeoutsshSSH service configurationpassword-policyPassword complexity and historyconsole-timeoutConsole session timeoutpost-login-bannerPost-login banner textallowaccessInterface access protocolsdnsDNS server settingsntpNTP server configurationtimezoneSystem timezonelog-memoryMemory-based logginglog-diskDisk-based loggingfortianalyzerFortiAnalyzer logging settingssyslogdSyslog server configurationpolicy-logtrafficFirewall policy traffic logginguser-radiusRADIUS server configurationsnmpSNMP community & trap settingsusbUSB device controlicmpICMP forwarding and restrictionsbroadcast-forwardBroadcast forwarding policyExit CodesCodeMeaning0Matches found and displayed1File not found or inaccessible2No matches found for the given patternContributingPull requests and issues are welcome!Potential enhancements:
JSON/CSV output modes
Parallel scanning of multiple patterns
Section grouping (e.g., full system global block display)
Happy FortiGate auditing!
