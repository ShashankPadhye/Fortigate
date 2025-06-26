#!/usr/bin/env python3
"""
FortiGate Config Parser v2.0

Optimizations:
  - Stream file line-by-line (low memory).
  - Maintain a rolling buffer for pre-match context (collections.deque).
  - After-match context counter instead of slicing full list.
  - Built-in preset patterns for quick audits.
  - Optional exact-match mode to extract setting values.

Usage:
    python fgt_cfg_parser.py [--list-presets] -f <config_file> -p <pattern> [options]

Options:
    --list-presets     Show available preset patterns and exit.
    -f, --file         Path to FortiGate config file.
    -p, --pattern      Audit pattern or preset name.
    -c, --context      Number of context lines before/after match (default: 10).
    --ignore-case      Case-insensitive matching.
    --exact            Only print the matching directive/value, not full context.

Presets:
    admin-timeout, ssh, admin-ssh-grace-time, password-policy,
    console-timeout, post-login-banner, allowaccess, dns,
    ip6-allowaccess, ntp, timezone, log-memory, log-disk,
    fortianalyzer, enc-algorithm, syslogd, log-setting,
    analytics, anycast, policy-logtraffic, reset-tcp,
    user-radius, user-ldap, user-tacacs, snmp, usb,
    icmp, broadcast-forward

Example:
    # List presets only
    python fgt_cfg_parser.py --list-presets

    # Use presets for context output
    python fgt_cfg_parser.py -f fortigate.conf -p ssh

    # Exact output for scripting
    python fgt_cfg_parser.py -f fortigate.conf -p dns --exact

    # Custom regex and context
    python fgt_cfg_parser.py -f fortigate.conf -p "^config firewall policy" -c 5 --ignore-case
"""
import argparse
import re
import sys
from collections import deque

PRESETS = {
    'admin-timeout': r'admin-timeout\s+\d+',
    'ssh': r'ssh.*',
    'admin-ssh-grace-time': r'admin-ssh-grace-time\s+\d+',
    'password-policy': r'password-policy.*',
    'console-timeout': r'console-timeout\s+\d+',
    'post-login-banner': r'post-login-banner.*',
    'allowaccess': r'allowaccess.*',
    'dns': r'set\s+dns.*',
    'ip6-allowaccess': r'ip6-allowaccess.*',
    'ntp': r'set\s+ntp.*',
    'timezone': r'set\s+timezone.*',
    'log-memory': r'log memory setting',
    'log-disk': r'log disk setting',
    'fortianalyzer': r'config log fortianalyzer setting',
    'enc-algorithm': r'enc-algorithm.*',
    'syslogd': r'config log syslogd setting',
    'log-setting': r'config log setting',
    'analytics': r'set\s+analytics.*',
    'anycast': r'set\s+anycast.*',
    'policy-logtraffic': r'policy.*logtraffic.*',
    'reset-tcp': r'reset-sessionless-tcp\s+\w+',
    'user-radius': r'config user radius',
    'user-ldap': r'config user ldap',
    'user-tacacs': r'config user tacacs\+',
    'snmp': r'set\s+snmp.*',
    'usb': r'set\s+usb.*',
    'icmp': r'set\s+icmp.*',
    'broadcast-forward': r'set\s+broadcast-forward.*',
}

def parse_args():
    parser = argparse.ArgumentParser(description="Optimized FortiGate config search.")
    parser.add_argument('--list-presets', action='store_true', help='List available presets and exit')
    parser.add_argument('-f', '--file',       help='FortiGate config file')
    parser.add_argument('-p', '--pattern',    help='Pattern or preset name')
    parser.add_argument('-c', '--context',    type=int, default=10, help='Context lines before/after')
    parser.add_argument('--ignore-case', action='store_true', help='Case-insensitive')
    parser.add_argument('--exact',        action='store_true', help='Output only matching text')
    args = parser.parse_args()

    # If listing presets, no other args required
    if args.list_presets:
        return args

    # For actual searching, require file and pattern
    if not args.file or not args.pattern:
        parser.error("the following arguments are required: -f/--file, -p/--pattern")

    return args


def main():
    args = parse_args()

    if args.list_presets:
        print("Available presets:")
        for name in sorted(PRESETS):
            print(f"  • {name}")
        sys.exit(0)

    # Determine regex
    if args.pattern in PRESETS:
        pattern_str = PRESETS[args.pattern]
    else:
        pattern_str = args.pattern

    flags = re.IGNORECASE if args.ignore_case else 0
    regex = re.compile(pattern_str, flags)

    before_ctx = deque(maxlen=args.context)
    after_count = 0
    found_any = False

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            for lineno, line in enumerate(f, 1):
                if after_count > 0:
                    print(f"  {lineno:5d}: {line.rstrip()}")
                    after_count -= 1
                    continue

                match = regex.search(line)
                if match:
                    found_any = True
                    if args.exact:
                        print(match.group(0))
                    else:
                        print(f"---- Match at line {lineno} ----")
                        for i, prev in enumerate(before_ctx, start=lineno - len(before_ctx)):
                            print(f"  {i:5d}: {prev.rstrip()}")
                        print(f"> {lineno:5d}: {line.rstrip()}")
                        after_count = args.context

                before_ctx.append(line)

    except FileNotFoundError:
        print(f"Error: cannot open '{args.file}'", file=sys.stderr)
        sys.exit(1)

    if not found_any:
        msg = f"No matches for pattern '{args.pattern}'."
        print(msg, file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
