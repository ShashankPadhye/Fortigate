FortiGate Config Parser v2.0A
A CLI Python tool for auditing FortiGate full-configuration files.

# Features
Stream-based parsing for low memory footprint

Regex or preset-based pattern matching

Configurable context lines before and after match

Exact-match mode for easy scripting

Meaningful exit codes for automation

# Prerequisites
Python 3.6+

(Optional) Git (for cloning this repo)

Installation

# Clone the repository
git clone https://github.com/ShashankPadhye/Fortigate.git
cd Fortigate

# (Optional) Make the script executable
chmod +x fortigate.py

Usage

python3 fortigate.py [--list-presets] -f <config_file> -p <pattern> [options]
# Options
Option	Description
--list-presets	List all built-in preset patterns and exit (no other flags required).
-f, --file	(Required) Path to the FortiGate full-configuration file.
-p, --pattern	(Required) Regex pattern or preset name to search for.
-c, --context	Context lines before/after each match (default: 10).
--ignore-case	Perform case-insensitive matching.
--exact	Print only the matching text (omit context lines).

Examples
🔍 List presets
python3 fortigate.py --list-presets

Search a preset with default context
python3 fortigate.py -f fortigate.conf -p admin-timeout

Exact-match for lines
python3 fortigate.py -f fortigate.conf -p ssh --exact

Custom regex, short context, ignore case
python3 fortigate.py \
  -f fortigate.conf \
  -p "^config firewall policy" \
  -c 5 --ignore-case
Presets

Use --list-presets to display the full list. Some commonly used ones:
